"""
Feature engineering for Task 1: Service Time and Lateness Prediction.

Builds a feature matrix from merged delivery + route leg data,
enriched with outlet, vehicle, calendar, traffic, and road condition data.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from src.preprocessing import (
    load_outlets,
    load_vehicles,
    load_calendar,
    load_district_travel,
    load_service_allowance,
    load_traffic_speed,
    load_road_conditions,
    hhmm_to_minutes,
    compute_stops_per_route,
)


# ──────────────────────────────────────────────
# Feature builders
# ──────────────────────────────────────────────
def add_calendar_features(df: pd.DataFrame, calendar: pd.DataFrame) -> pd.DataFrame:
    """Merge calendar context (festivals, paydays, monsoon) onto the data.

    Joins on order_date == calendar.date.
    """
    cal_cols = [
        "date", "dow", "is_weekend", "iso_year", "iso_week",
        "is_payday", "festival_ramp", "is_holiday", "monsoon", "is_operating",
    ]
    merged = df.merge(
        calendar[cal_cols],
        left_on="order_date",
        right_on="date",
        how="left",
        suffixes=("", "_cal"),
    )
    # Drop duplicate date column from calendar
    if "date" in merged.columns and "order_date" in merged.columns:
        merged.drop(columns=["date"], inplace=True, errors="ignore")
    return merged


def add_district_travel_features(
    df: pd.DataFrame, district_travel: pd.DataFrame
) -> pd.DataFrame:
    """Merge district travel info (distances, road class, free-flow times)."""
    dt_cols = [
        "district", "depot", "road_class", "free_flow_kmh",
        "depot_to_district_km", "depot_to_district_freeflow_min",
        "inter_stop_km", "inter_stop_freeflow_min",
    ]
    return df.merge(
        district_travel[dt_cols],
        on=["district", "depot"],
        how="left",
    )


def add_service_allowance_features(
    df: pd.DataFrame, service_allowance: pd.DataFrame, outlets: pd.DataFrame
) -> pd.DataFrame:
    """Add the planned service allowance for each delivery's brand + dock_type."""
    # Get dock_type from outlets
    if "dock_type" not in df.columns:
        df = df.merge(
            outlets[["outlet_id", "dock_type", "parking_constraint"]],
            on="outlet_id",
            how="left",
        )
    return df.merge(service_allowance, on=["brand", "dock_type"], how="left")


def add_traffic_speed_features(
    df: pd.DataFrame, traffic_speed: pd.DataFrame
) -> pd.DataFrame:
    """Merge traffic speed index based on district, hour, and monsoon.

    Uses the planned arrival hour to determine the relevant speed index.
    """
    # Extract hour from planned_arrival_time
    if "planned_arrival_hour" not in df.columns:
        df["planned_arrival_hour"] = (
            hhmm_to_minutes(df["planned_arrival_time"]) // 60
        ).astype("Int64")

    # Use monsoon from the calendar (already joined), or from route legs
    monsoon_col = "monsoon"
    if monsoon_col not in df.columns:
        monsoon_col = "monsoon_cal"

    merged = df.merge(
        traffic_speed,
        left_on=["district", "planned_arrival_hour", monsoon_col],
        right_on=["district", "hour", "monsoon"],
        how="left",
        suffixes=("", "_traffic"),
    )
    # Drop duplicate columns
    for col in ["hour", "monsoon_traffic"]:
        if col in merged.columns:
            merged.drop(columns=[col], inplace=True, errors="ignore")
    return merged


def add_road_condition_features(
    df: pd.DataFrame, road_conditions: pd.DataFrame
) -> pd.DataFrame:
    """Merge road disruption_index based on district and date."""
    return df.merge(
        road_conditions,
        left_on=["district", "order_date"],
        right_on=["district", "date"],
        how="left",
        suffixes=("", "_road"),
    )


