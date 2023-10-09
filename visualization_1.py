import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation 
import os

plt.rcParams['animation.ffmpeg_path'] = 'ffmpeg/bin/ffmpeg.exe'


# --- matplotlib animation ---

fig = plt.figure(figsize=(16,9))
ax = fig.add_subplot(projection='3d')

plt.xlim(-1, 16)
plt.ylim(-1, 16)
ax.set_zlim(-1, 16)

ax.scatter(0, 0, 0, marker="^", s=1, color="red")
ax.scatter(15, 0, 0, marker="^", s=1, color="red")
ax.scatter(0, 15, 0, marker="^", s=1, color="red")
ax.scatter(0, 0, 15, marker="^", s=1, color="red")

ax.scatter(15, 15, 0, marker="^", s=1, color="red")
ax.scatter(15, 0, 15, marker="^", s=1, color="red")
ax.scatter(0, 15, 15, marker="^", s=1, color="red")
ax.scatter(15, 15, 15, marker="^", s=1, color="red")

for i in range(1000): # get the last data file
    path = f"outputs/data_{i:04n}.json"
    if not os.path.isfile(path): 
        data_path = f"outputs/data_{i-1:04n}.json"
        break

# pos_dict = {}
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

    # data = json.load(f)
    # for i in range(len(data["obs"])):
    #     for agent in data["obs"][i]:
    #         if agent not in pos_dict.keys():
    #             pos_dict[agent] = {
    #                 "x": [],
    #                 "y": [],
    #                 "z": [],
    #             }
    #         pos_x = data["obs"][i][agent][0]
    #         pos_y = data["obs"][i][agent][1]
    #         pos_z = data["obs"][i][agent][2]
    #         pos_dict[agent]["x"].append(pos_x)
    #         pos_dict[agent]["y"].append(pos_y)
    #         pos_dict[agent]["z"].append(pos_z)

path_dict = {}
marker_dict = {}
for agent in agent_list:
    path, = ax.plot([], [], [], linestyle='--', linewidth=1) 
    # marker, = ax.plot([], [], [], marker='o', markersize=1) 
    marker, = ax.plot([], [], [], marker='o', markersize=2) 
    path_dict[agent] = path
    marker_dict[agent] = marker

num_agents = len(agent_list)

def run(k):
    out_tuple = []
    for i in range(num_agents): # loop through all pairs of agents
        for j in range(i, num_agents):
            
            if k > 250: return

            position_0 = np.array(pos_array[k, i])
            position_1 = np.array(pos_array[k, j])
            dist = np.linalg.norm(position_0 - position_1)
            if dist < 1.75:
                path = path_dict[agent_list[i]]
                path.set_data([position_0[0], position_1[0]], [position_0[1], position_1[1]])
                path.set_3d_properties([position_0[2], position_1[2]])
                out_tuple.append(path)
                # ax.plot(
                #     [position_0[0], position_1[0]],
                #     [position_0[1], position_1[1]],
                #     [position_0[2], position_1[2]],
                #     alpha=0.1,
                #     color="red",
                # )
    return tuple(out_tuple)

    # out_tuple = []
    # for agent in pos_dict:
    #     path = path_dict[agent]
    #     marker = marker_dict[agent]
        
    #     # path.set_data(pos_dict[agent]["x"][0:i], pos_dict[agent]["y"][0:i])
    #     # path.set_3d_properties(pos_dict[agent]["z"][0:i])

    #     marker.set_data(pos_dict[agent]["x"][i], pos_dict[agent]["y"][i])
    #     marker.set_3d_properties(pos_dict[agent]["z"][i])

    #     out_tuple.append(path)
    #     out_tuple.append(marker)

    # return tuple(out_tuple)
   

anim = FuncAnimation(
    fig, 
    run,
    save_count=225,
    # frames=20, # fps 
    interval=50, # micro seconds per interval
    blit = True
)

index = 0
for i in range(1000):
    path = f"outputs/animation_{i:04n}.mp4"
    if not os.path.isfile(path): break
anim.save(path, writer='ffmpeg', dpi=300)