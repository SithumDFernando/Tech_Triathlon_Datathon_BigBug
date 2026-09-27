# AI Tool Disclosure

As required by the competition rules, we are disclosing the use of AI tools in the preparation of this Datathon submission.

## 1. What Was AI-Assisted
- **Code Generation**: The Python code for data preprocessing (`src/preprocessing.py`), feature engineering (`src/features_task1.py`, `src/features_task2a.py`), and the allocator script (`src/task2b_allocator.py`) was co-written using an advanced AI coding assistant (Google Antigravity).
- **Documentation**: The AI assistant helped draft the documentation (architecture diagrams, prioritization policy, and this disclosure) based on our notes and outputs.
- **Debugging**: We used the AI to troubleshoot data type issues (e.g., datetime parsing, categorical encoding for LightGBM) and pandas merge conflicts.

## 2. What Was NOT AI-Assisted
- **Data & Domain Understanding**: The interpretation of the Waypoint Group domain rules (time budgets, access constraints, trip time calculation logic) was done by the human team members to ensure strict compliance with the competition spec.
- **Model Choice & Architecture**: The decision to use LightGBM for Tasks 1 and 2A, to apply Isotonic Calibration for probability outputs, and to use a greedy bin-packing heuristic for Task 2B was a human architectural decision.
- **Evaluation**: Validating the outputs against the official `check_allocation.py` and sanity-checking the predictions were performed manually.

## 3. How AI Tools Were Used
- The AI acted as a "pair programmer." We provided explicit instructions and architectural decisions (e.g., "Build a time-series feature pipeline that aggregates by depot and brand, and adds 4-week lags"), and the AI generated the boilerplate pandas and scikit-learn code.
- We did **NOT** use any automated end-to-end AutoML tools, low-code platforms, or proprietary API-based black-box modeling. All final model training (LightGBM) was executed locally on our machine using transparent, open-source libraries as required by the rules.
