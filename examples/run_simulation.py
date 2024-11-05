from src.simulation import simFIFO
from src.visualizer import sim_fifo_single_visual, plot_multiple_simulations

def main():
    # Run single visual simulation
    print("Running visual simulation...")
    sim_result = sim_fifo_single_visual(num_periods=200, save_movie=True)
    
    # Run multiple simulations
    print("\nRunning multiple simulations...")
    results = simFIFO(num_simulations=10, num_periods=100)
    
    # Plot results
    plot_multiple_simulations(results)

if __name__ == "__main__":
    main()