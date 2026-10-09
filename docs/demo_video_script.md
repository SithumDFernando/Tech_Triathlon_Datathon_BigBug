# BigBug - Datathon Demo Video Script

**Target Duration**: 3-5 minutes
**Format**: Screen recording with voiceover (upload as unlisted YouTube video).

## [0:00 - 0:30] Introduction
**Visual**: Title slide with Team Name "BigBug" and "Tech Triathlon 2026 Datathon". Switch to `BigBug_FinalNotebook.ipynb` showing the architecture diagram.
**Audio**: 
"Hello judges, we are team BigBug. Today we'll walk you through our solution for the Waypoint Group Datathon. Our approach focused on building a robust, single-source-of-truth data pipeline and leveraging LightGBM for fast, accurate predictions. As you can see in our architecture diagram, we unified the provided geographic, calendar, and transactional data into cohesive datasets before feeding them into our models."

## [0:30 - 1:30] Data Preprocessing & Label Construction
**Visual**: Show `src/preprocessing.py` focusing on the `construct_labels` function.
**Audio**: 
"For Task 1, our biggest preprocessing challenge was label construction. We defined service time as the difference between `leave_outlet_time` and `arrival_time`. We noticed that early arrivals inflate this duration because vehicles wait for the delivery window to open. Rather than manually deducting this wait time, we engineered features like `planned_slack_min` and `arrived_early` to let our models learn the operational reality implicitly. Lateness was modeled as a straightforward binary: did the arrival time exceed the window close time?"

## [1:30 - 2:30] Task 1 & 2A Modeling (LightGBM)
**Visual**: Scroll through the `02_task1_modeling.ipynb` and `03_task2a_modeling.ipynb` training cells. Show the calibration curve or metric outputs.
**Audio**: 
"For modeling, we relied on LightGBM. For Task 1's lateness probability, we noticed our raw classifier was overconfident. A key part of our architecture was applying Isotonic Regression to calibrate those probabilities, drastically reducing our Brier score to 0.040. For Task 2A's demand forecasting, we built a recursive time-series forecaster. We aggregated demand weekly and generated rolling 4-week lag features, heavily utilizing the calendar data to capture festival ramps and payday spikes."

## [2:30 - 3:30] Task 2B Peak-Day Allocation
**Visual**: Show `src/task2b_allocator.py` and run the `check_allocation.py` script in the terminal to show "FEASIBILITY: PASSED".
**Audio**: 
"Task 2B was an optimization challenge. When we analyzed Scenario 1, we found that 181 cubic meters of chilled demand had to fit into just 4 available reefer vehicles with only 86 cubic meters of capacity. It was mathematically impossible to serve everyone. 
We built a greedy bin-packing allocator that strictly protected outlets deferred yesterday, and packed vehicles while respecting all district and brand constraints. Our script deferred 14 orders—almost entirely chilled Fresh orders—because reefer capacity was the true bottleneck. As you can see, our allocation passes the official validation script with zero violations."

## [3:30 - 4:00] Conclusion & Output
**Visual**: Show the final inference cell in `BigBug_FinalNotebook.ipynb` loading models and making a prediction. Then show the file explorer with the ZIP file.
**Audio**: 
"Finally, our solution is fully reproducible. Our final notebook loads the saved models and can run inference on new data seamlessly. We've packaged all our CSV templates, documented our prioritization policy, and included our AI tool disclosure. Thank you for your time, and we look forward to the next stage of the Triathlon!"
