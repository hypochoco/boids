# take the stuff and convert it into obj files...

# what are some of the things that have to be done here... 

from visualizations import visualize

# get data
vertices_dict, edges = visualize()

# sort vertices
def sorting_func(e):
    return e[1]
data = list(vertices_dict.items())
data.sort(key=sorting_func)

# write to obj file
with open("object.obj", "w") as f:
    for item in data:

        position = item[0].split()
        if position[0] == "" or position[0] == "[":
            position.pop(0)
        if position[0][0] == "[":
            position[0] = position[0].replace("[", "")
        position[-1] = position[-1].replace("]", "")

        f.write(f"v {position[0]} {position[1]} {position[2]}\n")

    for edge in edges:
        f.write(f"l {edge[0] + 1} {edge[1] + 1}\n")