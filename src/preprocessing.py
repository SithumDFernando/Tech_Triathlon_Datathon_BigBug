"""
Preprocessing module for Tech Triathlon 2026 Datathon.
Handles data loading, label construction, and train/test preparation.
"""

import pandas as pd
import numpy as np
from pathlib import Path

# ──────────────────────────────────────────────
# Paths
# ──────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = PROJECT_ROOT / "data" / "raw"
GENERAL = DATA_RAW / "General Data"
TRAIN = DATA_RAW / "Training Data"
TEST = DATA_RAW / "Test Data"
TEMPLATES = DATA_RAW / "Submission Templates"


# ──────────────────────────────────────────────
# Time utilities
# ──────────────────────────────────────────────
def hhmm_to_minutes(series: pd.Series) -> pd.Series:
    """Convert HH:MM string series to minutes from midnight.

    Returns NaN for missing values.
    """
    def _convert(val):
        if pd.isna(val):
            return np.nan
        parts = str(val).split(":")
        return int(parts[0]) * 60 + int(parts[1])

    return series.apply(_convert)


def minutes_diff(end_series: pd.Series, start_series: pd.Series) -> pd.Series:
    """Compute minute difference (end - start), handling midnight crossings.

    If the result is negative, adds 24*60 to account for crossing midnight.
    """
    diff = end_series - start_series
    diff = diff.where(diff >= 0, diff + 24 * 60)
    return diff


# ──────────────────────────────────────────────
# Data loaders
# ──────────────────────────────────────────────
def load_outlets() -> pd.DataFrame:
    """Load outlets.csv with all outlet attributes."""
    return pd.read_csv(GENERAL / "outlets.csv")


def load_vehicles() -> pd.DataFrame:
    """Load vehicles.csv with all vehicle attributes."""
    return pd.read_csv(GENERAL / "vehicles.csv")


def load_calendar() -> pd.DataFrame:
    """Load calendar.csv with date parsed."""
    return pd.read_csv(GENERAL / "calendar.csv", parse_dates=["date"])


def load_district_travel() -> pd.DataFrame:
    """Load district_travel.csv."""
    return pd.read_csv(GENERAL / "district_travel.csv")


def load_service_allowance() -> pd.DataFrame:
    """Load service_allowance.csv."""
    return pd.read_csv(GENERAL / "service_allowance.csv")


def load_traffic_speed() -> pd.DataFrame:
    """Load traffic_speed.csv."""
    return pd.read_csv(GENERAL / "traffic_speed.csv")


def load_road_conditions() -> pd.DataFrame:
    """Load road_conditions.csv with date parsed."""
    return pd.read_csv(GENERAL / "road_conditions.csv", parse_dates=["date"])


def load_deliveries_train() -> pd.DataFrame:
    """Load deliveries_train.csv with order_date parsed."""
    df = pd.read_csv(TRAIN / "deliveries_train.csv")
    df["order_date"] = pd.to_datetime(df["order_date"])
    if "dispatch_date" in df.columns:
        df["dispatch_date"] = pd.to_datetime(df["dispatch_date"], errors="coerce")
    return df


