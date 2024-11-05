import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def sim_fifo_single_visual(num_periods=100, save_movie=True):
    # Adjustable parameters
    area_capacity1, area_capacity2 = 92, 166
    area_capacity3, area_capacity4 = 170, 226
    
    # Initialize storage areas
    areas = {
        1: {'items': [], 'capacity': area_capacity1, 'pos': (0.2, 0.5)},
        2: {'items': [], 'capacity': area_capacity2, 'pos': (0.4, 0.5)},
        3: {'items': [], 'capacity': area_capacity3, 'pos': (0.6, 0.5)},
        4: {'items': [], 'capacity': area_capacity4, 'pos': (0.8, 0.5)}
    }
    
    # Setup visualization
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), height_ratios=[3, 1])
    fig.suptitle('Storage Area Simulation', fontsize=16)
    
    # ... [rest of the visualization setup code remains the same]
    
    def update(frame):
        # ... [animation update function remains the same]
        pass
    
    # Create and save animation
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
    
    plt.legend()
    plt.show()
    
    return areas

def plot_multiple_simulations(results, num_sims=5):
    """Plot results from multiple simulations."""
    plt.figure(figsize=(12, 6))
    for sim in range(num_sims):
        single_sim = results[results['simulation'] == sim]
        for area in range(1, 5):
            plt.plot(single_sim[f'area{area}_occupancy'], 
                    label=f'Simulation {sim} Area {area}')
    
    plt.xlabel('Period')
    plt.ylabel('Occupancy')
    plt.legend()
    plt.title('Storage Area Occupancy Over Time for Multiple Simulations')
    plt.show()