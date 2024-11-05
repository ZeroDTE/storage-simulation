# Storage Area FIFO Simulation

A simulation of storage areas using FIFO (First In, First Out) principles. This project visualizes and analyzes the occupancy patterns of multiple storage areas with different capacities.

## Features
- Visual simulation of storage areas with animated forklifts
- FIFO-based item management
- Multiple simulation capabilities
- Real-time occupancy tracking
- Exportable animations

## Requirements
- Python 3.7+
- Dependencies listed in requirements.txt

## Installation
bash
git clone https://github.com/YOUR_USERNAME/storage-simulation.git
cd storage-simulation
pip install -r requirements.txt


## Usage
Run a single visual simulation:
python
from src.visualizer import sim_fifo_single_visual
sim_result = sim_fifo_single_visual(num_periods=200, save_movie=True)


##Run multiple simulations:
python
from src.simulation import simFIFO
results = simFIFO(num_simulations=10, num_periods=100)
