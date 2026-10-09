# System Architecture & Diagrams

## 1. High-Level Preprocessing & Modeling Pipeline

This diagram shows how raw CSV files are ingested, transformed into features, and fed into our models.

```mermaid
graph TD
    subgraph Data Sources
        DT(deliveries_train.csv)
        RL(route_legs_train.csv)
        CAL(calendar.csv)
        V(vehicles.csv)
        O(outlets.csv)
    end

    subgraph Preprocessing Module
        LC[Label Construction<br>service_time, is_late]
        FE1[Task 1 Features<br>37 variables]
        FE2[Task 2A Features<br>Lag & Calendar]
    end

    subgraph Modeling
        M1A(LightGBM Regressor<br>Service Time)
        M1B(LightGBM Classifier + Isotonic<br>Late Probability)
        M2(LightGBM Time-Series<br>Recursive Forecaster)
        M3(Greedy Allocator<br>Task 2B Constraint Solver)
    end

    subgraph Outputs
        S1[submission_task1.csv]
        S2[submission_task2a.csv]
        S3[submission_task2b.csv]
    end

    DT --> LC
    RL --> LC
    LC --> FE1
    CAL --> FE1
    V --> FE1
    O --> FE1
    
    FE1 --> M1A --> S1
    FE1 --> M1B --> S1
    
    DT --> FE2
    CAL --> FE2
    
    FE2 --> M2 --> S2
    
    O -.-> M3
    V -.-> M3
    M3 --> S3
```

## 2. Proposed Deployment Approach

For real-world Waypoint Group operations, this architecture proposes a daily batch-processing workflow orchestrated by Apache Airflow or AWS Step Functions.

```mermaid
sequenceDiagram
    participant WMS as Warehouse System
    participant Orchestrator as Batch Orchestrator
    participant Model as Inference Engine
    participant Allocator as Fleet Optimizer
    participant Dispatch as Dispatch System

    WMS->>Orchestrator: 4:00 PM: Daily order cutoff
    Orchestrator->>Model: Trigger Demand Forecast & Time Predictions
    Model-->>Orchestrator: Return predicted volumes and route timing
    Orchestrator->>Allocator: Pass confirmed orders & predicted constraints
    Allocator->>Allocator: Run constraint satisfaction (similar to Task 2B)
    Allocator-->>Orchestrator: Return optimal vehicle/trip allocations
    Orchestrator->>Dispatch: Send final manifest and routing instructions
```
