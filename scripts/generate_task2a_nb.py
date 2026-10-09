import json
import os

notebook_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Task 2A: Depot Demand Forecasting\n",
            "\n",
            "This notebook builds a time-series forecasting model for depot demand. We forecast the total volume and chilled volume for each depot and brand over 10 future weeks (2026 weeks 14-23)."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import sys\n",
            "sys.path.append('..')\n",
            "import pandas as pd\n",
            "import numpy as np\n",
            "import lightgbm as lgb\n",
            "from pathlib import Path\n",
            "import warnings\n",
            "warnings.filterwarnings('ignore')\n",
            "\n",
            "from src.preprocessing import load_deliveries_train, load_task1_test_inputs, load_calendar, load_submission_template\n",
            "from src.features_task2a import create_task2a_features\n",
            "\n",
            "PROJECT_ROOT = Path('..').resolve()\n",
            "MODELS_DIR = PROJECT_ROOT / 'models'\n",
            "MODELS_DIR.mkdir(exist_ok=True)"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 1. Data Loading and Preparation"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "print('Loading data...')\n",
            "train_del = load_deliveries_train()\n",
            "test1_del = load_task1_test_inputs()\n",
            "calendar = load_calendar()\n",
            "\n",
            "# Get historical aggregated demand (2024 W1 to 2026 W13)\n",
            "history_df = create_task2a_features(train_del, test1_del, calendar)\n",
            "print(f'Historical data shape: {history_df.shape}')\n",
            "print(history_df.head())"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "We need to build a complete grid of Depot x Brand x Week from 2024 W1 to 2026 W23."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Create the calendar weekly features\n",
            "cal_weekly = calendar.groupby(['iso_year', 'iso_week']).agg(\n",
            "    days_in_week=('date', 'count'),\n",
            "    paydays=('is_payday', 'sum'),\n",
            "    holidays=('is_holiday', 'sum'),\n",
            "    monsoon_days=('monsoon', 'sum'),\n",
            "    operating_days=('is_operating', 'sum'),\n",
            "    avg_festival_ramp=('festival_ramp', 'mean')\n",
            ").reset_index()\n",
            "\n",
            "# Generate the complete grid\n",
            "depots = ['Peliyagoda', 'Kandy']\n",
            "brands = ['Fresh', 'Style', 'Tech']\n",
            "years_weeks = cal_weekly[['iso_year', 'iso_week']].drop_duplicates().values\n",
            "\n",
            "grid = []\n",
            "for d in depots:\n",
            "    for b in brands:\n",
            "        for y, w in years_weeks:\n",
            "            grid.append({'depot': d, 'brand': b, 'iso_year': y, 'iso_week': w})\n",
            "\n",
            "grid_df = pd.DataFrame(grid)\n",
            "\n",
            "# Filter out weeks past 2026 W23 since we don't need to predict beyond that\n",
            "grid_df = grid_df[(grid_df['iso_year'] < 2026) | ((grid_df['iso_year'] == 2026) & (grid_df['iso_week'] <= 23))]\n",
            "\n",
            "# Merge with historical actuals\n",
            "df = grid_df.merge(history_df, on=['depot', 'brand', 'iso_year', 'iso_week'], how='left')\n",
            "\n",
            "# Merge with calendar features\n",
            "df = df.merge(cal_weekly, on=['iso_year', 'iso_week'], how='left')\n",
            "\n",
            "# Encode categoricals\n",
            "df['depot_enc'] = df['depot'].astype('category').cat.codes\n",
            "df['brand_enc'] = df['brand'].astype('category').cat.codes\n",
            "\n",
            "print(f'Full grid shape: {df.shape}')\n",
            "display(df[df['total_volume_m3'].isna()].head(3))"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 2. Recursive Forecasting Model\n",
            "We will train a LightGBM model on data up to 2026 W13. Then we will recursively predict W14 to W23, updating the lag features at each step."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "def compute_lags(data: pd.DataFrame):\n",
            "    \"\"\"Compute lag features based on the current state of total_volume_m3 and chilled_volume_m3\"\"\"\n",
            "    df = data.sort_values(['depot', 'brand', 'iso_year', 'iso_week']).copy()\n",
            "    \n",
            "    for i in [1, 2, 3, 4, 8, 52]:\n",
            "        df[f'lag_{i}_total'] = df.groupby(['depot', 'brand'])['total_volume_m3'].shift(i)\n",
            "        df[f'lag_{i}_chilled'] = df.groupby(['depot', 'brand'])['chilled_volume_m3'].shift(i)\n",
            "        \n",
            "    # Rolling means\n",
            "    df['roll_4_total'] = df.groupby(['depot', 'brand'])['lag_1_total'].rolling(4, min_periods=1).mean().reset_index(level=[0,1], drop=True)\n",
            "    df['roll_4_chilled'] = df.groupby(['depot', 'brand'])['lag_1_chilled'].rolling(4, min_periods=1).mean().reset_index(level=[0,1], drop=True)\n",
            "    \n",
            "    return df\n",
            "\n",
            "features = [\n",
            "    'depot_enc', 'brand_enc', 'iso_week', 'paydays', 'holidays', \n",
            "    'monsoon_days', 'operating_days', 'avg_festival_ramp',\n",
            "    'lag_1_total', 'lag_2_total', 'lag_3_total', 'lag_4_total', 'lag_8_total', 'lag_52_total', 'roll_4_total'\n",
            "]\n",
            "\n",
            "chilled_features = [\n",
            "    'depot_enc', 'iso_week', 'paydays', 'holidays', \n",
            "    'monsoon_days', 'operating_days', 'avg_festival_ramp',\n",
            "    'lag_1_chilled', 'lag_2_chilled', 'lag_3_chilled', 'lag_4_chilled', 'lag_8_chilled', 'lag_52_chilled', 'roll_4_chilled'\n",
            "]"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Initial lag computation on history\n",
            "df_features = compute_lags(df)\n",
            "\n",
            "# Train-validation split for initial evaluation (optional, here we train on all history)\n",
            "train_mask = (df_features['iso_year'] < 2026) | ((df_features['iso_year'] == 2026) & (df_features['iso_week'] <= 13))\n",
            "\n",
            "train_df = df_features[train_mask].dropna(subset=['lag_4_total'])\n",
            "\n",
            "# Model for Total Volume\n",
            "model_total = lgb.LGBMRegressor(\n",
            "    n_estimators=200, \n",
            "    learning_rate=0.05, \n",
            "    max_depth=5, \n",
            "    random_state=42\n",
            ")\n",
            "model_total.fit(train_df[features], train_df['total_volume_m3'])\n",
            "\n",
            "# Model for Chilled Volume (Only trained on Fresh brand)\n",
            "train_df_fresh = train_df[train_df['brand'] == 'Fresh']\n",
            "model_chilled = lgb.LGBMRegressor(\n",
            "    n_estimators=150, \n",
            "    learning_rate=0.05,\n",
            "    max_depth=4,\n",
            "    random_state=42\n",
            ")\n",
            "model_chilled.fit(train_df_fresh[chilled_features], train_df_fresh['chilled_volume_m3'])"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 3. Generate Forecast (Weeks 14-23)"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "forecast_df = df.copy()\n",
            "\n",
            "# Forecast step-by-step\n",
            "for week in range(14, 24):\n",
            "    # Recompute lags with current state of forecast_df\n",
            "    current_state = compute_lags(forecast_df)\n",
            "    \n",
            "    # Filter to target week\n",
            "    target_mask = (current_state['iso_year'] == 2026) & (current_state['iso_week'] == week)\n",
            "    X_target = current_state[target_mask]\n",
            "    \n",
            "    if len(X_target) == 0:\n",
            "        continue\n",
            "        \n",
            "    # Predict total volume\n",
            "    pred_total = model_total.predict(X_target[features])\n",
            "    \n",
            "    # Predict chilled volume (only for Fresh)\n",
            "    pred_chilled = np.zeros(len(X_target))\n",
            "    is_fresh = X_target['brand'] == 'Fresh'\n",
            "    if is_fresh.any():\n",
            "        pred_chilled[is_fresh] = model_chilled.predict(X_target.loc[is_fresh, chilled_features])\n",
            "        \n",
            "    # Update forecast_df\n",
            "    forecast_df.loc[target_mask, 'total_volume_m3'] = np.maximum(0, pred_total)\n",
            "    forecast_df.loc[target_mask, 'chilled_volume_m3'] = np.maximum(0, pred_chilled)\n",
            "\n",
            "print('Forecasting complete.')"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 4. Prepare Submission"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "test2a = pd.read_csv(PROJECT_ROOT / 'data/raw/Test Data/task2a_test_inputs.csv')\n",
            "\n",
            "submission = test2a.merge(\n",
            "    forecast_df[['depot', 'brand', 'iso_year', 'iso_week', 'total_volume_m3', 'chilled_volume_m3']],\n",
            "    on=['depot', 'brand', 'iso_year', 'iso_week'],\n",
            "    how='left'\n",
            ")\n",
            "\n",
            "# Format according to rules\n",
            "submission.rename(columns={\n",
            "    'total_volume_m3': 'pred_total_volume_m3',\n",
            "    'chilled_volume_m3': 'pred_chilled_volume_m3'\n",
            "}, inplace=True)\n",
            "\n",
            "# Ensure Style and Tech have strictly 0 chilled volume\n",
            "submission.loc[submission['brand'] != 'Fresh', 'pred_chilled_volume_m3'] = 0.0\n",
            "\n",
            "out_cols = ['row_id', 'pred_total_volume_m3', 'pred_chilled_volume_m3']\n",
            "submission_final = submission[out_cols]\n",
            "\n",
            "print(submission_final.head(10))\n",
            "\n",
            "out_path = PROJECT_ROOT / 'data/raw/Submission Templates/submission_task2a.csv'\n",
            "submission_final.to_csv(out_path, index=False)\n",
            "print(f'\\nSaved to {out_path}')\n",
            "\n",
            "# Save the models\n",
            "model_total.booster_.save_model(MODELS_DIR / 'task2a_total_volume_lgb.txt')\n",
            "model_chilled.booster_.save_model(MODELS_DIR / 'task2a_chilled_volume_lgb.txt')"
        ]
    }
]

notebook = {
    "cells": notebook_cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.11.9"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open("notebooks/03_task2a_modeling.ipynb", "w") as f:
    json.dump(notebook, f, indent=1)

print("Notebook generated: notebooks/03_task2a_modeling.ipynb")
