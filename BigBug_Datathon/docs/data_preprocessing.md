# Data Preprocessing & Modeling Document

## 1. Data Preparation Approach
Our approach centers on establishing a single source of truth for both Task 1 (prediction) and Task 2A (forecasting) by merging all transactional, contextual, and geographic data into cohesive modeling datasets. We used modular Python scripts (`src/preprocessing.py`, `src/features_task1.py`, `src/features_task2a.py`) to handle loading, transformation, and label construction cleanly.

## 2. Label Construction Methodology
For Task 1, we constructed two critical labels from the raw `route_legs_train.csv` and `deliveries_train.csv` files:
- **`service_time_min`**: Calculated as `leave_outlet_time - arrival_time`. We observed that early arrivals often inflate this number due to vehicles waiting for the `window_open_time`. However, to reflect the actual delivery operations, we allowed the model to learn this wait-time implicitly rather than subtracting it. We capped extreme outliers at 180 minutes to stabilize training.
- **`is_late`**: Created as a binary indicator, set to `1` if `arrival_time` > `window_close_time`, otherwise `0`.

## 3. Data Cleaning Steps
- Parsed all date strings to datetime objects for temporal joins.
- Converted `HH:MM` strings into `minutes_from_midnight` (integers) to allow numerical calculations for time windows.
- Managed missing values gracefully (e.g., `dispatch_date` is blank for never-run orders) by filling or creating boolean flags.
- Checked for and handled cross-midnight route scenarios using modulo-24 logic in time differences.

## 4. Feature Engineering and Rationale
### Task 1 (Service Time & Lateness)
We engineered 37 features, categorized into:
- **Order Characteristics**: `order_units`, `order_weight_kg`, `order_volume_m3`.
- **Temporal Context**: `dow`, `is_payday`, `festival_ramp`, `is_holiday`, `monsoon` to capture congestion and demand spikes.
- **Route & Topology**: `seq_in_route`, `total_stops`, `distance_km`, `depot_to_district_freeflow_min` to understand the leg context.
- **Constraints**: `window_duration_min`, `planned_slack_min` to capture how tight the delivery window was compared to planned arrival.
- **Categoricals**: `brand`, `district`, `vehicle_type`, `dock_type` encoded as integers for LightGBM.

### Task 2A (Demand Forecasting)
- **Data Pooling**: We combined `deliveries_train.csv` and `task1_test_inputs.csv` to capture every historical order.
- **Aggregation**: Grouped by `depot`, `brand`, `iso_year`, and `iso_week` to sum volumes. Chilled volume was exclusively extracted from the 'Fresh' brand where `temp_requirement == chilled`.
- **Lag Features**: Added 1-week, 2-week, 3-week, and 4-week lags, plus a rolling 4-week mean to capture momentum.
- **Calendar Alignment**: Joined weekly aggregated calendar features (paydays per week, holidays per week, monsoon days) to account for weekly structural changes.
