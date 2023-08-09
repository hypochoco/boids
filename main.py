import multiprocessing as mp
from simulation import Simulation
import numpy as np

def dict_to_string(in_dict: dict, level: int = 0):
    output = "\n"
    space = ""
    for _ in range(level):
        space += "  "
    for key in in_dict:
        if type(in_dict[key]) is dict:
            output += f"{space}{key}: " + dict_to_string(in_dict[key], level + 1) + "\n"
        else:
            output += f"{space}{key}: {in_dict[key]} \n"
    return output

# debug info
print(f"cpu cores: {mp.cpu_count()}")
np.set_printoptions(formatter={'float': '{: 0.3f}'.format})

# play simulation
simulation = Simulation()
obs = simulation.reset()
done = False
print(f"obs: {dict_to_string(obs, 1)}")
while not done:
    obs, done = simulation.step()
    print(f"obs: {dict_to_string(obs, 1)}")

# save output to a file
simulation.save_simulation()

# animation
import animator