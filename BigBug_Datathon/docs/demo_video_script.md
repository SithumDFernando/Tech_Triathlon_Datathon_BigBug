# Team BigBug — Datathon Demo Video Presentation Script

> **Target Duration:** 3:30 – 4:00 Minutes (Competition window: 3–5 minutes)  
> **Presentation Style:** Conversational, confident, human-paced screen recording with voiceover  
> **Video Format:** Screen recording uploaded to YouTube as **Unlisted**  
> **Deliverable Item:** Item 7 in Deliverables Checklist (10% of total Datathon score)  
> **Key Topics:** System Architecture, Data Preprocessing, Label Construction, Calibrated Machine Learning, Demand Forecasting, Constraint Optimization Policy, and Live Inference.

---

## 🎬 Quick Setup Checklist Before You Hit Record

1. **Resolution & Zoom:** 1080p (1920×1080). Press `Ctrl + +` once or twice in VS Code so all notebook code and markdown headings are easy to read.
2. **Windows Prepared:**
   - **Window 1 (Main):** VS Code with `BigBug_FinalNotebook.ipynb` open.
   - **Window 2 (Terminal):** Terminal pane split at the bottom or separate window in project root (`TT_Datathon`).
   - **Window 3 (Reference):** `docs/architecture_diagrams.md` preview open in a side tab.
3. **Recording Tool:** 
   - Windows Game Bar (`Win + G` → Start Recording)
   - OR OBS Studio / Loom / Zoom (Solo meeting → Share Screen → Record).

---

## ⏱️ Scene-by-Scene Script with Exact In-Line Scroll Anchors

---

### ⏱️ [0:00 – 0:35] Scene 1: Introduction & High-Level Architecture

#### 📍 [ACTION 1A]: Start at top of `BigBug_FinalNotebook.ipynb`
*Show the title markdown cell: `# Task 1: Service Time & Lateness Prediction — Team BigBug`.*

🗣️ **[SAY — Tone: Warm, welcoming, confident]:**
> *"Hi everyone, and welcome judges! We are Team BigBug, and today we’re excited to walk you through our complete solution for the Tech Triathlon Datathon challenge.*
> 
> *Waypoint Group operates a shared logistics network across Sri Lanka, serving 120 retail outlets from 2 central distribution depots in Peliyagoda and Kandy across 3 distinct retail brands: Fresh for groceries, Style for apparel, and Tech for consumer electronics."*

---

#### 📍 [ACTION 1B]: Switch to tab `docs/architecture_diagrams.md` (Mermaid Flowchart)
*Hover cursor over the flowchart showing Data Sources (`deliveries_train.csv`, `route_legs_train.csv`, `calendar.csv`) flowing into Preprocessing, then into LightGBM models and the Greedy Allocator.*

🗣️ **[SAY — Tone: Analytical, clear]:**
> *"To solve the challenge, we designed an end-to-end modular pipeline. As you can see in our system architecture diagram, we take the raw operational data—including delivery legs, vehicle constraints, district travel matrices, and calendar events—and unify them into a single source of truth.*
> 
> *From there, we branch into 3 tailored engines: Light Gradient Boosting Machine—or LightGBM—for service time regression, an Isotonic-calibrated classifier for lateness probability, a recursive time-series model for weekly demand forecasting, and a constraint-based bin-packing solver for festival peak-day fleet allocation."*

---

### ⏱️ [0:35 – 1:30] Scene 2: Data Preprocessing & Label Construction (Task 1)

#### 📍 [ACTION 2A]: Switch back to `BigBug_FinalNotebook.ipynb` and scroll to Cell 3 & 4
*Scroll to `## 1. Load Data & Construct Labels`. Highlight the output of Cell 3 showing 92,307 delivery rows and 91,894 route leg rows.*

🗣️ **[SAY — Tone: Engaging, storytelling]:**
> *"Jumping into Task 1, our first major hurdle was that the raw data didn't come with pre-packaged labels. We had 92,307 historical delivery orders and 91,894 route leg records.*
> 
> *To construct the service duration label, we took the outlet departure time and subtracted the arrival time. But as we explored the data, we noticed something interesting: vehicles often arrive early, before the store's scheduled delivery window even opens. Drivers end up waiting at the dock, which artificially inflates their dwell time."*

---

#### 📍 [ACTION 2B]: In Cell 4, highlight the printed summary stats
*Point cursor to: `mean: 19.85 min`, `median: 16.0 min`, `Late rate: 0.1958 (17991 / 91894)`, `Early arrival rate: 0.0438`.*

🗣️ **[SAY — Tone: Thoughtful, pragmatic]:**
> *"Rather than artificially stripping out that wait time with arbitrary rules, we recognized that in real-world retail logistics, early dwell time is part of the physical delivery cost. We capped extreme loading outliers at 180 minutes, and preserved the true operational duration.*
> 
> *Our dataset revealed an average service duration of 19.85 minutes, an early arrival rate of 4.38%, and an overall historical lateness rate of 19.58%—meaning roughly 1 in 5 deliveries ran late.*
> 
> *For lateness, we defined a clean binary indicator: did the vehicle's arrival time exceed the customer window close time?"*

