# Project Overview

> Tech Triathlon 2026 — Datathon Phase | Waypoint Group Logistics

---

## What This Project Is

This is the **Datathon phase** of Tech Triathlon 2026 (organized by Rootcode). The competition follows one business challenge — designing and building a delivery planning system for **Waypoint Group** — across three phases (Designathon, Hackathon, Datathon). This repo covers only the Datathon.

Waypoint Group (Pvt) Ltd is a **fictional** Sri Lankan retail group with three brands sharing one distribution network. All competition data is synthetic.

---

## The Three Tasks

| Task | Type | Objective | Output Columns |
|---|---|---|---|
| **Task 1** | ML Prediction | Predict service time (minutes) and probability of late arrival for each planned delivery | `pred_service_min`, `pred_late_prob` |
| **Task 2A** | Time-Series Forecasting | Forecast weekly depot demand (total and chilled volume) for 10 future weeks | `pred_total_volume_m3`, `pred_chilled_volume_m3` |
| **Task 2B** | Constraint Optimization | Allocate orders to vehicles/trips on a peak day; defer what cannot fit | `decision`, `vehicle_id`, `trip_id` |

> **The Datathon is judged separately from the Hackathon.** No integration required.

---

## Deadline

**Friday, October 9, 2026, at 11:59 PM** Sri Lanka time (Asia/Colombo, UTC+05:30).

---

## Repository Structure

```
├── check_allocation.py              # Task 2B feasibility validator
├── data/
│   └── raw/                         # Original competition data
│       ├── General Data/            # outlets, vehicles, calendar, district_travel, service_allowance, traffic_speed, road_conditions
│       ├── Training Data/           # deliveries_train.csv, route_legs_train.csv
│       ├── Test Data/               # task1_test_inputs, route_legs_test, task2a_test_inputs, task2b scenario files
│       └── Submission Templates/    # submission_task1.csv, submission_task2a.csv, submission_task2b.csv
├── src/                             # Python source files
├── notebooks/                       # Jupyter notebooks
├── docs/
│   ├── reference/                   # scenario.md, datathon.md (original challenge docs)
│   └── specs/                       # Agent-facing spec files (this directory)
└── AGENTS.md                        # Entry point linking all specs
```

---

## Judging Criteria

| Criterion | Weight |
|---|---|
| Data wrangling and label construction | 20% |
| Model and architecture implementation | 25% |
| Performance score (Task 1, Task 2A) | 20% |
| Task 2B allocation feasibility and prioritization policy | 15% |
| Creativity of the solution | 10% |
| Demo video | 10% |

---

## Competition Rules

1. **No pretrained models** — except for synthetic data generation or preprocessing.
2. **No proprietary API-based modelling/preprocessing** (e.g., OpenAI API for predictions).
3. **No low-code/no-code AI tools** or fully automated end-to-end modelling tools.
4. **AI tools must be disclosed** — explain which work was AI-assisted and how.
5. **All work must be original** — not previously published or exhibited.
6. **All dates/times use Sri Lanka Standard Time** (UTC+05:30).
7. Missing a phase = zero for that phase, but you may continue to later phases.
8. All three phases contribute equally to the overall score.

---

## Related Specs

- [Data Dictionary](./data-dictionary.md) — All CSV schemas and relationships
- [Domain Rules](./domain-rules.md) — Operating constraints and business logic
- [Task 1 Spec](./task1-spec.md) — Service time and lateness prediction
- [Task 2A Spec](./task2a-spec.md) — Depot demand forecasting
- [Task 2B Spec](./task2b-spec.md) — Peak-day fleet allocation
- [Deliverables Checklist](./deliverables-checklist.md) — Everything to submit
