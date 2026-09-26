# Task 1: Predict Service Time and Lateness

> Predict two values for each planned delivery in the test set.

---

## Objective

For each `delivery_id` in the test inputs, predict:

| Target | Column | Type | Description |
|---|---|---|---|
| Service time | `pred_service_min` | number (minutes) | Predicted handling/unloading time at the outlet |
| Late probability | `pred_late_prob` | number (0 to 1) | Probability that the delivery arrives AFTER the outlet's delivery window closes |

---

## Label Construction (Critical)

> **Labels are NOT provided in the data.** You must derive them from training data. Correct label construction is explicitly part of the assessment (20% of judging weight is "Data wrangling and label construction").

### Service Time Label

Derive from training route legs:

```
service_time_min = leave_outlet_time - arrival_time
```

- `arrival_time` = actual arrival at the outlet (from `route_legs_train.csv`)
- `leave_outlet_time` = when the vehicle left after completing delivery (from `route_legs_train.csv`)
- Both are `HH:MM` clock times. Handle midnight crossings if applicable.

### Late Label

Derive by comparing actual arrival to the outlet's delivery window:

```
is_late = 1 if arrival_time > window_close_time, else 0
```

- `arrival_time` = actual arrival (from `route_legs_train.csv`)
- `window_close_time` = end of outlet's delivery window (from deliveries or outlets)
- A delivery arriving AFTER the window closes is "late".

### Important Nuances

- **Early arrivals wait.** A vehicle that arrives before `window_open_time` waits until the window opens. This may affect the observed service time — the time between arrival and leaving may include wait time.
- **Late arrivals are still delivered.** A late delivery is completed but receiving staff may have moved to other duties (longer handling). Lateness refers specifically to arrival after `window_close_time`.
- **Actual times exist only in training data.** Test route legs have planned times only (no `actual_depart_time`, `actual_travel_duration_min`, `arrival_time`, `leave_outlet_time`).

---

## Input Files

| File | Location | Use |
|---|---|---|
| `deliveries_train.csv` | `data/raw/Training Data/` | Training orders — derive labels by joining to route legs |
| `route_legs_train.csv` | `data/raw/Training Data/` | Training route legs — contains actual times for label derivation |
| `task1_test_inputs.csv` | `data/raw/Test Data/` | Test orders to predict on |
| `route_legs_test.csv` | `data/raw/Test Data/` | Test route legs — planned times only |
| `outlets.csv` | `data/raw/General Data/` | Outlet attributes (dock_type, windows, etc.) |
| `vehicles.csv` | `data/raw/General Data/` | Vehicle attributes |
| `calendar.csv` | `data/raw/General Data/` | Date context (monsoon, payday, festival, etc.) |
| `district_travel.csv` | `data/raw/General Data/` | Travel distances and times |
| `service_allowance.csv` | `data/raw/General Data/` | Planning allowances per brand + dock_type |
| `traffic_speed.csv` | `data/raw/General Data/` | Congestion index |
| `road_conditions.csv` | `data/raw/General Data/` | Date-specific disruptions |

---

## Joining Deliveries to Route Legs

Each dispatched order (`delivery_id`) maps to exactly one route leg:

```
deliveries.route_id = route_legs.route_id
AND
deliveries.seq_in_route = route_legs.seq
```

---

## Feature Considerations

The challenge does NOT prescribe a feature set — choose and justify your own. Consider:

- **Planned timing:** `planned_depart_time`, `planned_travel_duration_min`, `planned_arrival_time`
- **Temporal context:** `monsoon`, `dow` (day of week), festival proximity (`festival_ramp`), payday
- **Route characteristics:** `distance_km`, position in route (`seq`), number of stops
- **Vehicle attributes:** `vehicle_type` (truck/van), `vehicle_temp` (reefer/ambient)
- **Outlet attributes:** `brand`, `dock_type`, `parking_constraint`, `district`
- **Traffic and road conditions:** `speed_index` from traffic_speed, `disruption_index` from road_conditions
- **Order size:** `order_units`, `order_weight_kg`, `order_volume_m3`
- **Window characteristics:** window duration, relationship between planned arrival and window

---

## Output Format

Complete `data/raw/Submission Templates/submission_task1.csv`:

| Column | Requirement |
|---|---|
| `delivery_id` | Keep unchanged — exact values from the template |
| `pred_service_min` | Fill with predicted handling time in minutes |
| `pred_late_prob` | Fill with probability (0 to 1) of late arrival |

### Rules
- **Do not add or remove rows.**
- **Keep the exact row order as supplied.**
- Fill only the two prediction columns.

---

## Model Restrictions

- No pretrained models (except for synthetic data generation or preprocessing).
- No proprietary API-based modelling/preprocessing.
- No low-code/no-code AI tools or automated end-to-end modelling tools.
