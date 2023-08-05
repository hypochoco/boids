import plotly.graph_objects as go
import numpy as np
import json

# reformat data
preprocessed_data = []
eps = 1e-8
with open('outputs/data.json') as f:
    data = json.load(f)
    for step in data:
        x, y, z, u, v, w = [], [], [], [], [], []
        for agent in step:
            agent_x, agent_y, agent_z = step[agent][0:3]
            agent_u, agent_v, agent_w = step[agent][3:6]
            norm = np.linalg.norm(np.array([agent_u, agent_v, agent_w]))
            if norm < eps: norm = np.array(1.)
            u_norm, v_norm, w_norm = [agent_u, agent_v, agent_w] / norm
            x.append(agent_x)
            y.append(agent_y)
            z.append(agent_z)
            u.append(u_norm)
            v.append(v_norm)
            w.append(w_norm)
        preprocessed_data.append({
            'x': x,
            'y': y,
            'z': z,
            'u': u,
            'v': v,
            'w': w,
        })

# animation 
frames = []
for i in range(len(preprocessed_data)):
    sub_fig = go.Cone(
        x=preprocessed_data[i]['x'],
        y=preprocessed_data[i]['y'],
        z=preprocessed_data[i]['z'],
        u=preprocessed_data[i]['u'],
        v=preprocessed_data[i]['v'],
        w=preprocessed_data[i]['w'],
        sizemode="absolute",
        sizeref=1,
    )

    if i == 0: first_fig = sub_fig
    frames.append(go.Frame(data=sub_fig, name=str(i)))

fig = go.Figure(frames=frames)
fig.add_trace(first_fig)
fig.update_layout(
    scene=dict(domain_x=[0, 1],
        camera_eye=dict(x=-1.57, y=1.36, z=0.58))
)

def frame_args(duration):
    return {
        "frame": {"duration": duration},
        "mode": "immediate",
        "fromcurrent": True,
        "transition": {"duration": duration, "easing": "linear"},
    }

sliders = [{
    "pad": {"b": 10, "t": 60},
    "len": 0.9,
    "x": 0.1,
    "y": 0,
    "steps": [
        {
            "args": [[f.name], frame_args(0)],
            "label": str(k),
            "method": "animate",
        }
        for k, f in enumerate(fig.frames)
    ],
}]

# Layout
fig.update_layout(
    title='Slices in volumetric data',
    width=600,
    height=600,
    scene=dict(
            zaxis=dict(range=[0, 5], autorange=False),
            xaxis=dict(range=[0, 5], autorange=False),
            yaxis=dict(range=[0, 5], autorange=False),
            aspectratio=dict(x=1, y=1, z=1),
            ),
    updatemenus = [{
        "buttons": [
            {
                "args": [None, frame_args(50)],
                "label": "&#9654;", # play symbol
                "method": "animate",
            },
            {
                "args": [[None], frame_args(0)],
                "label": "&#9724;", # pause symbol
                "method": "animate",
            },
        ],
        "direction": "left",
        "pad": {"r": 10, "t": 70},
        "type": "buttons",
        "x": 0.1,
        "y": 0,
    }],
    sliders=sliders
)

fig.show()





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


