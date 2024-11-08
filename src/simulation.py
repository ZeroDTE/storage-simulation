import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.animation as animation

def sim_fifo_single_visual(num_periods=100, 
                          num_loading_forklifts=3, 
                          num_unloading_forklifts=2, 
                          mean_trips_per_period=10,    
                          std_trips_per_period=2,      
                          mean_items_per_trip=5,       
                          std_items_per_trip=1,        
                          save_movie=True):
    # Adjustable parameters
    area_capacity1 = 92
    area_capacity2 = 166
    area_capacity3 = 170
    area_capacity4 = 226
    
    # Initialize storage areas (1,2,3,4) with capacity
    areas = {
        1: {'items': [], 'capacity': area_capacity1, 'pos': (0.2, 0.5)},
        2: {'items': [], 'capacity': area_capacity2, 'pos': (0.4, 0.5)},
        3: {'items': [], 'capacity': area_capacity3, 'pos': (0.6, 0.5)},
        4: {'items': [], 'capacity': area_capacity4, 'pos': (0.8, 0.5)}
    }
    
    # Initialize figure
    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(4, 1, height_ratios=[3, 1, 1, 1])
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])
    ax3 = fig.add_subplot(gs[2])
    ax4 = fig.add_subplot(gs[3])
    
    fig.suptitle('Storage Area Simulation with Multiple Forklifts', fontsize=16)
    
    # Setup main visualization area
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.set_xticks([])
    ax1.set_yticks([])
    
    # Add entry and exit points
    ax1.plot(0.1, 0.8, 'gs', markersize=15, label='Entry Point')
    ax1.plot(0.1, 0.2, 'rs', markersize=15, label='Exit Point')
    
    # Setup occupancy graph
    ax2.set_xlim(0, num_periods)
    ax2.set_ylim(0, 100)
    ax2.set_ylabel('Occupancy %')
    ax2.grid(True)
    
    # Setup forklift utilization graph
    ax3.set_xlim(0, num_periods)
    ax3.set_ylim(0, 100)
    ax3.set_xlabel('Period')
    ax3.set_ylabel('Forklift Utilization %')
    ax3.grid(True)
    
    # Setup parameter variation graph
    ax4.set_xlim(0, num_periods)
    ax4.set_ylim(0, max(mean_trips_per_period, mean_items_per_trip) * 2)
    ax4.set_xlabel('Period')
    ax4.set_ylabel('Parameters')
    ax4.grid(True)
    
    # Initialize storage area representations and their patches
    storage_patches = []
    text_labels = []
    for area_num, area_data in areas.items():
        # Create and store the rectangle patch
        rect = plt.Rectangle(
            (area_data['pos'][0]-0.05, area_data['pos'][1]-0.1),
            0.1, 0.2, 
            fill=True,
            facecolor='green',
            alpha=0.3,
            label=f'Area {area_num}'  # Add label to identify the area
        )
        ax1.add_patch(rect)
        storage_patches.append(rect)
        
        # Add path lines for forklifts
        ax1.plot([0.1, area_data['pos'][0]], [0.8, 0.8], 'b--', alpha=0.3)
        ax1.plot([0.1, area_data['pos'][0]], [0.2, 0.2], 'r--', alpha=0.3)
        
        # Create and store the text label
        text = ax1.text(area_data['pos'][0]-0.05, area_data['pos'][1]-0.15, 
                       f'Area {area_num}\n0/{area_data["capacity"]}\n(0%)', 
                       ha='center')
        text_labels.append(text)
    
    # Initialize tracking
    occupancy_history = {i: [] for i in range(1, 5)}
    loading_utilization_history = []
    unloading_utilization_history = []
    period_history = []
    trips_history = []
    items_per_trip_history = []
    
    # Create multiple forklift representations
    loading_forklifts = []
    unloading_forklifts = []
    
    for i in range(num_loading_forklifts):
        forklift, = ax1.plot([], [], 'bo', markersize=10, 
                            label=f'Loading Forklift {i+1}')
        loading_forklifts.append(forklift)
    
    for i in range(num_unloading_forklifts):
        forklift, = ax1.plot([], [], 'ro', markersize=10, 
                            label=f'Unloading Forklift {i+1}')
        unloading_forklifts.append(forklift)
    
    # Initialize lines for graphs with proper labels
    occupancy_lines = []
    for area_num in range(1, 5):
        line, = ax2.plot([], [], label=f'Area {area_num}')
        occupancy_lines.append(line)
    
    loading_util_line, = ax3.plot([], [], 'b-', label='Loading Forklifts')
    unloading_util_line, = ax3.plot([], [], 'r-', label='Unloading Forklifts')
    trips_line, = ax4.plot([], [], 'g-', label='Trips per Period')
    items_line, = ax4.plot([], [], 'y-', label='Items per Trip')

    def update(frame):
        # Generate random trips and items per trip
        trips_per_period = max(1, int(np.random.normal(mean_trips_per_period, std_trips_per_period)))
        items_per_trip = max(1, int(np.random.normal(mean_items_per_trip, std_items_per_trip)))
        
        # Remove loading capacity limitation
        loading_capacity_per_period = float('inf')  # No limitation for loading
        unloading_capacity_per_period = num_unloading_forklifts * trips_per_period * items_per_trip
        
        # Use Poisson distribution with mean of 22 ULDs per hour
        new_items = np.random.poisson(22)
        items_to_remove = np.random.poisson(20)
        
        active_loading_areas = []
        active_unloading_areas = []
        
        def find_next_available_area():
            for area_num in range(1, 5):
                if len(areas[area_num]['items']) < areas[area_num]['capacity']:
                    return area_num
            return None
        
        # Process removals - Modified to handle multiple areas with delays
        removed_items = 0
        if items_to_remove > 0:
            # Add random delays for unloading
            delay_probability = 0.3  # 30% chance of delay for each unloading operation
            processing_efficiency = np.random.uniform(0.6, 1.0)  # Random efficiency between 60-100%
            
            # Adjust items_to_remove based on processing efficiency
            actual_items_to_remove = int(items_to_remove * processing_efficiency)
            
            # Calculate items to remove from each non-empty area
            for area_num in range(1, 5):
                if len(areas[area_num]['items']) > 0:
                    # Apply random delays
                    if np.random.random() < delay_probability:
                        # Skip this area this period due to delay
                        continue
                        
                    area_items_to_remove = min(
                        actual_items_to_remove - removed_items,
                        len(areas[area_num]['items']),
                        int(unloading_capacity_per_period * processing_efficiency) // 4
                    )
                    
                    # Remove items and update visualization
                    for i in range(area_items_to_remove):
                        areas[area_num]['items'].pop(0)
                        removed_items += 1
                        
                        forklift_index = (removed_items // items_per_trip) % num_unloading_forklifts
                        if forklift_index < len(unloading_forklifts):
                            unloading_forklifts[forklift_index].set_data(
                                [0.1, areas[area_num]['pos'][0]], 
                                [0.2, 0.2]
                            )
                            if area_num not in active_unloading_areas:
                                active_unloading_areas.append(area_num)
                    
                    if removed_items >= actual_items_to_remove:
                        break
        
        # Process additions - Modified to ignore forklift capacity
        added_items = 0
        if new_items > 0:
            # Distribute new items across available areas without forklift limitations
            for area_num in range(1, 5):
                if len(areas[area_num]['items']) < areas[area_num]['capacity']:
                    space_available = areas[area_num]['capacity'] - len(areas[area_num]['items'])
                    area_items_to_add = min(
                        new_items - added_items,
                        space_available
                        # Removed the loading_capacity_per_period limitation
                    )
                    
                    # Add items and update visualization
                    for i in range(area_items_to_add):
                        areas[area_num]['items'].append({
                            'timestamp': frame,
                            'item_id': f"item_{frame}_{added_items}"
                        })
                        added_items += 1
                        
                        # Update forklift visualization (just for display)
                        forklift_index = (added_items % num_loading_forklifts)
                        if forklift_index < len(loading_forklifts):
                            loading_forklifts[forklift_index].set_data(
                                [0.1, areas[area_num]['pos'][0]], 
                                [0.8, 0.8]
                            )
                            if area_num not in active_loading_areas:
                                active_loading_areas.append(area_num)
                    
                    if added_items >= new_items:
                        break

        # Reset inactive forklifts
        for i in range(num_loading_forklifts):
            if i >= len(active_loading_areas):
                loading_forklifts[i].set_data([], [])

        for i in range(num_unloading_forklifts):
            if i >= len(active_unloading_areas):
                unloading_forklifts[i].set_data([], [])

        # Update area visualizations
        for area_num, area_data in areas.items():
            occupancy = len(area_data['items']) / area_data['capacity']
            
            # Update rectangle color
            storage_patches[area_num-1].set_facecolor(plt.cm.RdYlGn(max(0, 1 - occupancy)))
            storage_patches[area_num-1].set_alpha(0.5)
            
            # Update text label
            text_labels[area_num-1].set_text(
                f'Area {area_num}\n{len(area_data["items"])}/{area_data["capacity"]}\n({occupancy*100:.1f}%)'
            )
            
            # Update occupancy history
            occupancy_history[area_num].append(occupancy * 100)
        
        # Calculate and update utilization metrics
        loading_util = (len(active_loading_areas) / num_loading_forklifts) * 100
        unloading_util = (len(active_unloading_areas) / num_unloading_forklifts) * 100
        
        loading_utilization_history.append(loading_util)
        unloading_utilization_history.append(unloading_util)
        period_history.append(frame)
        trips_history.append(trips_per_period)
        items_per_trip_history.append(items_per_trip)
        
        # Update all graph lines
        for i, line in enumerate(occupancy_lines):
            line.set_data(period_history, occupancy_history[i+1])
        
        loading_util_line.set_data(period_history, loading_utilization_history)
        unloading_util_line.set_data(period_history, unloading_utilization_history)
        trips_line.set_data(period_history, trips_history)
        items_line.set_data(period_history, items_per_trip_history)
        
        # Update status text
        status_text = (f'Period: {frame}\n'
                      f'New Items: {new_items}\n'
                      f'Added: {added_items} (Capacity: {loading_capacity_per_period})\n'
                      f'Removals: {items_to_remove}\n'
                      f'Removed: {removed_items} (Capacity: {unloading_capacity_per_period})\n'
                      f'Active Area: {find_next_available_area()}\n'
                      f'Trips this period: {trips_per_period} (Mean: {mean_trips_per_period})\n'
                      f'Items per trip: {items_per_trip} (Mean: {mean_items_per_trip})')
        
        if hasattr(update, 'status_text'):
            update.status_text.remove()
        update.status_text = ax1.text(0.02, 0.98, status_text,
                                    transform=ax1.transAxes,
                                    verticalalignment='top',
                                    bbox=dict(boxstyle='round',
                                            facecolor='white',
                                            alpha=0.8))
        
        return (loading_forklifts + unloading_forklifts + storage_patches + 
                occupancy_lines + [loading_util_line, unloading_util_line] + 
                text_labels + [update.status_text] + [trips_line, items_line])

    # Create animation
    anim = animation.FuncAnimation(
        fig, update, frames=num_periods,
        interval=200,
        blit=True
    )
    
    if save_movie:
        writer = animation.PillowWriter(
            fps=15,
            metadata=dict(artist='Me'),
            bitrate=1800
        )
        anim.save('storage_simulation.gif', writer=writer)
        print("Animation saved as 'storage_simulation.gif'")
    
    # Add legends and show
    ax1.legend(loc='upper right')
    ax2.legend()
    ax3.legend()
    ax4.legend()
    plt.tight_layout()
    plt.show()
    
    return areas

def sim_fifo_single(num_periods=100):
    # Adjustable parameters
    area_capacity1 = 92
    area_capacity2 = 166
    area_capacity3 = 170
    area_capacity4 = 226
    num_periods = num_periods
    
    # Initialize storage areas (1,2,3,4) with capacity
    areas = {
        1: {'items': [], 'capacity': area_capacity1},
        2: {'items': [], 'capacity': area_capacity2},
        3: {'items': [], 'capacity': area_capacity3},
        4: {'items': [], 'capacity': area_capacity4}
    }
    
    # Track metrics
    results = []
    
    for period in range(num_periods):
        print(f"\nPeriod {period}:")
        print("Current Occupancy Rates:")
        for area_num in range(1, 5):
            occupancy = len(areas[area_num]['items'])
            capacity = areas[area_num]['capacity']
            occupancy_rate = (occupancy / capacity) * 100
            print(f"Area {area_num}: {occupancy}/{capacity} ({occupancy_rate:.1f}%)")
        
        # Simulate incoming shipments
        new_items = np.random.poisson(100)
        print(f"New items arriving: {new_items}")
        
        # Simulate item removal (FIFO)
        items_to_remove = np.random.poisson(80)
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
            stored = False
            for area_num in range(1, 5):
                if len(areas[area_num]['items']) < areas[area_num]['capacity']:
                    areas[area_num]['items'].append({
                        'timestamp': period,
                        'item_id': f"item_{period}_{_}"
                    })
                    items_stored[area_num] += 1
                    stored = True
                    break
        
        print("\nItems movement this period:")
        for area_num in range(1, 5):
            print(f"Area {area_num}: +{items_stored[area_num]} added, -{items_removed[area_num]} removed")
        
        # Record metrics for this period
        results.append({
            'period': period,
            'area1_occupancy': len(areas[1]['items']),
            'area2_occupancy': len(areas[2]['items']),
            'area3_occupancy': len(areas[3]['items']),
            'area4_occupancy': len(areas[4]['items'])
        })
    
    return pd.DataFrame(results)

def simFIFO(num_simulations=1000, num_periods=100):
    # Adjustable parameters
    num_simulations = num_simulations
    num_periods = num_periods
    
    sim_results = []
    for i in range(num_simulations):
        print(f"\nStarting simulation {i+1} of {num_simulations}")
        sim_df = sim_fifo_single(num_periods)
        sim_df['simulation'] = i
        sim_results.append(sim_df)
    
    return pd.concat(sim_results, ignore_index=True)
