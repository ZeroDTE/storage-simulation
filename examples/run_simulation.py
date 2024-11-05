from src.simulation import simFIFO
from src.visualizer import sim_fifo_single_visual
import matplotlib.pyplot as plt

def main():
    # Run single visual simulation
    print("Running visual simulation...")
    sim_result = sim_fifo_single_visual(num_periods=200, save_movie=True)
    
    # Run multiple simulations
    print("\nRunning multiple simulations...")
    results = simFIFO(num_simulations=10, num_periods=100)
    
    # Plot results
    plt.figure(figsize=(12, 6))
    for sim in range(5):
        single_sim = results[results['simulation'] == sim]
        for area in range(1, 5):
            plt.plot(single_sim[f'area{area}_occupancy'], 
                    label=f'Simulation {sim} Area {area}')
    plt.xlabel('Period')
    plt.ylabel('Occupancy')
    plt.legend()
    plt.title('Storage Area Occupancy Over Time for Multiple Simulations')
    plt.show()

if __name__ == "__main__":
    main()