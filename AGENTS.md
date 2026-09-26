# AGENTS.md — Tech Triathlon 2026 Datathon

> This file is the entry point for any AI agent working on this project. Read the relevant spec files linked below before starting any task.

---

## Project Context

This is the **Datathon phase** of Tech Triathlon 2026 — a logistics optimization challenge for **Waypoint Group**, a fictional Sri Lankan retail group with 3 brands, 120 outlets, 60 vehicles, and 2 depots. The Datathon has 3 tasks: service time/lateness prediction, demand forecasting, and peak-day fleet allocation.

---

## Spec Files

All specs live in [`docs/specs/`](docs/specs/). Read these before writing any code.

### Start Here

| Spec | Description |
|---|---|
| [Project Overview](docs/specs/project-overview.md) | Competition context, task summaries, judging weights, competition rules |
| [Data Dictionary](docs/specs/data-dictionary.md) | Every CSV file schema, column definitions, join keys, entity relationships |
| [Domain Rules](docs/specs/domain-rules.md) | Vehicle/outlet/brand constraints, order flow, depot topology, fleet composition, time budgets |

### Task-Specific Specs

| Spec | Task | Type |
|---|---|---|
| [Task 1 Spec](docs/specs/task1-spec.md) | Predict service time and lateness | ML Prediction |
| [Task 2A Spec](docs/specs/task2a-spec.md) | Forecast depot demand | Time-Series Forecasting |
| [Task 2B Spec](docs/specs/task2b-spec.md) | Peak-day fleet allocation | Constraint Optimization |

### Submission

| Spec | Description |
|---|---|
| [Deliverables Checklist](docs/specs/deliverables-checklist.md) | Complete list of what to submit, format rules, packaging, deadline |

---

## Quick Reference

### Key Paths

| Path | Contents |
|---|---|
| `data/General Data/` | Reference tables: outlets, vehicles, calendar, district_travel, service_allowance, traffic_speed, road_conditions |
| `data/Training Data/` | `deliveries_train.csv`, `route_legs_train.csv` |
| `data/Test Data/` | Task inputs: `task1_test_inputs.csv`, `route_legs_test.csv`, `task2a_test_inputs.csv`, `task2b_peak_day_scenarios.csv`, `task2b_peak_day_fleet.csv` |
| `data/Submission Templates/` | `submission_task1.csv`, `submission_task2a.csv`, `submission_task2b.csv` |
| `check_allocation.py` | Task 2B feasibility validator |
| `docs/reference/` | Original challenge documents (scenario.md, datathon.md) |

### Critical Rules (Do Not Violate)

1. **No pretrained models** (except for synthetic data generation or preprocessing).
2. **No proprietary API-based modelling/preprocessing.**
3. **No low-code/no-code AI tools** or automated end-to-end modelling tools.
4. **Submission identifiers must match exactly** — mismatched identifiers cannot be scored.
5. **Task 1 row order must be preserved.**
6. **Task 2B must pass `check_allocation.py`** before submission.

### Deadline

**Friday, October 9, 2026, at 11:59 PM** Sri Lanka time (UTC+05:30)
