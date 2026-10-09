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

### ⏱️ [0:00 – 0:30] Scene 1: Introduction & High-Level Architecture (~65 words)

#### 📍 [ACTION 1A]: Start at top of `BigBug_FinalNotebook.ipynb`
*Show title cell: `# Task 1: Service Time & Lateness Prediction — Team BigBug`.*

🗣️ **[SAY — Tone: Confident, energetic]:**
> *"Hi judges! We’re Team BigBug, presenting our end-to-end machine learning and optimization pipeline for the Tech Triathlon Datathon challenge."*

---

#### 📍 [ACTION 1B]: Switch to tab `docs/architecture_diagrams.md` (Mermaid Flowchart)
*Hover cursor over the flowchart showing Data Sources flowing into Preprocessing, Models, and Allocator.*

🗣️ **[SAY — Tone: Analytical, structured]:**
> *"As shown in our system architecture, our modular pipeline unifies raw delivery records, route legs, and calendar features into a single source of truth.
> 
> From there, we drive three specialized engines: calibrated LightGBM models for Task 1 service time and lateness, a recursive time-series forecaster for Task 2A, and a constraint-based greedy allocator for Task 2B."*

---

### ⏱️ [0:30 – 1:15] Scene 2: Data Preprocessing & Label Construction (~95 words)

#### 📍 [ACTION 2A]: Switch back to `BigBug_FinalNotebook.ipynb` and scroll to Cell 3 & 4
*Scroll to `## 1. Load Data & Construct Labels`. Highlight the printed dataset shapes and summary stats.*

🗣️ **[SAY — Tone: Engaging, practical]:**
> *"For Task 1, our first hurdle was constructing clean labels from over 90,000 operational records. We derived service time directly from departure minus arrival.
> 
> Crucially, we observed that trucks frequently arrive before delivery windows open. Rather than stripping that dwell time, we retained it as a real operational cost and capped extreme loading outliers at 180 minutes. For lateness, we flagged deliveries where arrival exceeded the window close."*

---

#### 📍 [ACTION 2B]: Scroll to Cell 9 (`Total model features: 37`)
*Highlight the engineered feature categories.*

🗣️ **[SAY — Tone: Confident, technical]:**
> *"We engineered 37 features across four pillars: physical order dimensions, temporal cycles like paydays and the festival ramp, route geography, and planned buffer slack—giving the model direct visibility into schedule tightness."*

---

### ⏱️ [1:15 – 2:15] Scene 3: Modeling, Calibration & Forecasting (~120 words)

#### 📍 [ACTION 3A]: Scroll to Cell 12 (`=== Service Time Model ===`)
*Highlight validation metrics on screen: `Val RMSE: 6.247`, `Val MAE: 3.918`, `Val R²: 0.7821`.*

🗣️ **[SAY — Tone: Direct, results-focused]:**
> *"We evaluated our models using a strict 75-week train and 4-week holdout split.
> 
> For service time regression, our LightGBM model achieves an MAE under 4 minutes and an R² of 0.78, explaining the vast majority of service duration variance."*

---

#### 📍 [ACTION 3B]: Scroll to Cell 15 & 17 (`Calibration`)
*Highlight Cell 17 output: `After calibration — Brier: 0.0400, AUC: 0.9750`.*

🗣️ **[SAY — Tone: Explanatory, technical]:**
> *"For lateness classification, gradient boosting achieved a high ROC-AUC of 0.975. Crucially, we applied Isotonic Calibration, driving our Brier score down to 0.04. This ensures our predicted probabilities reflect genuine operational risks rather than overconfident tree scores."*

---

#### 📍 [ACTION 3C]: Scroll to `## 3. Generate Forecast` in Task 2A
*Highlight Cell 5-7 displaying the 10-week forecast head and the zero chilled volume for ambient brands.*

🗣️ **[SAY — Tone: Systematic]:**
> *"For Task 2A depot forecasting across weeks 14 to 23, we implemented recursive models incorporating autoregressive lags and holiday features, strictly enforcing the domain constraint that ambient brands Style and Tech have zero chilled volume."*

---

### ⏱️ [2:15 – 3:00] Scene 4: Task 2B Peak-Day Allocation & Validation (~95 words)

#### 📍 [ACTION 4A]: Switch to Terminal window
*Type and run the official checker command:*
```bash
python check_allocation.py "BigBug_Datathon/submission_task2b.csv"
```
*Terminal outputs:*
```text
FEASIBILITY: PASSED - every rule satisfied.
```

🗣️ **[SAY — Tone: Decisive, authoritative]:**
> *"For Task 2B festival peak allocation, our capacity analysis uncovered a hard physical bottleneck: Peliyagoda chilled demand exceeded available refrigerated fleet capacity by roughly 9 cubic meters, making full fulfillment mathematically impossible.
> 
> Rather than deferring arbitrarily, we designed a greedy bin-packing policy anchored on fairness: any outlet deferred yesterday was strictly protected today. We deferred 14 orders—all of which were served yesterday, preventing back-to-back stockouts.
> 
> As shown live, running the official validator confirms: FEASIBILITY: PASSED with zero constraint violations."*

---

### ⏱️ [3:00 – 3:35] Scene 5: Live Inference & Wrap-Up (~60 words)

#### 📍 [ACTION 5A]: Return to Notebook and scroll to `# Final Inference Demonstration`
*Run or highlight the live inference output showing instant predictions across all tasks.*

🗣️ **[SAY — Tone: Warm, concluding]:**
> *"Finally, our notebook features a self-contained live inference block, instantly generating predictions for new delivery manifests and weekly demand queries.
> 
> All deliverables—including validated CSVs, trained models, technical documentation, and AI disclosure—are complete and packaged in BigBug_Datathon.zip.
> 
> Thank you very much to Rootcode and the judges!"*

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
