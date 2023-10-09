
# take the data and make some interesting visualizations...
# separate the data in some kinf of interesting way...
# just separate by the time steps, no agents...

import json
import numpy as np
import matplotlib.pyplot as plt
import random
import math

# preprocessing data
path = 'outputs/data_0007.json'

pos_array = []
with open(path) as f:
    data = json.load(f)
    for i in range(len(data["obs"])):
        step_array = []
        for agent in data["obs"][i]:
            pos_x = data["obs"][i][agent][0]
            pos_y = data["obs"][i][agent][1]
            pos_z = data["obs"][i][agent][2]
            step_array.append([pos_x, pos_y, pos_z])
        pos_array.append(step_array)
pos_array = np.array(pos_array)

# visualizing data
# fig = plt.figure(figsize=(16,9))
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

plt.xlim(-1, 16)
plt.ylim(-1, 16)
ax.set_zlim(-1, 16)

# pairs = []
# for i in range(1, pos_array.shape[0]-2): # step

#     # step index...
#         # as the numbers get higher, make more connections
#     num_steps, num_agents, _ = pos_array.shape
    
#     # desired visualization:
#         # longer connections further down the line...
#         # maybe these things are connected.. or the range that we can access is higher...



#     for _ in range(i):
#         future_step = min(i, num_steps)
#         step_index = math.floor(random.random() * (future_step - 1)) + 1
#         agent_index = math.floor(random.random() * num_agents)

#         ax.plot(
#             [pos_array[0, agent_index][0], pos_array[step_index,agent_index][0]],
#             [pos_array[0, agent_index][1], pos_array[step_index,agent_index][1]],
#             [pos_array[0, agent_index][2], pos_array[step_index,agent_index][2]],
#             alpha=0.5,
#         )

# --- lattice structures ---

# 301
# start_step, end_step = 200,250 # nice option
start_step, end_step = 250, 251 # nice lattice like structures
# start_step, end_step = 275, 280

num_steps, num_agents, _ = pos_array.shape
for i in range(num_agents): # loop through all pairs of agents
    for j in range(i, num_agents):
        for k in range(start_step, end_step): # loop through step range
            position_0 = np.array(pos_array[k, i])
            position_1 = np.array(pos_array[k, j])
            dist = np.linalg.norm(position_0 - position_1)
            if dist < 1.75:
                ax.plot(
                    [position_0[0], position_1[0]],
                    [position_0[1], position_1[1]],
                    [position_0[2], position_1[2]],
                    alpha=0.1,
                    color="red",
                )

plt.savefig(
    'visualizations_0.png',
    bbox_inches="tight", 
    dpi=300,
)

# plt.show()