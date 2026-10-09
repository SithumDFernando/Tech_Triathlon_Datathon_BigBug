# Data Dictionary

> Single source of truth for every data file, its columns, types, and relationships.

---

## Conventions

- **Clock times** use `HH:MM` in Asia/Colombo timezone. Column names ending in `_time` contain clock times.
- **Durations** are in minutes. Column names ending in `_duration_min` contain durations.
- **Dates** use `YYYY-MM-DD` format.
- All data is synthetic and does not represent real entities.

---

## File Index

### General Data (`data/raw/General Data/`)

| File | Purpose |
|---|---|
| `outlets.csv` | 120 outlets — brand, district, depot, access restrictions, delivery windows |
| `vehicles.csv` | 60 vehicles — type, temperature capability, capacity, fuel profile, depot |
| `calendar.csv` | Calendar context — dates, paydays, festivals, monsoon, operating flags |
| `district_travel.csv` | District travel distances and free-flow times from each depot |
| `service_allowance.csv` | Handling-time allowance per brand and dock type |
| `traffic_speed.csv` | Typical congestion by district and hour |
| `road_conditions.csv` | Date-specific district disruptions (roadworks, flooding, incidents) |

### Training Data (`data/raw/Training Data/`)

| File | Purpose |
|---|---|
| `deliveries_train.csv` | Historical orders — one row per order (`delivery_id`), includes dispatched and deferred/not_run |
| `route_legs_train.csv` | Historical route legs — one row per leg, includes planned AND actual times |

### Test Data (`data/raw/Test Data/`)

| File | Purpose |
|---|---|
| `task1_test_inputs.csv` | Task 1 orders for prediction — same schema as deliveries_train (all dispatched) |
| `route_legs_test.csv` | Route legs for Task 1 orders — planned times only, no actuals |
| `task2a_test_inputs.csv` | Task 2A forecast grid — one row per depot x brand x forecast week |
| `task2b_peak_day_scenarios.csv` | Task 2B orders — one row per order in the peak-day scenario |
| `task2b_peak_day_fleet.csv` | Task 2B fleet — vehicle availability for the scenario day |

### Submission Templates (`data/raw/Submission Templates/`)

| File | Task |
|---|---|
| `submission_task1.csv` | Service time and lateness predictions |
| `submission_task2a.csv` | Weekly depot demand forecasts |
| `submission_task2b.csv` | Peak-day allocation |

---

## Column Schemas

### `deliveries_train.csv` / `task1_test_inputs.csv`

One row per order.

| Column | Type | Format | Meaning |
|---|---|---|---|
| `delivery_id` | string | — | Unique order identifier; Task 1 prediction key |
| `order_date` | date | YYYY-MM-DD | The date the store's order was for |
| `dispatch_date` | date | YYYY-MM-DD | Date dispatched; blank if never ran |
| `dispatch_status` | string | — | `attempted` (dispatched on order_date), `deferred` (dispatched later), `not_run` (never dispatched) |
| `outlet_id` | string | — | Outlet identifier |
| `brand` | string | — | Fresh, Style, or Tech |
| `district` | string | — | One of 12 districts |
| `depot` | string | — | Peliyagoda or Kandy |
| `temp_requirement` | string | — | `chilled` (needs reefer) or `ambient` |
| `order_units` | integer | — | Number of items or cases |
| `order_weight_kg` | number | — | Weight in kilograms |
| `order_volume_m3` | number | — | Volume in cubic meters |
| `route_id` | string | — | Route carrying the order; blank if never ran |
| `seq_in_route` | integer | — | Position on route (0-indexed); with `route_id` identifies the matching route leg |
| `vehicle_id` | string | — | Assigned vehicle |
| `vehicle_type` | string | — | Vehicle type |
| `vehicle_temp` | string | — | Vehicle temperature capability |
| `planned_arrival_time` | HH:MM | — | Planned arrival at outlet |
| `window_open_time` | HH:MM | — | Start of delivery window |
| `window_close_time` | HH:MM | — | End of delivery window |