def load_route_legs_train() -> pd.DataFrame:
    """Load route_legs_train.csv with date parsed."""
    df = pd.read_csv(TRAIN / "route_legs_train.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df


def load_task1_test_inputs() -> pd.DataFrame:
    """Load task1_test_inputs.csv."""
    df = pd.read_csv(TEST / "task1_test_inputs.csv")
    df["order_date"] = pd.to_datetime(df["order_date"])
    if "dispatch_date" in df.columns:
        df["dispatch_date"] = pd.to_datetime(df["dispatch_date"], errors="coerce")
    return df


def load_route_legs_test() -> pd.DataFrame:
    """Load route_legs_test.csv."""
    df = pd.read_csv(TEST / "route_legs_test.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df


def load_submission_template(task: str) -> pd.DataFrame:
    """Load a submission template. task: 'task1', 'task2a', or 'task2b'."""
    return pd.read_csv(TEMPLATES / f"submission_{task}.csv")


# ──────────────────────────────────────────────
# Label construction
# ──────────────────────────────────────────────
def construct_labels(
    deliveries: pd.DataFrame,
    route_legs: pd.DataFrame,
    service_time_cap_min: float = 180.0,
) -> pd.DataFrame:
    """Derive service_time_min and is_late labels from training data.

    Steps:
    1. Filter to dispatched orders (route_id not null).
    2. Join deliveries to route_legs on (route_id, seq_in_route == seq).
    3. Compute service_time_min = leave_outlet_time - arrival_time.
    4. Compute is_late = arrival_time > window_close_time.

    Args:
        deliveries: deliveries_train DataFrame.
        route_legs: route_legs_train DataFrame.
        service_time_cap_min: Cap service time to this value to remove
            extreme outliers. Set to None to skip capping.

    Returns:
        DataFrame with columns from deliveries plus:
            - service_time_min (float): derived service time in minutes
            - is_late (int): 1 if arrival was after window_close_time, else 0
            - arrival_minutes (float): arrival_time in minutes from midnight
            - window_close_minutes (float): window_close_time in minutes
            - window_open_minutes (float): window_open_time in minutes
            - arrived_early (int): 1 if arrival was before window_open_time
    """
    # Only dispatched orders have route legs
    dispatched = deliveries[deliveries["route_id"].notna()].copy()

    # Select the columns we need from route_legs
    leg_cols = [
        "route_id", "seq",
        "arrival_time", "leave_outlet_time",
        "actual_depart_time", "actual_travel_duration_min",
        "distance_km", "from_point",
    ]
    legs = route_legs[leg_cols].copy()

    # Join
    merged = dispatched.merge(
        legs,
        left_on=["route_id", "seq_in_route"],
        right_on=["route_id", "seq"],
        how="inner",
    )

    # Convert times to minutes from midnight
    merged["arrival_minutes"] = hhmm_to_minutes(merged["arrival_time"])
    merged["leave_minutes"] = hhmm_to_minutes(merged["leave_outlet_time"])
    merged["window_open_minutes"] = hhmm_to_minutes(merged["window_open_time"])
    merged["window_close_minutes"] = hhmm_to_minutes(merged["window_close_time"])
    merged["planned_arrival_minutes"] = hhmm_to_minutes(merged["planned_arrival_time"])

    # --- Service Time Label ---
    merged["service_time_min"] = minutes_diff(
        merged["leave_minutes"], merged["arrival_minutes"]
    )

    # Cap extreme outliers
    if service_time_cap_min is not None:
        merged["service_time_min"] = merged["service_time_min"].clip(
            upper=service_time_cap_min
        )

    # --- Late Label ---
    merged["is_late"] = (
        merged["arrival_minutes"] > merged["window_close_minutes"]
    ).astype(int)

    # --- Early arrival flag (may include wait time in observed service_time) ---
    merged["arrived_early"] = (
        merged["arrival_minutes"] < merged["window_open_minutes"]
    ).astype(int)

    # Drop helper columns
    merged.drop(columns=["leave_minutes"], inplace=True)

    return merged


# ──────────────────────────────────────────────
# Stops-per-route aggregation
# ──────────────────────────────────────────────
def compute_stops_per_route(route_legs: pd.DataFrame) -> pd.DataFrame:
    """Count total stops on each route.

    Returns DataFrame with columns: route_id, total_stops.
    """
    return (
        route_legs.groupby("route_id")
        .size()
        .reset_index(name="total_stops")
    )


# ──────────────────────────────────────────────
# Main entrypoint for quick testing
# ──────────────────────────────────────────────
if __name__ == "__main__":
    print("Loading data...")
    deliveries = load_deliveries_train()
    route_legs = load_route_legs_train()

    print("Constructing labels...")
    labeled = construct_labels(deliveries, route_legs)

    print(f"\nLabeled dataset shape: {labeled.shape}")
    print(f"Service time stats:\n{labeled['service_time_min'].describe()}")
    print(f"\nLate rate: {labeled['is_late'].mean():.3f}")
    print(f"Early arrival rate: {labeled['arrived_early'].mean():.3f}")
    print(f"\nLate rate by brand:\n{labeled.groupby('brand')['is_late'].mean()}")
    print("\nLabel construction complete.")
