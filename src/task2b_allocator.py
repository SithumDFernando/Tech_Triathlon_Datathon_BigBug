import pandas as pd
import numpy as np
import os

def trip_time(district, brand, docks, dtravel, allowance):
    """Calculate trip time based on check_allocation.py logic."""
    d = dtravel[district]
    n = len(docks)
    if n == 0:
        return 0.0
    return (d["depot_to_district_freeflow_min"]
            + (n - 1) * d["inter_stop_freeflow_min"]
            + sum(allowance[(brand, dk)] for dk in docks))

def allocate_peak_day(scenario_path, fleet_path, vehicles_path, dtravel_path, allowance_path):
    # 1. Load Data
    orders = pd.read_csv(scenario_path)
    fleet = pd.read_csv(fleet_path)
    veh = pd.read_csv(vehicles_path).set_index("vehicle_id")
    dtravel = pd.read_csv(dtravel_path).set_index("district").to_dict("index")
    al = pd.read_csv(allowance_path)
    allowance = {(r.brand, r.dock_type): r.service_allowance_min for r in al.itertuples()}
    
    # 2. Filter available vehicles for Peliyagoda (S1 is Peliyagoda)
    avail_vids = fleet[fleet.status == 'available'].vehicle_id.values
    veh = veh.loc[veh.index.isin(avail_vids) & (veh.depot == 'Peliyagoda')].copy()
    
    # Initialize vehicle state
    v_state = {}
    for vid, row in veh.iterrows():
        v_state[vid] = {
            'type': row['type'],
            'temp': row['temp'],
            'vol_cap': row['volume_cap_m3'],
            'wt_cap': row['weight_cap_kg'],
            'trips': [], # list of dicts: {'brand': .., 'district': .., 'orders': [..], 'vol': 0, 'wt': 0, 'time': 0}
            'fresh_time': 0,
            'day_time': 0
        }
    
    # 3. Sort orders by Priority
    # Priority: deferred_yesterday (True first), days_since_last_served (Desc)
    # temp (chilled first), parking (van_only first), volume (Desc)
    orders['is_chilled'] = orders.temp_requirement == 'chilled'
    orders['is_van_only'] = orders.parking_constraint == 'van_only'
    orders = orders.sort_values(
        by=['deferred_yesterday', 'days_since_last_served', 'is_chilled', 'is_van_only', 'order_volume_m3'],
        ascending=[False, False, False, False, False]
    )
    
    allocations = [] # list of dict: order_ref -> {'decision', 'vehicle_id', 'trip_id'}
    
    # 4. Greedily assign orders
    for _, o in orders.iterrows():
        o_ref = o.order_ref
        brand = o.brand
        district = o.district
        vol = o.order_volume_m3
        wt = o.order_weight_kg
        dock = o.dock_type
        req_reefer = o.is_chilled
        req_van = o.is_van_only
        
        assigned = False
        
        # Try to add to existing trip first
        best_vid = None
        best_trip_idx = None
        best_score = -1
        
        # We prefer to add to a trip that leaves the vehicle with the least wasted space? 
        # Or just first valid trip. Let's just pick first valid trip to pack tightly.
        for vid, vs in v_state.items():
            if req_reefer and vs['temp'] != 'reefer': continue
            if req_van and vs['type'] != 'van': continue
            
            for t_idx, t in enumerate(vs['trips']):
                if t['brand'] == brand and t['district'] == district:
                    if t['vol'] + vol <= vs['vol_cap'] + 1e-6 and t['wt'] + wt <= vs['wt_cap'] + 1e-6:
                        # Check time budget
                        new_docks = [ord_obj.dock_type for ord_obj in t['orders']] + [dock]
                        new_trip_time = trip_time(district, brand, new_docks, dtravel, allowance)
                        time_diff = new_trip_time - t['time']
                        
                        if brand == 'Fresh':
                            if vs['fresh_time'] + time_diff <= 270 + 1e-6:
                                best_vid = vid
                                best_trip_idx = t_idx
                                break
                        else:
                            if vs['day_time'] + time_diff <= 480 + 1e-6:
                                best_vid = vid
                                best_trip_idx = t_idx
                                break
            if best_vid is not None:
                break
                
        if best_vid is not None:
            # Add to existing trip
            t = v_state[best_vid]['trips'][best_trip_idx]
            new_docks = [ord_obj.dock_type for ord_obj in t['orders']] + [dock]
            new_trip_time = trip_time(district, brand, new_docks, dtravel, allowance)
            time_diff = new_trip_time - t['time']
            
            t['orders'].append(o)
            t['vol'] += vol
            t['wt'] += wt
            t['time'] = new_trip_time
            if brand == 'Fresh':
                v_state[best_vid]['fresh_time'] += time_diff
            else:
                v_state[best_vid]['day_time'] += time_diff
                
            allocations.append({
                'scenario': 'S1', 'order_ref': o_ref, 'outlet_id': o.outlet_id,
                'decision': 'served', 'vehicle_id': best_vid, 'trip_id': best_trip_idx + 1
            })
            assigned = True
            continue
            
        # If couldn't add to existing, try to create a new trip
        # Score vehicles to prefer those with exact capabilities (don't waste reefer on ambient)
        best_vid = None
        best_score = 9999
        
        for vid, vs in v_state.items():
            if len(vs['trips']) >= 2: continue
            if req_reefer and vs['temp'] != 'reefer': continue
            if req_van and vs['type'] != 'van': continue
            if vol > vs['vol_cap'] + 1e-6 or wt > vs['wt_cap'] + 1e-6: continue
            
            # Check time
            new_trip_time = trip_time(district, brand, [dock], dtravel, allowance)
            if brand == 'Fresh':
                if vs['fresh_time'] + new_trip_time > 270 + 1e-6: continue
            else:
                if vs['day_time'] + new_trip_time > 480 + 1e-6: continue
                
            # Score: penalties for using over-capable vehicles
            penalty = 0
            if vs['temp'] == 'reefer' and not req_reefer: penalty += 100
            if vs['type'] == 'van' and not req_van: penalty += 100
            # Tie-breaker: prefer vehicles with less remaining capacity? Or more? 
            # Let's prefer larger vehicles to pack more into the new trip. So negative capacity.
            penalty -= vs['vol_cap']
            
            if penalty < best_score:
                best_score = penalty
                best_vid = vid
                
        if best_vid is not None:
            # Create new trip
            new_trip_time = trip_time(district, brand, [dock], dtravel, allowance)
            new_trip = {
                'brand': brand, 'district': district, 'orders': [o],
                'vol': vol, 'wt': wt, 'time': new_trip_time
            }
            v_state[best_vid]['trips'].append(new_trip)
            trip_idx = len(v_state[best_vid]['trips'])
            
            if brand == 'Fresh':
                v_state[best_vid]['fresh_time'] += new_trip_time
            else:
                v_state[best_vid]['day_time'] += new_trip_time
                
            allocations.append({
                'scenario': 'S1', 'order_ref': o_ref, 'outlet_id': o.outlet_id,
                'decision': 'served', 'vehicle_id': best_vid, 'trip_id': trip_idx
            })
            assigned = True
            
        if not assigned:
            # Defer
            allocations.append({
                'scenario': 'S1', 'order_ref': o_ref, 'outlet_id': o.outlet_id,
                'decision': 'deferred', 'vehicle_id': '', 'trip_id': ''
            })

    # Format output
    res = pd.DataFrame(allocations)
    return res

if __name__ == '__main__':
    res = allocate_peak_day(
        'data/raw/Test Data/task2b_peak_day_scenarios.csv',
        'data/raw/Test Data/task2b_peak_day_fleet.csv',
        'data/raw/General Data/vehicles.csv',
        'data/raw/General Data/district_travel.csv',
        'data/raw/General Data/service_allowance.csv'
    )
    
    print("Allocation Summary:")
    print(res.decision.value_counts())
    
    res.to_csv('data/raw/Submission Templates/submission_task2b.csv', index=False)
    print("Saved to submission_task2b.csv")