### `route_legs_train.csv` / `route_legs_test.csv`

One row per route leg.

| Column | Type | Format | Meaning |
|---|---|---|---|
| `leg_id` | string | — | Unique leg identifier |
| `date` | date | YYYY-MM-DD | Date the route ran |
| `route_id` | string | — | Route identifier |
| `seq` | integer | — | Position on route (0-indexed) |
| `depot` | string | — | Depot |
| `vehicle_id` | string | — | Vehicle identifier |
| `vehicle_type` | string | — | truck or van |
| `vehicle_temp` | string | — | reefer or ambient |
| `brand` | string | — | Fresh, Style, or Tech |
| `district` | string | — | District |
| `from_point` | string | — | `DEPOT` for first leg; otherwise previous outlet |
| `to_outlet` | string | — | Outlet served by this leg |
| `distance_km` | number | — | Road distance in km |
| `planned_depart_time` | HH:MM | — | Planned departure from previous point |
| `planned_travel_duration_min` | integer | minutes | Planned travel duration |
| `planned_arrival_time` | HH:MM | — | Planned arrival at outlet |
| `actual_depart_time` | HH:MM | — | **Training only.** Actual departure |
| `actual_travel_duration_min` | integer | minutes | **Training only.** Actual travel duration |
| `arrival_time` | HH:MM | — | **Training only.** Actual arrival at outlet |
| `leave_outlet_time` | HH:MM | — | **Training only.** Time vehicle left after delivery |
| `monsoon` | 0/1 | — | 1 in monsoon/inter-monsoon month |
| `dow` | 0-6 | — | Day of week (0 = Monday) |

### `outlets.csv`

| Column | Type | Meaning |
|---|---|---|
| `outlet_id` | string | OUT001 through OUT120 |
| `brand` | string | Fresh, Style, or Tech |
| `district` | string | One of 12 districts |
| `depot` | string | Peliyagoda or Kandy |
| `dock_type` | string | `rear_dock`, `street`, or `mall_bay` |
| `parking_constraint` | string | `normal` (any vehicle), `van_only` (no trucks), `mall_dock` (mall delivery window) |
| `mall_window` | HH:MM-HH:MM | Mall delivery window; blank for non-mall outlets |
| `window_open_time` | HH:MM | Start of delivery window |
| `window_close_time` | HH:MM | End of delivery window |

### `vehicles.csv`

| Column | Type | Meaning |
|---|---|---|
| `vehicle_id` | string | VEH001 through VEH060 |
| `type` | string | `truck` or `van` |
| `temp` | string | `reefer` (can carry chilled + ambient) or `ambient` (ambient only) |
| `weight_cap_kg` | number | Max weight per trip (kg) |
| `volume_cap_m3` | number | Max volume per trip (m3) |
| `fuel_type` | string | Fuel type |
| `km_per_l` | number | Fuel efficiency |
| `weekly_fuel_quota_l` | number | Weekly fuel quota in liters |
| `depot` | string | Home depot — vehicle serves only this depot's outlets |

### `calendar.csv`

| Column | Type | Meaning |
|---|---|---|
| `date` | date | One row per calendar date |
| `dow` | 0-6 | Day of week (0 = Monday) |
| `dow_name` | string | Day name |
| `is_weekend` | 0/1 | Weekend flag |
| `iso_year` | integer | ISO year (for grouping demand) |
| `iso_week` | integer | ISO week (for grouping demand) |
| `is_payday` | 0/1 | 1 on payday |
| `festival` | string | Festival name on festival date; blank otherwise |
| `festival_ramp` | 0-1 | Proximity to festival; rises over 9 preceding days; 1 on festival date |
| `is_holiday` | 0/1 | 1 on festival/public holiday |
| `monsoon` | 0/1 | 1 in monsoon/inter-monsoon month |
| `is_operating` | 0/1 | 1 when deliveries operate |

### `district_travel.csv`

