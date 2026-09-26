# Task 2B: Peak-Day Fleet Allocation

> Allocate orders to vehicles and trips on a day when demand exceeds fleet capacity.

---

## Objective

For every order in the peak-day scenario:
1. Mark it as **"served"** or **"deferred"**.
2. For served orders, assign a `vehicle_id` and `trip_id` (1 or 2).
3. Write a **prioritization policy** (~1 page) explaining your decisions.

> This is **NOT a machine learning task.** It is a constraint satisfaction / optimization problem. There is no single correct allocation — judges assess feasibility and reasoning.

---

## Scenario S1

| Property | Value |
|---|---|
| Depot | Peliyagoda |
| Conditions | Festival one week away; Fresh demand rising (dairy, meat, produce) |
| Payday | No |
| Monsoon | No |
| Fleet | Several vehicles are in the workshop (unavailable) |

---

## Feasibility Rules

**ALL rules must be satisfied. Violations = infeasible allocation.**

### Rule 1: Brand and District Segregation
All orders sharing a `vehicle_id` AND `trip_id` must belong to the **same brand** and **same district**.

### Rule 2: Refrigeration
- Orders with `temp_requirement = chilled` require a vehicle with `temp = reefer`.
- Reefer vehicles MAY also carry `ambient` orders.
- Ambient vehicles CANNOT carry chilled orders.

### Rule 3: Vehicle Access
- Outlets with `parking_constraint = van_only` require a vehicle with `type = van`.
- Trucks cannot serve van_only outlets.

### Rule 4: Home Depot
A vehicle may serve only outlets assigned to **its own depot**. For S1, all orders are Peliyagoda — use only Peliyagoda-depot vehicles.

### Rule 5: Whole Orders
Each served order must be assigned to **one vehicle and one trip**. Do not split an order across trips or vehicles.

### Rule 6: Capacity Limits
For each trip (group of orders sharing `vehicle_id` + `trip_id`):
- Total `order_volume_m3` must not exceed the vehicle's `volume_cap_m3`.
- Total `order_weight_kg` must not exceed the vehicle's `weight_cap_kg`.

### Rule 7: Trip Limit
Each vehicle may run **at most 2 trips total** in one day.

---

## Trip Time Calculation

Each trip leaves the depot, travels to one district, and delivers its orders there.

### Formula

```
trip_minutes = outbound_travel + inter_stop_travel + total_handling
```

Where:
- **Outbound travel** = `depot_to_district_freeflow_min` from `district_travel.csv` (counted ONCE per trip)
- **Inter-stop travel** = `inter_stop_freeflow_min` × (number_of_orders - 1)
  - A trip with 3 orders has 2 inter-stop journeys
  - A trip with 1 order has 0 inter-stop journeys
- **Total handling** = sum of `service_allowance_min` for each order, looked up from `service_allowance.csv` using the trip's `brand` + the outlet's `dock_type`

> **Do NOT add return journey to the depot** — the stated time budgets already account for it.

### Worked Example

A Fresh trip to Gampaha with 3 orders (2 rear_dock, 1 street):

| Component | Calculation | Minutes |
|---|---|---|
| Depot to Gampaha | `depot_to_district_freeflow_min` = 37 | 37 |
| Travel between 3 stops | 9 × (3 - 1) = 18 | 18 |
| Handle stop 1 | Fresh + rear_dock | 15 |
| Handle stop 2 | Fresh + rear_dock | 15 |
| Handle stop 3 | Fresh + street | 16 |
| **Trip total** | 37 + 18 + 15 + 15 + 16 | **101** |

---

## Daily Time Budgets

| Brand(s) | Operating Window | Budget Per Vehicle |
|---|---|---|
| Fresh | 3:30 AM - 8:00 AM | **270 minutes** |
| Style + Tech (combined) | Trading day | **480 minutes** |

### Budget Rules

- Fresh budget applies to the **total time of all Fresh trips** for that vehicle.
- Style/Tech budget applies to the **combined time of all Style and Tech trips** for that vehicle.
- These are **separate windows** — a vehicle may run 1 Fresh trip + 1 Style/Tech trip, checked against their respective budgets.
- A vehicle may still run only **2 trips total** (across both windows).

### Example

- Trip 1 (Fresh, Gampaha): 101 minutes
- Trip 2 (Fresh, Colombo, 4 street-access stops): 24 + (3 × 8) + (4 × 16) = 112 minutes
- Combined Fresh time: 101 + 112 = 213 of 270 minutes ✓
- But: a 3rd trip is NOT allowed (max 2 trips total).

---

## Input Files

| File | Location | Use |
|---|---|---|
| `task2b_peak_day_scenarios.csv` | `data/Test Data/` | All orders in the scenario |
| `task2b_peak_day_fleet.csv` | `data/Test Data/` | Vehicle availability |
| `vehicles.csv` | `data/General Data/` | Vehicle capacity, type, temp, depot |
| `district_travel.csv` | `data/General Data/` | Travel times for trip calculation |
| `service_allowance.csv` | `data/General Data/` | Handling times for trip calculation |

### Fleet Availability

- Only vehicles with `status = available` in `task2b_peak_day_fleet.csv` can be allocated.
- Vehicles with `status = in_workshop` **cannot be used**.
- Cross-reference with `vehicles.csv` for capacity and capability details.

---

## Output Format

Complete `data/Submission Templates/submission_task2b.csv`:

| Column | Requirement |
|---|---|
| `scenario` | Keep unchanged (always S1) |
| `order_ref` | Keep unchanged — this is the allocation key |
| `outlet_id` | Keep unchanged — included for readability |
| `decision` | `"served"` or `"deferred"` for every order |
| `vehicle_id` | Assigned vehicle for served orders; **leave blank** for deferred |
| `trip_id` | `1` or `2` for served orders; **leave blank** for deferred |

### Rules
- Replace every placeholder in the template.
- Keep all supplied identifiers and rows unchanged.
- For deferred orders, leave `vehicle_id` and `trip_id` blank.

---

## Prioritization Policy (Written Deliverable)

Submit a write-up of approximately one page or less that includes:
- The calculations behind your allocation
- Why you deferred specific orders
- What limited service on this day (the bottleneck)
- Which deferrals were unavoidable vs. your choice
- What the deferrals cost (impact on outlets)

Consider using `deferred_yesterday` and `days_since_last_served` columns to prioritize outlets that have been underserved.

---

## Validation

Run `check_allocation.py` before submitting:

```bash
python check_allocation.py "data/Submission Templates/submission_task2b.csv"
```

A passing result confirms feasibility (all rules satisfied), NOT optimality. Judges separately assess prioritization reasoning.
