import os
import json
import numpy as np

# convert data to obj file format

# --- data preprocessing ---
for i in range(1000): # get the last data file
    path = f"outputs/data_{i:04n}.json"
    if not os.path.isfile(path): 
        data_path = f"outputs/data_{i-1:04n}.json"
        break

pos_array = []
agent_list = []
with open(data_path) as f:
    data = json.load(f)
    for i in range(len(data["obs"])):
        step_array = []
        for agent in data["obs"][i]:
            agent_list.append(agent)
            pos_x = data["obs"][i][agent][0]
            pos_y = data["obs"][i][agent][1]
            pos_z = data["obs"][i][agent][2]
            step_array.append([pos_x, pos_y, pos_z])
        pos_array.append(step_array)
pos_array = np.array(pos_array)

print(f"\nsteps | agents | coordinates") # debugging information
print(f"{pos_array.shape}\n")


# --- writing data to obj format ---

for i in range(1000): # make a file name
    path = f"outputs/myobj_{i:04n}.obj"
    if not os.path.isfile(path): 
        file_path = f"outputs/myobj_{i:04n}.obj"
        break

file1 = open(file_path,"w") # open file

n0 = 125 # start step
nf = 150 # end step | max is 300
V = [] # vertices to write
L = [] # lines to write

coord_array = []

for i in range(pos_array.shape[1]): # iteration over each agent
    start = len(V) + 1
    for j in range(n0, nf): # iteration over each step
        coord = pos_array[j, i]
        V.append(f"v {coord[0]} {coord[1]} {coord[2]}\n")

        coord_array.append(coord)

    line = "l " # lines
    for j in range(n0, nf):
        index = j - n0
        if j == nf - 1: # stop check if at the end
            line += f"{start + index} "
            break
            
        # check coords
        coord0 = pos_array[j, i]
        coord1 = pos_array[j + 1, i]
        dist = np.linalg.norm(coord0 - coord1)
        line += f"{start + index} "
        if dist > 5:
            L.append(line + "\n")
            line = "l "    
    L.append(line + "\n")

# lattice structure
L = [] # clear previous lines
for i in range(len(coord_array)):
    coord0 = coord_array[i]
    line = f"l {i + 1} "
    print(f"{i} / {len(coord_array)}")
    for j in range(i, len(coord_array)):
        if i == j: continue
        # check distance
        coord1 = coord_array[j]
        dist = np.linalg.norm(coord0 - coord1)
        if dist < 0.5:
            line += f"{j + 1} "
    L.append(line + "\n")

file1.writelines(V)
file1.writelines(L)
file1.close() 