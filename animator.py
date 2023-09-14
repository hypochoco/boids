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

for i in range(1000):
    path = f"outputs/data_{i:04n}.json"
    if not os.path.isfile(path): 
        data_path = f"outputs/data_{i-1:04n}.json"
        break

pos_dict = {}
with open(data_path) as f:
    data = json.load(f)
    for i in range(len(data["obs"])):
        for agent in data["obs"][i]:
            if agent not in pos_dict.keys():
                pos_dict[agent] = {
                    "x": [],
                    "y": [],
                    "z": [],
                }
            pos_x = data["obs"][i][agent][0]
            pos_y = data["obs"][i][agent][1]
            pos_z = data["obs"][i][agent][2]
            pos_dict[agent]["x"].append(pos_x)
            pos_dict[agent]["y"].append(pos_y)
            pos_dict[agent]["z"].append(pos_z)

path_dict = {}
marker_dict = {}
for agent in pos_dict:
    path, = ax.plot([], [], [], linestyle='--', linewidth=1) 
    # marker, = ax.plot([], [], [], marker='o', markersize=1) 
    marker, = ax.plot([], [], [], marker='o', markersize=2) 
    path_dict[agent] = path
    marker_dict[agent] = marker

def run(i):
    out_tuple = []
    for agent in pos_dict:
        path = path_dict[agent]
        marker = marker_dict[agent]
        
        # path.set_data(pos_dict[agent]["x"][0:i], pos_dict[agent]["y"][0:i])
        # path.set_3d_properties(pos_dict[agent]["z"][0:i])

        marker.set_data(pos_dict[agent]["x"][i], pos_dict[agent]["y"][i])
        marker.set_3d_properties(pos_dict[agent]["z"][i])

        out_tuple.append(path)
        out_tuple.append(marker)

    return tuple(out_tuple)
   
anim = FuncAnimation(
    fig, 
    run,
    save_count=len(pos_dict[agent]["x"]),
    # frames=20, # fps 
    interval=50, # micro seconds per interval
    blit = True
)

index = 0
for i in range(1000):
    path = f"outputs/animation_{i:04n}.mp4"
    if not os.path.isfile(path): break
anim.save(path, writer='ffmpeg', dpi=300)


# # --- matplotlib ---

# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')
# col_x, col_y, col_z = [], [], []

# pos_dict = {}

# with open('outputs/data.json') as f:
#     data = json.load(f)

#     for i in range(len(data["obs"])):
#         for agent in data["obs"][i]:
#             if agent not in pos_dict.keys():
#                 pos_dict[agent] = {
#                     "x": [],
#                     "y": [],
#                     "z": [],
#                 }
#             pos_x = data["obs"][i][agent][0]
#             pos_y = data["obs"][i][agent][1]
#             pos_z = data["obs"][i][agent][2]
#             pos_dict[agent]["x"].append(pos_x)
#             pos_dict[agent]["y"].append(pos_y)
#             pos_dict[agent]["z"].append(pos_z)
#             # if i == 0: continue
#             # acc_x = data["acceleration"][i-1][agent][0]
#             # acc_y = data["acceleration"][i-1][agent][1]
#             # acc_z = data["acceleration"][i-1][agent][2]
#             # dir_x = [pos_x, pos_x + acc_x]
#             # dir_y = [pos_y, pos_y + acc_y]
#             # dir_z = [pos_z, pos_z + acc_z]
#             # ax.plot(dir_x, dir_y, dir_z, color='red')

#     for step in data["collisions"]:
#         for agent in step:
#             col_x.append(step[agent][0])
#             col_y.append(step[agent][1])
#             col_z.append(step[agent][2])

# for agent in pos_dict:
#     ax.scatter(
#         pos_dict[agent]["x"], 
#         pos_dict[agent]["y"], 
#         pos_dict[agent]["z"],
#         marker='o'
#     )
# ax.scatter(col_x, col_y, col_z, marker='^')

# # plt.xlim(0, 5)
# # plt.ylim(0, 5)
# # ax.set_zlim(0, 5)

# plt.show()


# # --- plotly ---

# # reformat data
# preprocessed_data = []
# eps = 1e-4
# with open('outputs/data.json') as f:
#     data = json.load(f)
#     for step in data:
#         x, y, z, u, v, w = [], [], [], [], [], []
#         for agent in step:
#             agent_x, agent_y, agent_z = step[agent][0:3]
#             agent_u, agent_v, agent_w = step[agent][3:6]