---

#### 📍 [ACTION 2C]: Scroll to Cell 9 (`Total model features: 37`)
*Highlight the feature list: `order_units`, `order_weight_kg`, `order_volume_m3`, `dow`, `is_payday`, `festival_ramp`, `window_duration_min`, `planned_slack_min`, `speed_index`.*

🗣️ **[SAY — Tone: Confident, technical]:**
> *"To help the models capture these dynamics, we engineered exactly 37 features across 4 pillars: physical order attributes like units, weight, and volume; temporal signals including Day of the Week—or DOW—payday spikes, and the April festival ramp; route geography like stop sequence and speed indices; and buffer metrics like planned slack minutes, which directly tell the model how tight a delivery window is."*

---

### ⏱️ [1:30 – 2:30] Scene 3: Modeling, Probability Calibration & Forecasting (Task 1 & 2A)

#### 📍 [ACTION 3A]: Scroll to Cell 12 (`=== Service Time Model ===`)
*Highlight Cell 12 output: `Train RMSE: 5.648 | Val RMSE: 6.247`, `Train MAE: 3.930 | Val MAE: 3.918`, `Val R²: 0.7821`.*

🗣️ **[SAY — Tone: Direct, results-focused]:**
> *"We trained our models using Light Gradient Boosting Machine on a strict time-based split—using the first 75 weeks for training, and holding out the final 4 weeks as our validation set.*
> 
> *For service time regression, our model achieved a validation Root Mean Squared Error—or RMSE—of 6.247 minutes, an average Mean Absolute Error—or MAE—of just 3.918 minutes, and a Coefficient of Determination—or R-squared—of 0.7821, meaning it explains over 78% of service duration variance."*

---

#### 📍 [ACTION 3B]: Scroll to Cell 15 & 17 (`=== Lateness Probability Model ===` & `Calibration`)
*Highlight Cell 15 output: `Val ROC AUC: 0.9738`, `Val Brier Score: 0.0475`.*  
*Then highlight Cell 17 output: `After calibration — Brier: 0.0400, AUC: 0.9750`.*

🗣️ **[SAY — Tone: Explanatory, proud]:**
> *"For lateness prediction, raw gradient-boosted trees gave us a strong Receiver Operating Characteristic Area Under the Curve—or ROC-AUC—of 0.9738. But tree classifiers are notoriously overconfident with raw probabilities.*
> 
> *To fix this, we passed the predicted probabilities through an Isotonic Calibrator. This pushed our validation ROC-AUC up to 0.9750, and lowered our Brier Score—which measures probability calibration error—down to 0.0400, ensuring our probability scores represent true statistical likelihoods."*

---

#### 📍 [ACTION 3C]: Scroll down to `## 3. Generate Forecast (Weeks 14-23)` in Task 2A
*Highlight Cell 5 & 6 (recursive loop from week 14 to 23), then Cell 7 displaying the submission head (`W0000 = 1037.36 m³ total, 381.87 m³ chilled`, and `W0001 Style chilled = 0.0000`).*

🗣️ **[SAY — Tone: Systematic]:**
> *"Moving to Task 2A, we forecasted depot demand for 10 future weeks—from International Organization for Standardization—or ISO—week 14 through week 23 of 2026 across both depots and all 3 brands.*
> 
> *We implemented a recursive forecaster with 4-week autoregressive lag features and rolling monthly averages, tightly aligned with Sri Lankan calendar paydays, monsoon rains, and holiday counts. Furthermore, we strictly adhered to domain rules: ambient brands Style and Tech were explicitly constrained to 0.0 m³ of chilled volume."*

---

### ⏱️ [2:30 – 3:20] Scene 4: Task 2B Peak-Day Allocation & Constraint Validation

#### 📍 [ACTION 4A]: Switch to Terminal window
*Type and run the official checker command:*
```bash
python check_allocation.py "BigBug_Datathon/submission_task2b.csv"
```
*Wait 1 second until the terminal outputs:*
```text
FEASIBILITY: PASSED - every rule satisfied.
```

🗣️ **[SAY — Tone: Decisive, authoritative]:**
> *"Now for Task 2B: peak-day fleet allocation under Scenario S1. On this festival peak day, 85 store orders arrived, but several vehicles were grounded in the workshop.*
> 
> *When we ran capacity math on the Peliyagoda depot, we pinpointed the exact bottleneck: Refrigerated vehicle capacity. Total chilled demand surged to 181.6 m³ across 26 Fresh orders. But Peliyagoda had only 4 refrigerated trucks and vans available, offering a maximum 2-trip physical capacity of 172.4 m³. Serving every single chilled order was mathematically impossible."*

---

#### 📍 [ACTION 4B]: Keep terminal visible highlighting `FEASIBILITY: PASSED`
*Point with cursor to `FEASIBILITY: PASSED - every rule satisfied.`*