def add_route_features(
    df: pd.DataFrame, route_legs: pd.DataFrame
) -> pd.DataFrame:
    """Add route-level features: total stops, position ratio."""
    stops = compute_stops_per_route(route_legs)
    df = df.merge(stops, on="route_id", how="left")

    # Position ratio: how far along the route is this stop? (0 = first, 1 = last)
    df["route_position_ratio"] = df["seq_in_route"] / df["total_stops"].clip(lower=1)

    return df


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived time-based features."""
    # Planned arrival in minutes from midnight
    if "planned_arrival_minutes" not in df.columns:
        df["planned_arrival_minutes"] = hhmm_to_minutes(df["planned_arrival_time"])

    # Window duration
    if "window_open_minutes" not in df.columns:
        df["window_open_minutes"] = hhmm_to_minutes(df["window_open_time"])
    if "window_close_minutes" not in df.columns:
        df["window_close_minutes"] = hhmm_to_minutes(df["window_close_time"])

    df["window_duration_min"] = df["window_close_minutes"] - df["window_open_minutes"]

    # Buffer: how much slack between planned arrival and window close
    df["planned_slack_min"] = (
        df["window_close_minutes"] - df["planned_arrival_minutes"]
    )

    # How early/late is the planned arrival relative to window open
    df["planned_vs_window_open_min"] = (
        df["planned_arrival_minutes"] - df["window_open_minutes"]
    )

    return df


def add_order_density_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add aggregated features about order density and load."""
    # Orders per route (how loaded is the vehicle)
    route_load = (
        df.groupby("route_id")
        .agg(
            route_total_weight=("order_weight_kg", "sum"),
            route_total_volume=("order_volume_m3", "sum"),
            route_total_units=("order_units", "sum"),
        )
        .reset_index()
    )
    df = df.merge(route_load, on="route_id", how="left")
    return df


# ──────────────────────────────────────────────
# Main pipeline
# ──────────────────────────────────────────────
def build_features(
    df: pd.DataFrame,
    route_legs: pd.DataFrame,
    is_train: bool = True,
) -> pd.DataFrame:
    """Full feature engineering pipeline for Task 1.

    Args:
        df: Merged deliveries + route_legs DataFrame (from construct_labels
            for training, or merged test data).
        route_legs: Full route_legs DataFrame (train or test).
        is_train: If True, assumes labels are present.

    Returns:
        DataFrame with all engineered features added.
    """
    # Load reference data
    outlets = load_outlets()
    calendar = load_calendar()
    district_travel = load_district_travel()
    service_allowance = load_service_allowance()
    traffic_speed = load_traffic_speed()
    road_conditions = load_road_conditions()

    # Add features step by step
    df = add_calendar_features(df, calendar)
    df = add_district_travel_features(df, district_travel)
    df = add_service_allowance_features(df, service_allowance, outlets)
    df = add_time_features(df)
    df = add_route_features(df, route_legs)
    df = add_order_density_features(df)
    df = add_traffic_speed_features(df, traffic_speed)
    df = add_road_condition_features(df, road_conditions)

    return df


def get_feature_columns() -> list[str]:
    """Return the list of feature columns to use for modeling.

    This is the single source of truth for which columns feed into the model.
    """
    return [
        # Order characteristics
        "order_units",
        "order_weight_kg",
        "order_volume_m3",
        # Temporal
        "dow",
        "is_payday",
        "festival_ramp",
        "is_holiday",
        "monsoon",
        # Timing
        "planned_arrival_minutes",
        "planned_arrival_hour",
        "window_duration_min",
        "planned_slack_min",
        "planned_vs_window_open_min",
        # Route
        "seq_in_route",
        "total_stops",
        "route_position_ratio",
        "distance_km",
        # Route load
        "route_total_weight",
        "route_total_volume",
        "route_total_units",
        # District travel
        "depot_to_district_km",
        "depot_to_district_freeflow_min",
        "inter_stop_km",
        "inter_stop_freeflow_min",
        # Service allowance (planned baseline)
        "service_allowance_min",
        # Traffic and road
        "speed_index",
        "disruption_index",
    ]


def get_categorical_columns() -> list[str]:
    """Return the categorical columns to encode for the model."""
    return [
        "brand",
        "district",
        "depot",
        "vehicle_type",
        "vehicle_temp",
        "temp_requirement",
        "dock_type",
        "parking_constraint",
        "road_class",
        "dispatch_status",
    ]


# ──────────────────────────────────────────────
# Quick test
# ──────────────────────────────────────────────
if __name__ == "__main__":
    from src.preprocessing import (
        load_deliveries_train,
        load_route_legs_train,
        construct_labels,
    )

    print("Loading data...")
    deliveries = load_deliveries_train()
    route_legs = load_route_legs_train()

    print("Constructing labels...")
    labeled = construct_labels(deliveries, route_legs)

    print("Building features...")
    featured = build_features(labeled, route_legs, is_train=True)

    print(f"\nFeatured dataset shape: {featured.shape}")
    print(f"Columns: {list(featured.columns)}")

    # Check feature availability
    feature_cols = get_feature_columns()
    cat_cols = get_categorical_columns()
    missing = [c for c in feature_cols + cat_cols if c not in featured.columns]
    if missing:
        print(f"\n⚠️  Missing columns: {missing}")
    else:
        print(f"\n✅ All {len(feature_cols)} numeric + {len(cat_cols)} categorical features present.")

    print("\nFeature engineering complete.")