| Column | Type | Meaning |
|---|---|---|
| `district` | string | District name |
| `depot` | string | Serving depot |
| `road_class` | string | `urban`, `suburban`, `highway`, or `hill` |
| `free_flow_kmh` | number | Clear-road speed (km/h) |
| `depot_to_district_km` | number | Distance from depot to district (km) |
| `depot_to_district_freeflow_min` | integer | Clear-road travel time depot to district (min) |
| `inter_stop_km` | number | Typical distance between outlets within district (km) |
| `inter_stop_freeflow_min` | integer | Typical inter-stop travel time (min) |

### `service_allowance.csv`

| Column | Type | Meaning |
|---|---|---|
| `brand` | string | Fresh, Style, or Tech |
| `dock_type` | string | rear_dock, street, or mall_bay |
| `service_allowance_min` | integer | Handling time per stop (minutes) — planning allowance, not observed |

### `traffic_speed.csv`

| Column | Type | Meaning |
|---|---|---|
| `monsoon` | 0/1 | Monsoon flag |
| `speed_index` | number | Speed relative to clear roads; 100 = free-flow, lower = slower |

### `road_conditions.csv`

| Column | Type | Meaning |
|---|---|---|
| `disruption_index` | number | Date-specific disruption; 100 = clear, lower = disrupted (roadworks/flooding/incidents) |

### `task2a_test_inputs.csv`

| Column | Type | Meaning |
|---|---|---|
| `row_id` | string | Unique identifier for the forecast row |
| `depot` | string | Peliyagoda or Kandy |
| `brand` | string | Fresh, Style, or Tech |
| `iso_year` | integer | ISO year of forecast week |
| `iso_week` | integer | ISO week of forecast week |

### `task2b_peak_day_scenarios.csv`

| Column | Type | Meaning |
|---|---|---|
| `scenario` | string | Always S1 |
| `order_ref` | string | Unique order identifier (allocation key) |
| `outlet_id` | string | Outlet identifier |
| `brand` | string | Fresh, Style, or Tech |
| `district` | string | District |
| `depot` | string | Always Peliyagoda for S1 |
| `dock_type` | string | rear_dock, street, or mall_bay |
| `parking_constraint` | string | normal, van_only, or mall_dock |
| `mall_window` | HH:MM-HH:MM | Mall window if applicable |
| `window_open_time` | HH:MM | Delivery window start |
| `window_close_time` | HH:MM | Delivery window end |
| `temp_requirement` | string | chilled or ambient |
| `order_units` | integer | Number of items |
| `order_weight_kg` | number | Weight (kg) |
| `order_volume_m3` | number | Volume (m3) |
| `deferred_yesterday` | 0/1 | 1 if outlet was skipped on previous run |
| `days_since_last_served` | integer | Days since last delivery to this outlet |

### `task2b_peak_day_fleet.csv`

| Column | Type | Meaning |
|---|---|---|
| `scenario` | string | Always S1 |
| `vehicle_id` | string | Vehicle identifier |
| `status` | string | `available` or `in_workshop` |

---

## Key Join Rules

1. **Deliveries to Route Legs:** Join on `route_id` AND `seq_in_route` (deliveries) = `seq` (route_legs)
2. **Deliveries to Outlets:** Join on `outlet_id`
3. **Route Legs to Vehicles:** Join on `vehicle_id`
4. **Route Legs to Calendar:** Join on `date`
5. **Route Legs to District Travel:** Join on `district` (and `depot`)
6. **Outlets to Service Allowance:** Join on `brand` + `dock_type`
7. **Outlets to District Travel:** Join on `district` (and `depot`)

---

## Entity Relationship Summary

```
DELIVERIES ──(route_id + seq_in_route)──> ROUTE_LEGS
DELIVERIES ──(outlet_id)──────────────> OUTLETS
ROUTE_LEGS ──(vehicle_id)─────────────> VEHICLES
ROUTE_LEGS ──(date)────────────────────> CALENDAR
ROUTE_LEGS ──(district)────────────────> DISTRICT_TRAVEL
OUTLETS ───(brand + dock_type)────────> SERVICE_ALLOWANCE
OUTLETS ───(district)──────────────────> DISTRICT_TRAVEL
```