🗣️ **[SAY — Tone: Fair, solution-oriented]:**
> *"Rather than deferring randomly, we engineered a greedy bin-packing prioritization policy focused on fairness: any store deferred yesterday was strictly guaranteed delivery today. In total, 14 orders were deferred—13 chilled Fresh orders and 1 Style order—and every single one of them had been successfully served the previous day, preventing back-to-back stockouts.*
> 
> *As you can see live in our terminal, running the official competition validator outputs: FEASIBILITY: PASSED with 0 violations across capacity, district segregation, and time budgets."*

---

### ⏱️ [3:20 – 3:55] Scene 5: Live Inference Demonstration & Wrap-Up

#### 📍 [ACTION 5A]: Return to Notebook and scroll to the very last cell: `# Final Inference Demonstration`
*Highlight the executed output of Cell 1:*
- *Task 1: Order `ORD0092308` (Peliyagoda, Fresh, Colombo) → `pred_service_min: 8.22`, `pred_late_prob: 0.0`*
- *Task 2A: Row `W0000` (Kandy, Fresh, W14) → `pred_total_volume_m3: 1037.36`, `pred_chilled_volume_m3: 381.87`*

🗣️ **[SAY — Tone: Warm, concluding]:**
> *"To ensure complete reproducibility, our final notebook includes a self-contained inference cell. As shown here, it loads our saved LightGBM models and instantly evaluates new delivery manifests and 10-week demand forecast requests in real time.*
> 
> *All deliverables—including our verified submission CSV files, trained model files, data preprocessing documentation, prioritization policy, and our transparent AI tool disclosure—are fully assembled inside `BigBug_Datathon.zip`.*
> 
> *Thank you very much to Rootcode and the judges for this fantastic challenge. We look forward to your questions!"*

---

## 📊 Quick-Reference Metric Cross-Reference Table

*(Verified against `BigBug_Datathon/BigBug_FinalNotebook.ipynb`)*

| Metric / Parameter | Value in Notebook | Expanded Form & Definition |
|---|---|---|
| **Raw Deliveries / Route Legs** | `92,307` / `91,894` | Historical delivery transactions & GPS route legs |
| **Clean Labeled Set** | `91,894` rows | Combined labeled records after merging |
| **Service Duration Mean / Median** | `19.85 min` / `16.00 min` | Dwell duration: departure minus arrival |
| **Historical Lateness Rate** | `19.58%` (17,991 / 91,894) | Orders where arrival exceeded window close |
| **Early Arrival Rate** | `4.38%` | Trucks arriving before window open |
| **Engineered Features** | `37` features | Input dimensions for Task 1 models |
| **Train / Validation Split** | `88,395` (96.2%) / `3,499` (3.8%) | Time-based holdout split (cutoff: 2026-01-17) |
| **Task 1 Service RMSE** | `6.247 min` (Val) | Root Mean Squared Error (RMSE) |
| **Task 1 Service MAE** | `3.918 min` (Val) | Mean Absolute Error (MAE) |
| **Task 1 Service R²** | `0.7821` (Val) | Coefficient of Determination ($R^2$) |
| **Task 1 Best Iteration (Service)** | `488` trees | Early stopping iteration for regressor |
| **Task 1 Uncalibrated ROC-AUC** | `0.9738` (Val) | Receiver Operating Characteristic — Area Under the Curve |
| **Task 1 Uncalibrated Brier Score** | `0.0475` (Val) | Probability forecast mean squared error |
| **Task 1 Calibrated ROC-AUC** | `0.9750` (Val) | Area Under Curve after Isotonic Calibration |
| **Task 1 Calibrated Brier Score** | `0.0400` (Val) | Calibrated probability error (lower is better) |
| **Task 1 Best Iteration (Late)** | `680` trees | Early stopping iteration for classifier |
| **Task 1 Test Output Orders** | `5,014` deliveries | Rows in `task1_test_inputs.csv` |
| **Task 2A Grid & Horizons** | `6` streams, `10` weeks | 2 depots × 3 brands across 2026 W14–W23 |
| **Task 2B Chilled Demand** | `181.6 m³` | Chilled volume demanded across 26 orders |
| **Task 2B Available Fleet Capacity** | `172.4 m³` (max 2 trips) | Capacity of 4 available reefer vehicles |
| **Task 2B Deferrals** | `14` orders (13 Fresh, 1 Style) | Protected 100% of outlets deferred yesterday |
| **Task 2B Feasibility Result** | **PASSED** | Official validator (`check_allocation.py`) passed |

---

## 🚀 Recording & Submission Instructions

1. **Rehearse Once:** Read the script aloud while scrolling in VS Code to ensure smooth timing (~3 minutes 45 seconds).
2. **Record Screen:**
   - Use Windows Game Bar (`Win + G`), OBS, or Zoom.
   - Keep microphone volume clear and background quiet.
3. **Upload Video:**
   - Go to [studio.youtube.com](https://studio.youtube.com/)
   - Upload file → Title: `Tech Triathlon 2026 Datathon - Team BigBug Demo`
   - **Visibility: UNLISTED** (Anyone with the link can watch).
4. **Submit Form:**
   - Link: https://forms.gle/CcPPmttWdQgHvUdi6
   - Paste the YouTube link and upload `BigBug_Datathon.zip`.
