"""
Exploratory Data Analysis — Tech Triathlon 2026 Datathon
Team BigBug

Run from project root:
    .venv\\Scripts\\python.exe src/eda.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings

warnings.filterwarnings("ignore")

# ──────────────────────────────────────────────
# Setup
# ──────────────────────────────────────────────
sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams["figure.figsize"] = (14, 6)
plt.rcParams["figure.dpi"] = 100

BASE = Path(__file__).resolve().parent.parent  # project root
GENERAL = BASE / "data" / "raw" / "General Data"
TRAIN = BASE / "data" / "raw" / "Training Data"
TEST = BASE / "data" / "raw" / "Test Data"
TEMPLATES = BASE / "data" / "raw" / "Submission Templates"

# Output directory for plots
PLOTS_DIR = BASE / "outputs" / "eda_plots"
PLOTS_DIR.mkdir(parents=True, exist_ok=True)


def save_fig(name: str):
    """Save current figure and close it."""
    plt.savefig(PLOTS_DIR / f"{name}.png", bbox_inches="tight", dpi=150)
    plt.close()


def time_to_minutes(time_str):
    """Convert HH:MM to minutes from midnight."""
    if pd.isna(time_str):
        return np.nan
    parts = str(time_str).split(":")
    return int(parts[0]) * 60 + int(parts[1])


# ──────────────────────────────────────────────
# 1. General Data — Reference Tables
# ──────────────────────────────────────────────
print("=" * 60)
print("1. GENERAL DATA — REFERENCE TABLES")
print("=" * 60)

# 1.1 Outlets
print("\n--- 1.1 Outlets ---")
outlets = pd.read_csv(GENERAL / "outlets.csv")
print(f"Shape: {outlets.shape}")
print(f"\nColumns: {list(outlets.columns)}")
print(f"\nNull counts:\n{outlets.isnull().sum()}")
print(outlets.head())

fig, axes = plt.subplots(1, 3, figsize=(18, 5))
outlets["brand"].value_counts().plot.bar(ax=axes[0], color=["#2ecc71", "#3498db", "#e74c3c"])
axes[0].set_title("Outlets by Brand")
axes[0].set_ylabel("Count")

outlets["depot"].value_counts().plot.bar(ax=axes[1], color=["#9b59b6", "#f39c12"])
axes[1].set_title("Outlets by Depot")

outlets["district"].value_counts().plot.bar(ax=axes[2], color="#1abc9c")
axes[2].set_title("Outlets by District")
axes[2].tick_params(axis="x", rotation=45)

plt.tight_layout()
save_fig("01_outlets_distribution")

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
outlets["dock_type"].value_counts().plot.bar(ax=axes[0], color="#e67e22")
axes[0].set_title("Dock Type Distribution")

outlets["parking_constraint"].value_counts().plot.bar(ax=axes[1], color="#e74c3c")
axes[1].set_title("Parking Constraints")

pd.crosstab(outlets["brand"], outlets["parking_constraint"]).plot.bar(ax=axes[2])
axes[2].set_title("Brand vs Parking Constraint")

plt.tight_layout()
save_fig("02_outlets_access")

print(f"\nUnique window_open_time values: {outlets['window_open_time'].unique()}")
print(f"Unique window_close_time values: {outlets['window_close_time'].unique()}")
print(f"\nMall outlets: {outlets['mall_window'].notna().sum()}")
print(f"Van-only outlets: {(outlets['parking_constraint'] == 'van_only').sum()}")

print("\nBrand x Depot:")
print(pd.crosstab(outlets["brand"], outlets["depot"], margins=True))

print("\nBrand x Dock Type:")
print(pd.crosstab(outlets["brand"], outlets["dock_type"], margins=True))


# 1.2 Vehicles
print("\n--- 1.2 Vehicles ---")
vehicles = pd.read_csv(GENERAL / "vehicles.csv")
print(f"Shape: {vehicles.shape}")
print(f"\nColumns: {list(vehicles.columns)}")
print(f"\nNull counts:\n{vehicles.isnull().sum()}")
print(vehicles.head())

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
vehicles["type"].value_counts().plot.bar(ax=axes[0], color=["#3498db", "#e74c3c"])
axes[0].set_title("Vehicle Type")

vehicles["temp"].value_counts().plot.bar(ax=axes[1], color=["#2ecc71", "#9b59b6"])
axes[1].set_title("Temperature Capability")

vehicles["depot"].value_counts().plot.bar(ax=axes[2], color=["#f39c12", "#1abc9c"])
axes[2].set_title("Vehicles by Depot")

plt.tight_layout()
save_fig("03_vehicles_composition")

print("\nType x Temp:")
print(pd.crosstab(vehicles["type"], vehicles["temp"], margins=True))
print("\nType x Depot:")
print(pd.crosstab(vehicles["type"], vehicles["depot"], margins=True))

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
vehicles.boxplot(column="weight_cap_kg", by="type", ax=axes[0])
axes[0].set_title("Weight Capacity by Type")
axes[0].set_xlabel("")

vehicles.boxplot(column="volume_cap_m3", by="type", ax=axes[1])
axes[1].set_title("Volume Capacity by Type")
axes[1].set_xlabel("")

vehicles.boxplot(column="weekly_fuel_quota_l", by="type", ax=axes[2])
axes[2].set_title("Weekly Fuel Quota by Type")
axes[2].set_xlabel("")

plt.suptitle("")
plt.tight_layout()
save_fig("04_vehicles_capacity")

print("\nCapacity summary by type:")
print(vehicles.groupby("type")[["weight_cap_kg", "volume_cap_m3", "weekly_fuel_quota_l", "km_per_l"]].describe().T)


# 1.3 Calendar
print("\n--- 1.3 Calendar ---")
calendar_df = pd.read_csv(GENERAL / "calendar.csv", parse_dates=["date"])
print(f"Shape: {calendar_df.shape}")
print(f"\nDate range: {calendar_df['date'].min()} to {calendar_df['date'].max()}")
print(f"\nColumns: {list(calendar_df.columns)}")
print(calendar_df.head(10))

print(f"\nTotal days: {len(calendar_df)}")
print(f"Operating days: {calendar_df['is_operating'].sum()}")
print(f"Non-operating days: {(~calendar_df['is_operating'].astype(bool)).sum()}")
print(f"Paydays: {calendar_df['is_payday'].sum()}")
print(f"Holidays: {calendar_df['is_holiday'].sum()}")
print(f"Monsoon days: {calendar_df['monsoon'].sum()}")

festivals = calendar_df[calendar_df["festival"].notna()][["date", "festival", "festival_ramp", "is_holiday"]]
print(f"\nFestivals:")
print(festivals.reset_index(drop=True))

print(f"\nISO weeks range: {calendar_df['iso_week'].min()} to {calendar_df['iso_week'].max()}")
print(f"ISO years: {calendar_df['iso_year'].unique()}")

fig, ax = plt.subplots(figsize=(16, 4))
ax.plot(calendar_df["date"], calendar_df["festival_ramp"], color="#e74c3c", alpha=0.8)
ax.fill_between(calendar_df["date"], calendar_df["festival_ramp"], alpha=0.3, color="#e74c3c")
ax.set_title("Festival Ramp Over Time")
ax.set_ylabel("festival_ramp")

paydays = calendar_df[calendar_df["is_payday"] == 1]
ax.scatter(paydays["date"], [1.05] * len(paydays), marker="v", color="green", s=50, label="Paydays", zorder=5)
ax.legend()
plt.tight_layout()
save_fig("05_calendar_festivals")


# 1.4 District Travel
print("\n--- 1.4 District Travel ---")
district_travel = pd.read_csv(GENERAL / "district_travel.csv")
print(f"Shape: {district_travel.shape}")
print(district_travel)
print(f"\nDistricts: {district_travel['district'].nunique()} unique")
print(f"Road classes: {district_travel['road_class'].unique()}")


# 1.5 Service Allowance
print("\n--- 1.5 Service Allowance ---")
service_allowance = pd.read_csv(GENERAL / "service_allowance.csv")
print(f"Shape: {service_allowance.shape}")
print(service_allowance)

print("\nService allowance (minutes) — Brand x Dock Type:")
print(service_allowance.pivot(index="brand", columns="dock_type", values="service_allowance_min"))


# 1.6 Traffic Speed
print("\n--- 1.6 Traffic Speed ---")
traffic_speed = pd.read_csv(GENERAL / "traffic_speed.csv")
print(f"Shape: {traffic_speed.shape}")
print(f"\nColumns: {list(traffic_speed.columns)}")
print(traffic_speed.head(10))
print(traffic_speed.describe())


# 1.7 Road Conditions
print("\n--- 1.7 Road Conditions ---")
road_conditions = pd.read_csv(GENERAL / "road_conditions.csv")
print(f"Shape: {road_conditions.shape}")
print(f"\nColumns: {list(road_conditions.columns)}")
print(road_conditions.head(10))
print(road_conditions.describe())

if "disruption_index" in road_conditions.columns:
    disrupted = road_conditions[road_conditions["disruption_index"] < 100]
    print(f"\nDisrupted records (disruption_index < 100): {len(disrupted)} / {len(road_conditions)}")


# ──────────────────────────────────────────────
# 2. Training Data
# ──────────────────────────────────────────────
print("\n" + "=" * 60)
print("2. TRAINING DATA")
print("=" * 60)

# 2.1 Deliveries
print("\n--- 2.1 Deliveries (Training) ---")
deliveries = pd.read_csv(TRAIN / "deliveries_train.csv")
print(f"Shape: {deliveries.shape}")
print(f"\nColumns: {list(deliveries.columns)}")
print(f"\nDtypes:\n{deliveries.dtypes}")
print(f"\nNull counts:\n{deliveries.isnull().sum()}")
print(deliveries.head())

print(f"\nUnique delivery_ids: {deliveries['delivery_id'].nunique()}")
print(f"Unique outlets: {deliveries['outlet_id'].nunique()}")
print(f"Unique routes: {deliveries['route_id'].nunique()}")
print(f"Unique vehicles: {deliveries['vehicle_id'].nunique()}")
print(f"\nDate range: {deliveries['order_date'].min()} to {deliveries['order_date'].max()}")

print(f"\nDispatch status:")
print(deliveries["dispatch_status"].value_counts())
print(deliveries["dispatch_status"].value_counts(normalize=True).mul(100).round(1))

fig, axes = plt.subplots(1, 4, figsize=(20, 5))

deliveries["brand"].value_counts().plot.bar(ax=axes[0], color=["#2ecc71", "#3498db", "#e74c3c"])
axes[0].set_title("Orders by Brand")

deliveries["depot"].value_counts().plot.bar(ax=axes[1], color=["#9b59b6", "#f39c12"])
axes[1].set_title("Orders by Depot")

deliveries["temp_requirement"].value_counts().plot.bar(ax=axes[2], color=["#1abc9c", "#e67e22"])
axes[2].set_title("Temperature Requirement")

deliveries["dispatch_status"].value_counts().plot.bar(ax=axes[3], color=["#27ae60", "#c0392b", "#7f8c8d"])
axes[3].set_title("Dispatch Status")

plt.tight_layout()
save_fig("06_deliveries_distribution")

# Order size distributions
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

deliveries["order_units"].hist(bins=50, ax=axes[0], color="#3498db", edgecolor="white")
axes[0].set_title("Order Units Distribution")
axes[0].set_xlabel("units")

deliveries["order_weight_kg"].hist(bins=50, ax=axes[1], color="#e74c3c", edgecolor="white")
axes[1].set_title("Order Weight Distribution")
axes[1].set_xlabel("kg")

deliveries["order_volume_m3"].hist(bins=50, ax=axes[2], color="#2ecc71", edgecolor="white")
axes[2].set_title("Order Volume Distribution")
axes[2].set_xlabel("m³")

plt.tight_layout()
save_fig("07_order_sizes")

print("\nOrder size summary by brand:")
print(deliveries.groupby("brand")[["order_units", "order_weight_kg", "order_volume_m3"]].describe().round(2))

# Temporal patterns — orders per day
deliveries["order_date"] = pd.to_datetime(deliveries["order_date"])
daily_orders = deliveries.groupby(["order_date", "brand"]).size().unstack(fill_value=0)

fig, ax = plt.subplots(figsize=(16, 5))
daily_orders.plot(ax=ax, alpha=0.7)
ax.set_title("Daily Order Count by Brand")
ax.set_ylabel("Number of Orders")
ax.legend(title="Brand")
plt.tight_layout()
save_fig("08_daily_orders")

# Weekly volume by depot and brand (preview of Task 2A aggregation)
deliveries_cal = deliveries.merge(
    calendar_df[["date", "iso_year", "iso_week"]],
    left_on="order_date",
    right_on="date",
    how="left",
)

weekly_vol = (
    deliveries_cal.groupby(["depot", "brand", "iso_year", "iso_week"])
    .agg(total_volume=("order_volume_m3", "sum"), order_count=("delivery_id", "count"))
    .reset_index()
)

for depot in weekly_vol["depot"].unique():
    depot_data = weekly_vol[weekly_vol["depot"] == depot]
    fig, ax = plt.subplots(figsize=(16, 4))
    for brand in depot_data["brand"].unique():
        brand_data = depot_data[depot_data["brand"] == brand]
        ax.plot(range(len(brand_data)), brand_data["total_volume"], label=brand, alpha=0.8)
    ax.set_title(f"Weekly Total Volume — {depot}")
    ax.set_ylabel("Volume (m³)")
    ax.set_xlabel("Week index")
    ax.legend()
    plt.tight_layout()
    save_fig(f"09_weekly_volume_{depot.lower()}")

# Chilled vs ambient
print("\nTemperature requirement by brand:")
print(pd.crosstab(deliveries["brand"], deliveries["temp_requirement"], margins=True))

chilled_non_fresh = deliveries[
    (deliveries["temp_requirement"] == "chilled") & (deliveries["brand"] != "Fresh")
]
print(f"\nChilled orders for non-Fresh brands: {len(chilled_non_fresh)} (should be 0)")

# Fresh outlets with dual orders
fresh_orders = deliveries[deliveries["brand"] == "Fresh"]
dual_orders = fresh_orders.groupby(["outlet_id", "order_date"]).size().reset_index(name="order_count")
print(f"\nFresh outlet-days with 2+ orders: {(dual_orders['order_count'] >= 2).sum()}")
print(f"Fresh outlet-days with exactly 1 order: {(dual_orders['order_count'] == 1).sum()}")
print(f"Max orders per Fresh outlet per day: {dual_orders['order_count'].max()}")


# 2.2 Route Legs (Training)
print("\n--- 2.2 Route Legs (Training) ---")
route_legs = pd.read_csv(TRAIN / "route_legs_train.csv")
print(f"Shape: {route_legs.shape}")
print(f"\nColumns: {list(route_legs.columns)}")
print(f"\nNull counts:\n{route_legs.isnull().sum()}")
print(route_legs.head())

# Planned vs actual
print("\nPlanned travel duration stats:")
print(route_legs["planned_travel_duration_min"].describe())

print("\nActual travel duration stats:")
print(route_legs["actual_travel_duration_min"].describe())

route_legs["travel_diff_min"] = (
    route_legs["actual_travel_duration_min"] - route_legs["planned_travel_duration_min"]
)

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

route_legs["planned_travel_duration_min"].hist(bins=50, ax=axes[0], color="#3498db", edgecolor="white")
axes[0].set_title("Planned Travel Duration")
axes[0].set_xlabel("minutes")

route_legs["actual_travel_duration_min"].hist(bins=50, ax=axes[1], color="#e74c3c", edgecolor="white")
axes[1].set_title("Actual Travel Duration")
axes[1].set_xlabel("minutes")

route_legs["travel_diff_min"].hist(bins=50, ax=axes[2], color="#9b59b6", edgecolor="white")
axes[2].set_title("Actual - Planned (Travel)")
axes[2].set_xlabel("minutes")

plt.tight_layout()
save_fig("10_travel_duration")

# Derive service time label
route_legs["arrival_min"] = route_legs["arrival_time"].apply(time_to_minutes)
route_legs["leave_min"] = route_legs["leave_outlet_time"].apply(time_to_minutes)

route_legs["service_time_min"] = route_legs["leave_min"] - route_legs["arrival_min"]
route_legs.loc[route_legs["service_time_min"] < 0, "service_time_min"] += 24 * 60

print("\nService time (derived label) stats:")
print(route_legs["service_time_min"].describe())

fig, ax = plt.subplots(figsize=(14, 5))
route_legs["service_time_min"].hist(bins=60, ax=ax, color="#2ecc71", edgecolor="white")
ax.set_title("Derived Service Time Distribution (leave_outlet_time - arrival_time)")
ax.set_xlabel("minutes")
median_val = route_legs["service_time_min"].median()
ax.axvline(median_val, color="red", linestyle="--", label=f"Median: {median_val:.1f} min")
ax.legend()
plt.tight_layout()
save_fig("11_service_time")

# Service time by brand and vehicle type
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

route_legs.boxplot(column="service_time_min", by="brand", ax=axes[0])
axes[0].set_title("Service Time by Brand")
axes[0].set_xlabel("")
axes[0].set_ylabel("minutes")

route_legs.boxplot(column="service_time_min", by="vehicle_type", ax=axes[1])
axes[1].set_title("Service Time by Vehicle Type")
axes[1].set_xlabel("")

plt.suptitle("")
plt.tight_layout()
save_fig("12_service_time_breakdown")

# Derive late label
dispatched = deliveries[deliveries["route_id"].notna()].copy()

merged = dispatched.merge(
    route_legs[["route_id", "seq", "arrival_time", "leave_outlet_time", "service_time_min"]],
    left_on=["route_id", "seq_in_route"],
    right_on=["route_id", "seq"],
    how="inner",
)
print(f"\nDispatched orders: {len(dispatched)}")
print(f"Successfully joined: {len(merged)}")
print(f"Join rate: {len(merged) / len(dispatched) * 100:.1f}%")

merged["arrival_min"] = merged["arrival_time"].apply(time_to_minutes)
merged["window_close_min"] = merged["window_close_time"].apply(time_to_minutes)
merged["is_late"] = (merged["arrival_min"] > merged["window_close_min"]).astype(int)

print(f"\nLate deliveries: {merged['is_late'].sum()} / {len(merged)} ({merged['is_late'].mean() * 100:.1f}%)")
print(f"\nLate rate by brand:")
print(merged.groupby("brand")["is_late"].agg(["mean", "sum", "count"]))

# Late delivery analysis
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

merged.groupby("brand")["is_late"].mean().plot.bar(ax=axes[0], color=["#2ecc71", "#3498db", "#e74c3c"])
axes[0].set_title("Late Rate by Brand")
axes[0].set_ylabel("Late Fraction")

merged.groupby("district")["is_late"].mean().sort_values(ascending=False).plot.bar(ax=axes[1], color="#e67e22")
axes[1].set_title("Late Rate by District")
axes[1].tick_params(axis="x", rotation=45)

late_orders = merged[merged["is_late"] == 1].copy()
late_orders["minutes_late"] = late_orders["arrival_min"] - late_orders["window_close_min"]
late_orders["minutes_late"].hist(bins=40, ax=axes[2], color="#c0392b", edgecolor="white")
axes[2].set_title("How Late? (Late Orders Only)")
axes[2].set_xlabel("minutes past window close")

plt.tight_layout()
save_fig("13_lateness_analysis")

# Route characteristics
print("\nStops per route:")
stops_per_route = route_legs.groupby("route_id").size()
print(stops_per_route.describe())

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

stops_per_route.hist(bins=30, ax=axes[0], color="#3498db", edgecolor="white")
axes[0].set_title("Stops per Route")
axes[0].set_xlabel("Number of stops")

route_legs["distance_km"].hist(bins=50, ax=axes[1], color="#e74c3c", edgecolor="white")
axes[1].set_title("Leg Distance Distribution")
axes[1].set_xlabel("km")

plt.tight_layout()
save_fig("14_route_characteristics")


# ──────────────────────────────────────────────
# 3. Test Data
# ──────────────────────────────────────────────
print("\n" + "=" * 60)
print("3. TEST DATA")
print("=" * 60)

# 3.1 Task 1 Test Inputs
print("\n--- 3.1 Task 1 Test Inputs ---")
task1_test = pd.read_csv(TEST / "task1_test_inputs.csv")
print(f"Shape: {task1_test.shape}")
print(f"\nColumns: {list(task1_test.columns)}")
print(f"\nNull counts:\n{task1_test.isnull().sum()}")
print(f"\nDate range: {task1_test['order_date'].min()} to {task1_test['order_date'].max()}")
print(f"\nDispatch status: {task1_test['dispatch_status'].unique()}")
print(task1_test.head())

# Compare test vs train distributions
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

train_brand = deliveries["brand"].value_counts(normalize=True)
test_brand = task1_test["brand"].value_counts(normalize=True)
pd.DataFrame({"Train": train_brand, "Test": test_brand}).plot.bar(ax=axes[0])
axes[0].set_title("Brand Distribution: Train vs Test")

train_depot = deliveries["depot"].value_counts(normalize=True)
test_depot = task1_test["depot"].value_counts(normalize=True)
pd.DataFrame({"Train": train_depot, "Test": test_depot}).plot.bar(ax=axes[1])
axes[1].set_title("Depot Distribution: Train vs Test")

train_temp = deliveries["temp_requirement"].value_counts(normalize=True)
test_temp = task1_test["temp_requirement"].value_counts(normalize=True)
pd.DataFrame({"Train": train_temp, "Test": test_temp}).plot.bar(ax=axes[2])
axes[2].set_title("Temp Requirement: Train vs Test")

plt.tight_layout()
save_fig("15_train_vs_test")

# Route legs test
print("\n--- Route Legs Test ---")
route_legs_test = pd.read_csv(TEST / "route_legs_test.csv")
print(f"Shape: {route_legs_test.shape}")
print(f"\nColumns: {list(route_legs_test.columns)}")
print(f"\nNull counts:\n{route_legs_test.isnull().sum()}")
print("--- Note: actual times should be missing in test ---")
print(route_legs_test.head())


# 3.2 Task 2A Test Inputs
print("\n--- 3.2 Task 2A Test Inputs ---")
task2a_test = pd.read_csv(TEST / "task2a_test_inputs.csv")
print(f"Shape: {task2a_test.shape}")
print(f"\nColumns: {list(task2a_test.columns)}")
print(f"\nForecast weeks: iso_week {task2a_test['iso_week'].min()} to {task2a_test['iso_week'].max()}")
print(f"ISO years: {task2a_test['iso_year'].unique()}")
print(f"Depots: {task2a_test['depot'].unique()}")
print(f"Brands: {task2a_test['brand'].unique()}")
print(task2a_test)


# 3.3 Task 2B Scenario
print("\n--- 3.3 Task 2B Scenario ---")
task2b_orders = pd.read_csv(TEST / "task2b_peak_day_scenarios.csv")
print(f"Shape: {task2b_orders.shape}")
print(f"\nColumns: {list(task2b_orders.columns)}")
print(task2b_orders.head())

print(f"\nOrders by brand:")
print(task2b_orders["brand"].value_counts())
print(f"\nOrders by district:")
print(task2b_orders["district"].value_counts())
print(f"\nTemp requirements:")
print(task2b_orders["temp_requirement"].value_counts())
print(f"\nParking constraints:")
print(task2b_orders["parking_constraint"].value_counts())
print(f"\nDeferred yesterday: {task2b_orders['deferred_yesterday'].sum()} orders")

# Task 2B fleet
print("\n--- Task 2B Fleet ---")
task2b_fleet = pd.read_csv(TEST / "task2b_peak_day_fleet.csv")
print(f"Shape: {task2b_fleet.shape}")
print(task2b_fleet["status"].value_counts())

available = task2b_fleet[task2b_fleet["status"] == "available"]
available_vehicles = available.merge(vehicles, on="vehicle_id", how="left")

print(f"\nAvailable vehicles: {len(available)}")
print(f"In workshop: {(task2b_fleet['status'] == 'in_workshop').sum()}")
print(f"\nAvailable vehicle breakdown:")
print(pd.crosstab(available_vehicles["type"], available_vehicles["temp"], margins=True))
print(f"\nAvailable by depot:")
print(available_vehicles["depot"].value_counts())

# Demand vs capacity
total_demand_vol = task2b_orders["order_volume_m3"].sum()
total_demand_wt = task2b_orders["order_weight_kg"].sum()

peli_available = available_vehicles[available_vehicles["depot"] == "Peliyagoda"]
total_cap_vol = peli_available["volume_cap_m3"].sum() * 2
total_cap_wt = peli_available["weight_cap_kg"].sum() * 2

print(f"\n=== Task 2B Demand vs Capacity ===")
print(f"Total demand volume: {total_demand_vol:.1f} m³")
print(f"Total capacity volume (2 trips): {total_cap_vol:.1f} m³")
print(f"Volume utilization: {total_demand_vol / total_cap_vol * 100:.1f}%")
print(f"\nTotal demand weight: {total_demand_wt:.1f} kg")
print(f"Total capacity weight (2 trips): {total_cap_wt:.1f} kg")
print(f"Weight utilization: {total_demand_wt / total_cap_wt * 100:.1f}%")
print(f"\nChilled orders: {(task2b_orders['temp_requirement'] == 'chilled').sum()}")
print(f"Available reefer vehicles (Peliyagoda): {(peli_available['temp'] == 'reefer').sum()}")
print(f"Van-only orders: {(task2b_orders['parking_constraint'] == 'van_only').sum()}")
print(f"Available vans (Peliyagoda): {(peli_available['type'] == 'van').sum()}")


# ──────────────────────────────────────────────
# 4. Submission Templates
# ──────────────────────────────────────────────
print("\n" + "=" * 60)
print("4. SUBMISSION TEMPLATES")
print("=" * 60)

sub1 = pd.read_csv(TEMPLATES / "submission_task1.csv")
sub2a = pd.read_csv(TEMPLATES / "submission_task2a.csv")
sub2b = pd.read_csv(TEMPLATES / "submission_task2b.csv")

print(f"\nTask 1 template: {sub1.shape} — columns: {list(sub1.columns)}")
print(sub1.head())

print(f"\nTask 2A template: {sub2a.shape} — columns: {list(sub2a.columns)}")
print(sub2a.head())

print(f"\nTask 2B template: {sub2b.shape} — columns: {list(sub2b.columns)}")
print(sub2b.head())


# ──────────────────────────────────────────────
# Summary
# ──────────────────────────────────────────────
print("\n" + "=" * 60)
print("EDA COMPLETE")
print("=" * 60)
print(f"\nPlots saved to: {PLOTS_DIR}")
print(f"Total plots: {len(list(PLOTS_DIR.glob('*.png')))}")
