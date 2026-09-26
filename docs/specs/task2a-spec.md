# Task 2A: Forecast Depot Demand

> Forecast the volume ordered for each depot and brand over 10 future weeks.

---

## Objective

For every row in the test inputs (one per depot x brand x iso_week), predict:

| Target | Column | Type | Description |
|---|---|---|---|
| Total volume | `pred_total_volume_m3` | number (m3) | Total order volume for that depot, brand, and week |
| Chilled volume | `pred_chilled_volume_m3` | number (m3) | Chilled portion of that total |

> You only need to predict volumes. You do NOT need to convert them into vehicle or driver requirements.

---

## Training Data Construction Rules

These rules are critical — how you build training data is part of the assessment.

### Rule 1: Count Every Order

Include ALL orders regardless of dispatch status:
- `attempted` — dispatched on order_date
- `deferred` — dispatched later
- `not_run` — never dispatched

**All represent demand.** A deferred or undelivered order still means the store wanted that volume.

### Rule 2: Assign Orders to Request Week

Assign each order to the week the store requested it, NOT when it was dispatched:
- Use `order_date` to determine the week.
- Look up `iso_year` and `iso_week` from `calendar.csv` for that date.
- The forecast periods in the test inputs use iso_year/iso_week — your training aggregation must match.

### Rule 3: Chilled Volume by Brand

- **Only Fresh has chilled demand.** Fresh orders with `temp_requirement = chilled` contribute to chilled volume.
- **Set `pred_chilled_volume_m3 = 0` for Style and Tech** — always, unconditionally.

### Rule 4: Data Sources

Build training data from BOTH:
- `deliveries_train.csv` (Training Data) — historical orders
- `task1_test_inputs.csv` (Test Data) — these are also historical orders from a later period

Both files have the same order-record schema with `order_date`, `order_volume_m3`, `temp_requirement`, `depot`, `brand`.

### Aggregation

For each (depot, brand, iso_year, iso_week) combination, sum:
- `order_volume_m3` across ALL orders → total volume
- `order_volume_m3` where `temp_requirement = chilled` → chilled volume (Fresh only)

---

## Input Files

| File | Location | Use |
|---|---|---|
| `task2a_test_inputs.csv` | `data/Test Data/` | Forecast grid — rows to predict |
| `deliveries_train.csv` | `data/Training Data/` | Historical orders for training |
| `task1_test_inputs.csv` | `data/Test Data/` | Additional historical orders for training |
| `calendar.csv` | `data/General Data/` | Maps dates to iso_year/iso_week + contextual features |

---

## Feature Considerations

- **Seasonal patterns:** Weekly, monthly, and yearly trends in demand
- **Festival effects:** `festival_ramp` rises over 9 days before a festival
- **Payday effects:** `is_payday` flag in calendar
- **Monsoon:** `monsoon` flag — may affect both demand patterns and delivery capabilities
- **Brand-specific patterns:** Fresh is daily, Style is weekly with seasonal peaks, Tech is sporadic
- **Depot differences:** Peliyagoda and Kandy may have different demand profiles

---

## Output Format

Complete `data/Submission Templates/submission_task2a.csv`:

| Column | Requirement |
|---|---|
| `row_id` | Keep unchanged — exact values from the template |
| `pred_total_volume_m3` | Fill with predicted total demand volume (m3) |
| `pred_chilled_volume_m3` | Fill with predicted chilled volume (m3). Use 0 for Style and Tech. |

### Rules
- Preserve the supplied `row_id` values.
- Fill only the two prediction columns.

---

## Model Restrictions

Same as Task 1:
- No pretrained models (except for synthetic data generation or preprocessing).
- No proprietary API-based modelling/preprocessing.
- No low-code/no-code AI tools or automated end-to-end modelling tools.
