import multiprocessing as mp
from simulation import Simulation
import numpy as np


# debug info
print(f"cpu cores: {mp.cpu_count()}")
np.set_printoptions(formatter={'float': '{: 0.3f}'.format})

# play simulation
simulation = Simulation()
obs = simulation.reset()
done = False
print(f"obs: {obs}\n")
while not done:
    obs, done = simulation.step()
    print(f"obs: {obs}\n")

# save output to a file
simulation.save_simulation()

# animation
import animator