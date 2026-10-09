# Domain Rules

> Operating constraints and business logic for Waypoint Group's delivery network. These rules govern all tasks. Violating any of them produces an invalid result.

---

## Depot Topology

- **Two depots:** Peliyagoda (main distribution center) and Kandy (regional hub).
- A vehicle operates from its **assigned (home) depot only**.
- A vehicle may serve **only outlets assigned to its home depot**.
- The network serves **120 outlets** across **12 districts**.

---

## Fleet Composition

| Vehicle Type | Count | Temperature | Notes |
|---|---|---|---|
| Refrigerated trucks | 12 | reefer | Can carry chilled + ambient |
| Dry-box trucks | 40 | ambient | Cannot carry chilled |
| Refrigerated vans | 4 | reefer | Can carry chilled + ambient; can access van_only outlets |
| Ambient vans | 4 | ambient | Cannot carry chilled; can access van_only outlets |
| **Total** | **60** | — | 16 vehicles total can carry chilled goods |

---

## Vehicle Constraints

1. **Weight and volume limits:** Every load must satisfy BOTH the vehicle's weight limit (`weight_cap_kg`) and volume limit (`volume_cap_m3`).
2. **Temperature capability:**
   - `reefer` vehicles can carry both `chilled` and `ambient` goods.
   - `ambient` vehicles can carry `ambient` goods ONLY. They **cannot** carry chilled or frozen goods.
3. **Weekly fuel quota:** Each vehicle has a `weekly_fuel_quota_l`. Route distance consumes this allowance.
4. **Maximum trips per day:** A vehicle can run up to **2 routes (trips) per day**.
5. **Operating days:** Waypoint operates **Monday through Saturday** (6 days/week). Check `is_operating` in `calendar.csv`.
6. **Driver availability:** Each vehicle has a driver. Driver availability is NOT a separate constraint.

---

## Outlet Constraints

1. **Delivery windows:** Every outlet has a `window_open_time` and `window_close_time`. Deliveries must arrive within this window.
   - Fresh deliveries must generally arrive **before 8 AM**, though individual outlet windows may differ.
   - A vehicle arriving **early waits** until the window opens.
   - A **late arrival** (after `window_close_time`) is still delivered but is penalized.
2. **Van-only access:** Outlets with `parking_constraint = van_only` can **only** be served by vehicles with `type = van`. Trucks cannot access these outlets.
3. **Mall outlets:** Outlets with `parking_constraint = mall_dock` accept deliveries only within the `mall_window` (a fixed access window set by the mall).
4. **Dock types:** `rear_dock` (proper loading bay), `street` (curbside), `mall_bay` (shared mall bay). Dock type affects service/handling time.

---

## Brand-Specific Rules

### Fresh (80 outlets)
- **Delivery schedule:** Daily, before stores open at 8 AM.
- **Goods:** Groceries, chilled and frozen goods; wide product range.
- **Temperature:** Has BOTH chilled and ambient orders. Only Fresh has chilled demand.
- **Dual orders:** A Fresh outlet can have **two orders for the same delivery day** (one dry grocery, one chilled).
- **Time budget:** Fresh trips operate in the **3:30 AM - 8:00 AM** window (270 minutes total per vehicle).

### Style (25 outlets)
- **Delivery schedule:** Weekly, with seasonal peaks.
- **Goods:** Hanging garments and cartons.
- **Temperature:** Ambient only. `pred_chilled_volume_m3 = 0` always.
- **Volume characteristic:** Garments fill volume before reaching weight limit.
- **Location:** Around half of Style stores are in malls with fixed delivery windows.
- **Time budget:** Shares the daytime window with Tech (480 minutes per vehicle).

### Tech (15 outlets)
- **Delivery schedule:** As needed; demand varies day to day.
- **Goods:** Appliances and consumer electronics.
- **Temperature:** Ambient only. `pred_chilled_volume_m3 = 0` always.
- **Characteristics:** Heavy, fragile, high-value goods.
- **Time budget:** Shares the daytime window with Style (480 minutes per vehicle).

---

## Order Flow

1. Store managers place orders according to their brand's schedule.
2. **Orders for the next day close at 4 PM.** Orders after cutoff wait for the following run.
3. After cutoff, the dispatcher plans against confirmed orders, available vehicles, and constraints.
4. When demand exceeds capacity, the dispatcher decides which orders to **defer** and records the reason.

### Dispatch Statuses

| Status | Meaning |
|---|---|
| `attempted` | Dispatched on the `order_date` |
| `deferred` | Dispatched on a later date (fleet capacity was short) |
| `not_run` | Never dispatched |

> **All statuses represent real demand.** When building demand data (Task 2A), count every order regardless of dispatch status.

---

## Demand Drivers

The following factors affect demand volume and/or travel time:

| Factor | Column in `calendar.csv` | Effect |
|---|---|---|
| Paydays | `is_payday` | Demand spike |
| Festivals | `festival`, `festival_ramp` | Demand ramps up over 9 days before festival |
| Monsoon | `monsoon` | Affects travel time and road conditions |
| Weekends | `is_weekend` | Waypoint does not operate on Sundays |
| Holidays | `is_holiday` | May affect operations |
| Operating days | `is_operating` | 1 = deliveries run; 0 = no deliveries |

---

## Time Budget Summary

| Brand(s) | Operating Window | Daily Budget Per Vehicle |
|---|---|---|
| Fresh | 3:30 AM - 8:00 AM | 270 minutes |
| Style + Tech (combined) | Trading day | 480 minutes |

- These are **separate windows**. A vehicle may run 1 Fresh trip AND 1 Style/Tech trip, each checked against its own budget.
- A vehicle may still run only **2 trips total** across both windows.
