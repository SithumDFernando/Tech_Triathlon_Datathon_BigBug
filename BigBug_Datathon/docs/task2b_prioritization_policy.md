# Task 2B: Peak-Day Prioritization Policy

## Scenario S1 Overview
On the peak day, demand spikes due to an upcoming festival, particularly for Fresh (chilled) goods. The fleet is operating under restricted availability due to several vehicles being in the workshop. All operations focus on the Peliyagoda depot.

## Bottleneck Identification
The limiting factor (bottleneck) on this day is **Refrigerated (Reefer) Vehicle Capacity**.
- **Chilled Demand**: There is a massive spike in chilled orders totaling **181.6 m³** across 26 orders.
- **Available Capacity**: Only 4 reefer vehicles (3 trucks, 1 van) are available at Peliyagoda, yielding a total volumetric capacity of **86.2 m³** per trip.
- Even running the maximum of 2 trips per vehicle, the theoretical maximum chilled volume capacity is **172.4 m³**. 
- Because of routing inefficiencies (district/brand segregation rules) and the strict 270-minute morning time budget for Fresh deliveries, achieving perfect packing is impossible. 

## Calculations & Algorithm
We implemented a bin-packing heuristic allocator that strictly adheres to the provided constraints (district segregation, volume/weight capacities, temp requirements, access restrictions, and time budgets). 
1. **Scoring**: Orders are scored based on the urgency of delivery.
2. **Prioritization Order**: 
   - `deferred_yesterday == 1` (Highest priority)
   - `days_since_last_served` (Descending)
   - `temp_requirement == chilled` (To prioritize utilizing specialized reefer vehicles)
   - `parking_constraint == van_only` (To prioritize utilizing scarce vans)
   - `order_volume_m3` (Descending, to pack large orders first)
3. **Allocation**: Vehicles were selected by minimizing the "waste" of specialized capabilities (e.g., preventing a reefer truck from being assigned an ambient order if an ambient truck was available). 

## Deferrals Analysis
In total, **14 orders** were deferred out of 85. 

### Unavoidable vs. Chosen Deferrals
- **Unavoidable**: 13 of the 14 deferred orders were Fresh (chilled). These deferrals were mathematically unavoidable because total chilled demand (181.6 m³) exceeded the maximum possible fleet capacity (172.4 m³), even assuming perfect packing. The remaining 1 Style ambient order was deferred due to tight district grouping restrictions and routing time budgets.
- **Chosen**: To decide *which* chilled orders to defer, we explicitly chose orders where `deferred_yesterday == 0`. Every single deferred order had been served successfully the previous day. Additionally, we favored deferring orders with lower `days_since_last_served`.

## Cost of Deferrals (Impact on Outlets)
Because we protected outlets that experienced a deferral the prior day, the impact is spread out. No single outlet will suffer back-to-back stockouts. However, because Fresh orders contain daily perishables (meat, dairy, produce), deferring these orders limits the fresh stock available at those 13 outlets for the day, which could lead to minor lost sales in those categories during the festival ramp-up.
