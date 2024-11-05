import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.animation as animation

def sim_fifo_single_visual(num_periods=100, save_movie=True):
    # Adjustable parameters
    area_capacity1 = 92
    area_capacity2 = 166
    area_capacity3 = 170
    area_capacity4 = 226
    num_periods = num_periods
    save_movie = save_movie
    
    # Initialize storage areas (1,2,3,4) with capacity
    areas = {
        1: {'items': [], 'capacity': area_capacity1, 'pos': (0.2, 0.5)},
        2: {'items': [], 'capacity': area_capacity2, 'pos': (0.4, 0.5)},
        3: {'items': [], 'capacity': area_capacity3, 'pos': (0.6, 0.5)},
        4: {'items': [], 'capacity': area_capacity4, 'pos': (0.8, 0.5)}
    }
    
    # Initialize figure
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), height_ratios=[3, 1])
    fig.suptitle('Storage Area Simulation', fontsize=16)
    
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
    ax2.set_xlabel('Period')
    ax2.set_ylabel('Occupancy %')
    ax2.grid(True)
    
    # Initialize occupancy tracking
    occupancy_history = {i: [] for i in range(1, 5)}
    period_history = []
    
    # Create forklift representations with paths
    forklift1, = ax1.plot([], [], 'bo', markersize=10, label='Loading Forklift')
    forklift2, = ax1.plot([], [], 'ro', markersize=10, label='Unloading Forklift')
    
    # Create storage area representations
    text_labels = []  # Store text labels separately
    for area_num, area_data in areas.items():
        # Add storage area
        rect = plt.Rectangle(
            (area_data['pos'][0]-0.05, area_data['pos'][1]-0.1),
            0.1, 0.2, 
            fill=True,
            facecolor='green',
            alpha=0.3
        )
        ax1.add_patch(rect)
        
        # Add path lines for forklifts
        ax1.plot([0.1, area_data['pos'][0]], [0.8, 0.8], 'b--', alpha=0.3)  # Loading path
        ax1.plot([0.1, area_data['pos'][0]], [0.2, 0.2], 'r--', alpha=0.3)  # Unloading path
        
        # Add text labels and store reference
        text = ax1.text(area_data['pos'][0]-0.05, area_data['pos'][1]-0.15, 
                       f'Area {area_num}\n0/{area_data["capacity"]}\n(0%)', 
                       ha='center')
        text_labels.append(text)
    
    # Initialize occupancy lines
    lines = []
    for area_num in range(1, 5):
        line, = ax2.plot([], [], label=f'Area {area_num}')
        lines.append(line)
    
    # Animation update function
    def update(frame):
        # Adjustable parameters
        new_items = np.random.poisson(3)  # Reduced from 100 to 3
        items_to_remove = np.random.poisson(2)  # Reduced from 80 to 2
        # Process both operations simultaneously
        max_operations = max(new_items, items_to_remove)
        for _ in range(max_operations):
            # Simulate item removal (FIFO)
            if _ < items_to_remove:
                for area_num in range(1, 5):
                    if len(areas[area_num]['items']) > 0:
                        # Show forklift movement for removal
                        forklift2.set_data([0.1, areas[area_num]['pos'][0]], [0.2, 0.2])
                        areas[area_num]['items'].pop(0)
                        break
            
            # Process new storage
            if _ < new_items:
                for area_num, area_data in areas.items():
                    if len(area_data['items']) < area_data['capacity']:
                        # Show forklift movement for loading
                        forklift1.set_data([0.1, area_data['pos'][0]], [0.8, 0.8])
                        area_data['items'].append({
                            'timestamp': frame,
                            'item_id': f"item_{frame}_{_}"
                        })
                        break
        
        # Update area colors and occupancy rates
        for area_num, area_data in areas.items():
            occupancy = len(area_data['items']) / area_data['capacity']
            rect = ax1.patches[area_num-1]
            rect.set_facecolor(plt.cm.RdYlGn(1 - occupancy))
            rect.set_alpha(0.5)
            
            # Update text using stored text_labels
            text_labels[area_num-1].set_text(
                f'Area {area_num}\n{len(area_data["items"])}/{area_data["capacity"]}\n({occupancy*100:.1f}%)'
            )
            
            # Update occupancy history
            occupancy_history[area_num].append(occupancy * 100)
        
        period_history.append(frame)
        
        # Update occupancy graph
        for i, line in enumerate(lines):
            line.set_data(period_history, occupancy_history[i+1])
        
        return [forklift1, forklift2] + ax1.patches + lines + text_labels

    # Create animation with slower interval
    anim = animation.FuncAnimation(
        fig, update, frames=num_periods,
        interval=200,  # Increased from 50 to 200 (slower animation)
        blit=True
    )
    
    if save_movie:
        writer = animation.PillowWriter(
            fps=15,  # Reduced from 30 to 15 for slower playback
            metadata=dict(artist='Me'),
            bitrate=1800
        )
        anim.save('storage_simulation.gif', writer=writer)
        print("Animation saved as 'storage_simulation.gif'")
    
    plt.legend()
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