#             norm = np.linalg.norm(np.array([agent_u, agent_v, agent_w]))
#             if norm < eps:
#                 u_norm, v_norm, w_norm = [0.57, 0.57, 0.57]
#             else:
#                 u_norm, v_norm, w_norm = [agent_u, agent_v, agent_w] / norm

#             x.append(agent_x)
#             y.append(agent_y)
#             z.append(agent_z)
#             u.append(u_norm)
#             v.append(v_norm)
#             w.append(w_norm)
#         preprocessed_data.append({
#             'x': x,
#             'y': y,
#             'z': z,
#             'u': u,
#             'v': v,
#             'w': w,
#         })

# # animation 
# frames = []
# for i in range(len(preprocessed_data)):
#     sub_fig = go.Cone(
#         x=preprocessed_data[i]['x'],
#         y=preprocessed_data[i]['y'],
#         z=preprocessed_data[i]['z'],
#         u=preprocessed_data[i]['u'],
#         v=preprocessed_data[i]['v'],
#         w=preprocessed_data[i]['w'],
#         sizemode="absolute",
#         sizeref=10,
#     )
#     if i == 0: first_fig = sub_fig
#     frames.append(go.Frame(data=sub_fig, name=str(i)))

# fig = go.Figure(frames=frames)
# fig.add_trace(first_fig)
# fig.update_layout(
#     scene=dict(domain_x=[0, 1],
#         camera_eye=dict(x=-1.57, y=1.36, z=0.58))
# )

# def frame_args(duration):
#     return {
#         "frame": {"duration": duration},
#         "mode": "immediate",
#         "fromcurrent": True,
#         "transition": {"duration": duration, "easing": "linear"},
#     }

# sliders = [{
#     "pad": {"b": 10, "t": 60},
#     "len": 0.9,
#     "x": 0.1,
#     "y": 0,
#     "steps": [
#         {
#             "args": [[f.name], frame_args(0)],
#             "label": str(k),
#             "method": "animate",
#         }
#         for k, f in enumerate(fig.frames)
#     ],
# }]

# # Layout
# fig.update_layout(
#     title='Boids',
#     width=600,
#     height=600,
#     scene=dict(
#             zaxis=dict(range=[-2, 60], autorange=False),
#             xaxis=dict(range=[-2, 60], autorange=False),
#             yaxis=dict(range=[-2, 60], autorange=False),
#             aspectratio=dict(x=1, y=1, z=1),
#             ),
#     updatemenus = [{
#         "buttons": [
#             {
#                 "args": [None, frame_args(50)],
#                 "label": "&#9654;", # play symbol
#                 "method": "animate",
#             },
#             {
#                 "args": [[None], frame_args(0)],
#                 "label": "&#9724;", # pause symbol
#                 "method": "animate",
#             },
#         ],
#         "direction": "left",
#         "pad": {"r": 10, "t": 70},
#         "type": "buttons",
#         "x": 0.1,
#         "y": 0,
#     }],
#     sliders=sliders
# )

# # hiding color-bar 
# fig.update_coloraxes(showscale=False)

# fig.show()





# from dash import Dash, dcc, html, Input, Output
# import plotly.express as px

# app = Dash(__name__)


# app.layout = html.Div([
#     html.H4('Animated GDP and population over decades'),
#     html.P("Select an animation:"),
#     dcc.RadioItems(
#         id='selection',
#         options=["GDP - Scatter", "Population - Bar", "test"],
#         value='GDP - Scatter',
#     ),
#     dcc.Loading(dcc.Graph(id="graph"), type="cube")
# ])

# data = {
#     "test-x": [1,2,3,4,5],
#     "test-y": [1,2,3,4,5],
#     "test-f": [1,2,3,4,5],
#     "test-g": [1,2,3,4,5],
# }


# @app.callback(
#     Output("graph", "figure"), 
#     Input("selection", "value"))
# def display_animated_graph(selection):
#     df = px.data.gapminder() # replace with your own data source
#     # data = ...
#     animations = {
#         'GDP - Scatter': px.scatter(
#             df, x="gdpPercap", y="lifeExp", animation_frame="year", 
#             animation_group="country", size="pop", color="continent", 
#             hover_name="country", log_x=True, size_max=55, 
#             range_x=[100,100000], range_y=[25,90]),
#         'Population - Bar': px.bar(
#             df, x="continent", y="pop", color="continent", 
#             animation_frame="year", animation_group="country", 
#             range_y=[0,4000000000]),
#         'test': px.scatter(
#             data, x='test-x', y='test-y', animation_frame='test-f', animation_group='test-g',
#             range_x=[0, 5], range_y=[0, 5]
#         )
#     }
#     return animations[selection]


# app.run_server(debug=True)
# # app.run_server(debug=False)


