# Team BigBug — Datathon Demo Video Presentation Script

> **Target Duration:** 3:30 – 4:00 Minutes (Competition requirement: 3–5 minutes)  
> **Format:** Screen recording with voiceover (upload as **Unlisted** YouTube video)  
> **Deliverable Item:** Item 7 in Deliverables Checklist (10% of total Datathon score)  
> **Key Topics Covered:** Model Architecture, Preprocessing Pipeline, Label Construction, Operational Challenges, Validation Results, and Live Inference.

---

## 🎬 Quick Setup Checklist Before You Hit Record

1. **Screen Resolution:** 1080p (1920x1080) recommended. Zoom in your editor/browser slightly (`Ctrl + +`) so code and text are sharp and easy to read.
2. **Windows to Have Ready:**
   - **Window 1 (Main):** VS Code with `BigBug_FinalNotebook.ipynb` open.
   - **Window 2 (Terminal):** Split terminal or command prompt inside project root (`TT_Datathon`).
   - **Window 3 (Optional backup):** `docs/architecture_diagrams.md` preview in VS Code or browser.
3. **Recording Tool:** 
   - Windows Game Bar (`Win + G` → Click Record)
   - OR OBS Studio / Loom / Zoom (Host a solo meeting, share screen, click Record).

---

## ⏱️ Scene-by-Scene Script with Exact Visual Cues

---

### ⏱️ [0:00 – 0:35] Scene 1: Introduction & High-Level Architecture

#### 👁️ Visual Cues (What to show on screen)
* **Start On:** `BigBug_FinalNotebook.ipynb` at the very top (Title markdown cell: *"Task 1: Service Time & Lateness Prediction — Team BigBug"*).
* **Switch / Scroll To:** `docs/architecture_diagrams.md` (or the architecture diagram preview) showing the **End-to-End Pipeline Diagram** (Data Sources → Preprocessing → Modeling → Submissions).
* **Mouse Action:** Slowly hover over the boxes: `deliveries_train.csv` + `route_legs_train.csv` feeding into Preprocessing, then branching to LightGBM and the Greedy Allocator.

#### 🎙️ Spoken Audio (Word-for-Word Script)
> *"Hello judges, we are Team BigBug. Today, we're presenting our complete data science and optimization solution for the Waypoint Group Datathon.*
> 
> *Waypoint Group manages a complex, shared retail distribution network across three distinct brands—Fresh, Style, and Tech—supplying 120 retail outlets from central depots in Peliyagoda and Kandy.*
> 
> *As shown in our system architecture, our approach unifies transactional deliveries, route tracking, store parking constraints, and Sri Lankan calendar data into a robust, single-source-of-truth pipeline. We leverage LightGBM machine learning models for service duration and demand forecasting, and a constraint-based bin-packing solver for peak-day fleet allocation."*

---

### ⏱️ [0:35 – 1:30] Scene 2: Data Preprocessing & Label Construction (Task 1)

#### 👁️ Visual Cues (What to show on screen)
* **Switch Back To:** `BigBug_FinalNotebook.ipynb`.
* **Scroll To:** **"1. Load Data & Construct Labels"** (Cells 3 and 4).
* **Highlight / Point To:** 
  * The `construct_labels` import and execution.
  * The printed output:
    * `Service time stats: mean = 19.85 min, median = 16.0 min`
    * `Late rate: 0.1958 (17,991 / 91,894)`
    * `Early arrival rate: 0.0438`
* **Scroll Down Slightly To:** Feature engineering section showing the 37 engineered variables (`window_duration_min`, `planned_slack_min`, `arrived_early`, `dow`, `festival_ramp`).

#### 🎙️ Spoken Audio (Word-for-Word Script)
> *"Moving to Task 1, our most critical preprocessing challenge was label construction, as raw logs did not provide ground-truth targets directly.*
> 
> *We constructed `service_time_min` as outlet departure time minus arrival time. An interesting operational challenge we discovered was that early vehicle arrivals artificially inflate duration, because drivers must wait for the outlet delivery window to open. Rather than manually deducting wait time, we engineered features such as `planned_slack_min` and `arrived_early` to allow our model to learn true dwell time patterns naturally.*
> 
> *For lateness, we constructed a binary target indicating whether arrival exceeded the delivery window close time.*
> 
> *Our pipeline extracts 37 rich features—capturing order volume and weight, road network speeds, store dock types, and temporal factors like payday surges and holiday traffic."*

---

### ⏱️ [1:30 – 2:30] Scene 3: Modeling, Calibration & Forecasting (Task 1 & Task 2A)

#### 👁️ Visual Cues (What to show on screen)
* **In Notebook:** Scroll to **Task 1 Model Evaluation** cells.
* **Highlight Output 1 (Service Time):**
  * `Train RMSE: 5.648 | Val RMSE: 6.247`
  * `Train MAE: 3.930 | Val MAE: 3.918`
  * `Val R²: 0.7821`
* **Highlight Output 2 (Lateness & Calibration):**
  * `Train ROC AUC: 0.9419 | Val ROC AUC: 0.9381`
  * `Val Brier Score: 0.0401`
  * `Val Log Loss: 0.1444`
* **Scroll Down To:** **Task 2A Demand Forecasting** (the step-by-step recursive forecast loop across weeks 14 to 23).
* **Point To:** The rule enforcing `pred_chilled_volume_m3 = 0.0` for Style and Tech.

