# Deliverables Checklist

> Everything that must be submitted for the Datathon phase.

---

## Deadline

**Friday, October 9, 2026, at 11:59 PM** Sri Lanka time (Asia/Colombo, UTC+05:30)

Submission form: https://forms.gle/CcPPmttWdQgHvUdi6

---

## Packaging

- Place all deliverables in **one folder**.
- Compress as **`TeamName_Datathon.zip`**.
- Upload through the submission form.

---

## Required Deliverables

### 1. Prediction Files (Submissions)

- [ ] `submission_task1.csv` — Service time and lateness predictions
  - Columns: `delivery_id`, `pred_service_min`, `pred_late_prob`
  - Keep exact row order as supplied
  - Do not add or remove rows
- [ ] `submission_task2a.csv` — Weekly depot demand forecasts
  - Columns: `row_id`, `pred_total_volume_m3`, `pred_chilled_volume_m3`
  - Preserve supplied `row_id` values
- [ ] `submission_task2b.csv` — Peak-day fleet allocation
  - Columns: `scenario`, `order_ref`, `outlet_id`, `decision`, `vehicle_id`, `trip_id`
  - Replace all placeholders; leave `vehicle_id` and `trip_id` blank for deferred orders
  - Validate with `check_allocation.py` before submitting

### 2. Final Notebook

- [ ] **`TeamName_FinalNotebook.ipynb`**
  - Retain cells for: label construction, preprocessing, training, evaluation
  - Add a **final cell** that:
    - Loads saved models
    - Demonstrates inference for Task 1 and Task 2A
    - Clearly prints the inputs and predictions

### 3. Model Files

- [ ] Save final trained model files **alongside the notebook**
  - These should be loadable by the inference cell in the notebook

### 4. Architecture Diagrams

- [ ] Show your models, preprocessing pipeline, and proposed deployment approach
  - High-level diagrams are sufficient

### 5. Data Preprocessing Document

- [ ] Brief write-up covering:
  - Data preparation approach
  - Label construction methodology and reasoning
  - Data cleaning steps
  - Feature engineering and rationale

### 6. Peak-Day Prioritization Policy

- [ ] Written policy for Task 2B (~1 page or less)
  - Show calculations behind the allocation
  - Explain deferral reasoning
  - Identify what limited service (bottleneck)
  - Distinguish unavoidable vs. chosen deferrals
  - Describe the cost of deferrals

### 7. Demo Video

- [ ] **3-5 minutes** duration
  - Upload as **unlisted YouTube video**
  - Cover: model architecture, preprocessing, label construction, challenges encountered

### 8. AI Tool Disclosure

- [ ] Explain:
  - Which work was AI-assisted
  - Which work was not
  - How AI tools were used

---

## Submission Format Reminders

- Use **exact filenames** as specified in submission templates.
- Keep all supplied **identifiers and rows unchanged** — mismatched identifiers cannot be scored.
- Task 1 requires the **original row order**.
- All prediction columns must be filled (no blanks in prediction fields).
