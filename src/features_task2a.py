import pandas as pd
import numpy as np

def load_and_combine_demand_data(
    deliveries_train: pd.DataFrame, 
    task1_test_inputs: pd.DataFrame,
    calendar: pd.DataFrame
) -> pd.DataFrame:
    """Combine training and test orders, attach calendar, and compute chilled volume."""
    
    # Concatenate the datasets
    # Both have the same order-record schema: order_date, order_volume_m3, temp_requirement, depot, brand
    df = pd.concat([deliveries_train, task1_test_inputs], ignore_index=True)
    
    # Merge with calendar to get iso_year and iso_week
    # We only need specific columns from calendar
    cal_cols = ["date", "iso_year", "iso_week"]
    df = df.merge(calendar[cal_cols], left_on="order_date", right_on="date", how="left")
    
    # Chilled volume logic:
    # 1. Only Fresh has chilled demand.
    # 2. Fresh orders with temp_requirement = chilled contribute to chilled volume.
    # 3. Style and Tech always have 0 chilled volume.
    is_chilled = (df["temp_requirement"] == "chilled") & (df["brand"] == "Fresh")
    df["chilled_volume_m3"] = np.where(is_chilled, df["order_volume_m3"], 0.0)
    
    return df

def aggregate_weekly_demand(df: pd.DataFrame) -> pd.DataFrame:
    """Group by depot, brand, iso_year, iso_week and sum volumes."""
    agg_df = df.groupby(["depot", "brand", "iso_year", "iso_week"]).agg(
        total_volume_m3=("order_volume_m3", "sum"),
        chilled_volume_m3=("chilled_volume_m3", "sum")
    ).reset_index()
    
    return agg_df

def create_task2a_features(
    deliveries_train: pd.DataFrame,
    task1_test_inputs: pd.DataFrame,
    calendar: pd.DataFrame
) -> pd.DataFrame:
    """Main pipeline for Task 2A feature engineering."""
    # 1. Load and combine data
    df = load_and_combine_demand_data(deliveries_train, task1_test_inputs, calendar)
    
    # 2. Aggregate demand weekly
    agg_df = aggregate_weekly_demand(df)
    
    # Now we have a time series dataset for each (depot, brand)
    # We can add lag features or calendar features here, 
    # but that might be better done during the modeling step 
    # since we have to predict for the test set too.
    # Let's keep this as the base target dataframe.
    
    return agg_df

def add_time_series_features(df: pd.DataFrame, calendar: pd.DataFrame) -> pd.DataFrame:
    """Add lag features and calendar context for forecasting.
    
    df should be a complete grid of (depot, brand, iso_year, iso_week).
    """
    # Sort for time-series operations
    df = df.sort_values(["depot", "brand", "iso_year", "iso_week"]).copy()
    
    # Create a simple time index to handle year crossovers
    # Since we don't have a direct continuous week counter in calendar (just year/week),
    # we can use rank or cumcount if the grid is complete. 
    # Actually, let's create lag features using groupby and shift.
    
    df["lag_1_total"] = df.groupby(["depot", "brand"])["total_volume_m3"].shift(1)
    df["lag_2_total"] = df.groupby(["depot", "brand"])["total_volume_m3"].shift(2)
    df["lag_3_total"] = df.groupby(["depot", "brand"])["total_volume_m3"].shift(3)
    df["lag_4_total"] = df.groupby(["depot", "brand"])["total_volume_m3"].shift(4)
    
    df["lag_1_chilled"] = df.groupby(["depot", "brand"])["chilled_volume_m3"].shift(1)
    df["lag_2_chilled"] = df.groupby(["depot", "brand"])["chilled_volume_m3"].shift(2)
    df["lag_3_chilled"] = df.groupby(["depot", "brand"])["chilled_volume_m3"].shift(3)
    df["lag_4_chilled"] = df.groupby(["depot", "brand"])["chilled_volume_m3"].shift(4)
    
    # Add calendar context (e.g., number of holidays in the week, monsoon days, paydays)
    # Group calendar by year and week
    cal_weekly = calendar.groupby(["iso_year", "iso_week"]).agg(
        days_in_week=("date", "count"),
        paydays=("is_payday", "sum"),
        holidays=("is_holiday", "sum"),
        monsoon_days=("monsoon", "sum"),
        operating_days=("is_operating", "sum")
    ).reset_index()
    
    df = df.merge(cal_weekly, on=["iso_year", "iso_week"], how="left")
    
    return df