#### 🎙️ Spoken Audio (Word-for-Word Script)
> *"For predictive modeling, we chose LightGBM for its speed and superior handling of tabular interactions.*
> 
> *For service time regression, our model achieved a validation RMSE of 6.2 minutes and an MAE of 3.9 minutes, explaining over 78% of service variance.*
> 
> *For lateness probability, standard tree classifiers often output overconfident scores. To resolve this, we applied Isotonic Regression calibration. This dramatically improved our probability reliability, achieving an outstanding validation ROC-AUC of 0.938 and reducing our Brier score to 0.040.*
> 
> *For Task 2A, we built a recursive time-series forecaster projecting 10 weeks of depot demand. We engineered 4-week autoregressive lag features and aggregated weekly calendar variables—such as payday counts and the Sinhala and Tamil New Year festival ramp. Importantly, we strictly enforced domain rules: ambient brands Style and Tech were locked to exactly zero chilled volume."*

---

### ⏱️ [2:30 – 3:20] Scene 4: Task 2B Peak-Day Allocation & Feasibility

#### 👁️ Visual Cues (What to show on screen)
* **Open Terminal Window:** Bring terminal into focus.
* **Type and Run:** 
  ```bash
  python check_allocation.py "BigBug_Datathon/submission_task2b.csv"
  ```
* **Wait 1 Second & Highlight Output:**
  ```text
  FEASIBILITY: PASSED - every rule satisfied.
  ```
* **Briefly Show / Mention:** `docs/task2b_prioritization_policy.md` summary (the calculation showing 181.6 m³ chilled demand vs 172.4 m³ theoretical fleet capacity).

#### 🎙️ Spoken Audio (Word-for-Word Script)
> *"Task 2B presented an operational constraint optimization challenge during Scenario S1. On this festival peak day, demand surged while several vehicles were sidelined in the workshop.*
> 
> *Through mathematical capacity analysis, we identified the definitive bottleneck: Refrigerated vehicle capacity. Chilled demand reached 181.6 cubic meters across 26 orders, but Peliyagoda only had 4 available reefer vehicles, yielding a maximum two-trip capacity of 172.4 cubic meters. Serving all chilled orders was mathematically impossible.*
> 
> *We implemented a greedy bin-packing prioritization policy designed around fairness and customer retention: outlets deferred yesterday were strictly protected from back-to-back stockouts. In total, 14 orders were deferred—13 chilled Fresh orders and 1 Style order—all of which had been served the previous day.*
> 
> *As verified live in our terminal, running the official validator confirms: FEASIBILITY: PASSED with zero constraint violations."*

---

### ⏱️ [3:20 – 3:55] Scene 5: Live Inference Demonstration & Wrap-Up

#### 👁️ Visual Cues (What to show on screen)
* **Back in Notebook:** Scroll to the very last cell: **"Final Inference Demonstration"**.
* **Highlight Code & Output:**
  * Task 1 Input order (`ORD0092308`) → Predicted Service Time: `8.22 min`, Predicted Late Prob: `0.0`.
  * Task 2A Input request (`W0000`, Kandy Fresh Week 14) → Predicted Total: `1037.36 m³`, Chilled: `381.87 m³`.
* **Switch To File Explorer:** Show the root workspace directory with `BigBug_Datathon.zip` and the generated submission CSVs.

#### 🎙️ Spoken Audio (Word-for-Word Script)
> *"Finally, our solution is fully reproducible and deployment-ready. As demonstrated in our final notebook cell, our saved models load seamlessly and execute instant inference for new delivery orders and weekly forecast requests.*
> 
> *All deliverables—including our verified submission files, trained model weights, prioritization policy, and complete AI tool disclosures—are packaged in `BigBug_Datathon.zip`.*
> 
> *Thank you to Rootcode and the judges for this engaging challenge. Team BigBug looks forward to the next stage of the Triathlon!"*

---

## 📊 Summary of Key Metrics to Mention

| Metric | Value | Significance |
|---|---|---|
| **Task 1 Service RMSE** | `6.247 min` | Low error on high-variance unloading times |
| **Task 1 Service MAE** | `3.918 min` | Average prediction within 4 minutes |
| **Task 1 Val R²** | `0.7821` | Captures 78.2% of service time variance |
| **Task 1 Lateness ROC-AUC** | `0.9381` | Exceptional rank-ordering of high-risk trips |
| **Task 1 Brier Score** | `0.0401` | Highly calibrated probabilities via Isotonic Regression |
| **Task 2B Chilled Demand** | `181.6 m³` | Exceeded available fleet capacity of `172.4 m³` |
| **Task 2B Deferrals** | `14 orders` | Protected all outlets deferred yesterday |
| **Task 2B Feasibility** | **PASSED** | 100% compliant with all domain & vehicle constraints |

---

## 🚀 Post-Recording Steps (Submit Before 11:59 PM)

1. **Review Recording:** Verify audio is audible and total runtime is between **3:15 and 4:15 minutes**.
2. **Upload to YouTube:**
   - Go to [studio.youtube.com](https://studio.youtube.com/)
   - Title: `Tech Triathlon 2026 Datathon - Team BigBug Demo`
   - **Visibility: UNLISTED** (Crucial: Public is not needed, Private cannot be viewed by judges).
3. **Grab the URL:** e.g., `https://youtu.be/xxxxxxxxx`
4. **Submit Form:** Paste your unlisted YouTube link and upload `BigBug_Datathon.zip` at:
   👉 **https://forms.gle/CcPPmttWdQgHvUdi6**
