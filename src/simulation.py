import numpy as np
import pandas as pd

def sim_fifo_single(num_periods=100):
    # Adjustable parameters
    area_capacity1 = 92
    area_capacity2 = 166
    area_capacity3 = 170
    area_capacity4 = 226
    
    # Initialize storage areas
    areas = {
        1: {'items': [], 'capacity': area_capacity1},
        2: {'items': [], 'capacity': area_capacity2},
        3: {'items': [], 'capacity': area_capacity3},
        4: {'items': [], 'capacity': area_capacity4}
    }
    
    # Track metrics
    results = []
    
    for period in range(num_periods):
        # Simulate incoming and outgoing items
        new_items = np.random.poisson(100)
        items_to_remove = np.random.poisson(80)
        
        # Process removals (FIFO)
        items_removed = {1: 0, 2: 0, 3: 0, 4: 0}
        for _ in range(items_to_remove):
            for area_num in range(1, 5):
                if len(areas[area_num]['items']) > 0:
                    areas[area_num]['items'].pop(0)
                    items_removed[area_num] += 1
                    break
        
        # Process storage
        items_stored = {1: 0, 2: 0, 3: 0, 4: 0}
        for _ in range(new_items):
            for area_num in range(1, 5):
                if len(areas[area_num]['items']) < areas[area_num]['capacity']:
                    areas[area_num]['items'].append({
                        'timestamp': period,
                        'item_id': f"item_{period}_{_}"
                    })
                    items_stored[area_num] += 1
                    break
        
        # Record metrics
        results.append({
            'period': period,
            'area1_occupancy': len(areas[1]['items']),
            'area2_occupancy': len(areas[2]['items']),
            'area3_occupancy': len(areas[3]['items']),
            'area4_occupancy': len(areas[4]['items'])
        })
    
    return pd.DataFrame(results)

def simFIFO(num_simulations=1000, num_periods=100):
    sim_results = []
    for i in range(num_simulations):
        sim_df = sim_fifo_single(num_periods)
        sim_df['simulation'] = i
        sim_results.append(sim_df)
    
    return pd.concat(sim_results, ignore_index=True)