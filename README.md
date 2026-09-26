# Tech Triathlon 2026 — Datathon | Team BigBug

This repository contains data, documentation, evaluation scripts, and solutions for the **Tech Triathlon 2026 Datathon** challenge (Waypoint Group logistics optimization).

**Team:** BigBug

---

## 📋 Overview of Tasks

The competition consists of three primary data science and optimization tasks:

| Task | Objective | Target Outputs |
| :--- | :--- | :--- |
| **Task 1: Service Time & Lateness** | Predict handling duration and probability of missing delivery windows for planned delivery orders. | `pred_service_min`, `pred_late_prob` |
| **Task 2A: Depot Demand Forecasting** | Forecast 10-week future demand across depots and brands. | `pred_total_volume_m3`, `pred_chilled_volume_m3` |
| **Task 2B: Peak-Day Fleet Allocation** | Optimally allocate orders to available vehicles and trips during peak festival demand (Scenario S1). | `decision`, `vehicle_id`, `trip_id` |

---

## 📁 Repository Structure

```text
├── AGENTS.md                    # AI agent entry point — links all specs
├── check_allocation.py          # Feasibility validator for Task 2B submissions
├── data/
│   ├── General Data/            # Calendars, vehicle specs, district travel times, service allowances
│   ├── Submission Templates/    # Templates for submission_task1.csv, task2a.csv, task2b.csv
│   ├── Test Data/               # Test inputs for Task 1, Task 2A, and Task 2B
│   └── Training Data/           # Historical delivery and route leg records
└── docs/
    ├── reference/               # Original challenge documents (scenario.md, datathon.md)
    └── specs/                   # Agent-facing spec files (rules, constraints, task details)
```

---

## ⚙️ `check_allocation.py` — Task 2B Validator

`check_allocation.py` is an official validation script designed to verify that your Task 2B allocation plan satisfies all business and operational constraints before submission.

### Constraints Checked:
1. **Schema & Completeness:** All scenario orders accounted for, valid decisions (`served` or `deferred`), no duplicates.
2. **Fleet Availability:** Only vehicles marked as `available` in `task2b_peak_day_fleet.csv` are used (skips vehicles in the workshop).
3. **Depot Match:** Vehicle home depot must match the order's depot.
4. **Trip Segregation:** A single trip can serve only one brand and one district.
5. **Vehicle Capabilities:**
   - **Refrigeration:** Orders requiring `chilled` conditions must be on a `reefer` vehicle.
   - **Access / Parking:** Outlets marked as `van_only` must receive a `van` (not a truck).
6. **Physical Capacity:** Total volume ($m^3$) and weight ($kg$) per trip cannot exceed vehicle capacity.
7. **Trip Budgets & Shift Limits:**
   - At most 2 trips per vehicle per day.
   - Fresh pre-dawn trips $\le$ 270 minutes (03:30–08:00 window).
   - Daytime trips $\le$ 480 minutes (8-hour shift window).

### Running the Validator

Run the script by passing your Task 2B submission CSV:

```bash
python check_allocation.py "data/Submission Templates/submission_task2b.csv"
```

If valid, it outputs:
```text
FEASIBILITY: PASSED - every rule satisfied.
```
Otherwise, it reports detailed violation messages to help you adjust your allocation strategy.
