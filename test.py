
# the bounds aren't working because directions matter..

# they gotta face the same or different?

# --- fix static collisions ---

from structs import Bounds, Vector3
import numpy as np
import matplotlib.pyplot as plt

def _ray_plane_collision(
    pos_0: Vector3, 
    pos_f: Vector3, 
    normal: Vector3,
    point_on_plane: Vector3
):
    eps = 1e-8
    ray_dir = pos_f - pos_0
    denom = normal.dot(ray_dir)
    if np.abs(denom) < eps: # vectors are perpendicular
        return 0 if np.abs((pos_0 - point_on_plane).dot(normal)) < eps else np.inf
    numer = normal.dot(point_on_plane - pos_0)
    return numer / denom



# params...
pos_0 = Vector3(0.5, 0.5, 0.5)
pos_f = pos_0 + Vector3(0, 0, 1)
normal = Vector3(0, 0.1, 1)
point_on_plane = Vector3(-0.75, -0.75, 0.75)

t = _ray_plane_collision(pos_0, pos_f, normal, point_on_plane)
print(t)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter( # init point
    pos_0.tolist()[0],
    pos_0.tolist()[1],
    pos_0.tolist()[2],
    marker='o',
    color='green'
)
ax.scatter( # point on plane
    point_on_plane.tolist()[0],
    point_on_plane.tolist()[1],
    point_on_plane.tolist()[2],
    marker='o',
    color='red'
)
ax.plot( # line
    [0, normal.tolist()[0]],
    [0, normal.tolist()[1]],
    [0, normal.tolist()[2]],
    color='red'
)
ax.plot( # line
    [pos_0.tolist()[0], pos_f.tolist()[0]],
    [pos_0.tolist()[1], pos_f.tolist()[1]],
    [pos_0.tolist()[2], pos_f.tolist()[2]],
)
hit_point = (pos_f - pos_0) * t + pos_0
ax.scatter( # collision point
    hit_point.tolist()[0],
    hit_point.tolist()[1],
    hit_point.tolist()[2],
    marker='^'
)

plt.show()






# --- fix directions code ---

# from structs import Vector3
# import numpy as np
# import math
# import matplotlib.pyplot as plt

# dir = Vector3(1, 0, 1).normalized()

# index = np.argmax(np.abs(dir.tolist()))

# if index == 0:
#     perp_1 = Vector3(-(dir.z + dir.y) / dir.x, 1, 1).normalized()
# elif index == 1:
#     perp_1 = Vector3(1, -(dir.x + dir.z) / dir.y, 1).normalized()
# else:
#     perp_1 = Vector3(1, 1, -(dir.x + dir.y) / dir.z).normalized()

# perp_2 = dir.cross(perp_1)


# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')

# x, y, z = [], [], []
# for magnitude in np.arange(0.1, 1, 0.1):
#     for theta in np.arange(0.25, 2 * math.pi, 0.25): 

#         # TODO: flip this so it goes inside out...
#         # TODO: also figure out a better madnitude method??? too densely packed in the middle...
#         # just don't even normalize...

#         # what is the actual calculation of getting the point...
#         # we need the total mag to be 1... so we could just get mag and add the component...

#         comp_1 = perp_1 * math.cos(theta) * magnitude
#         comp_2 = perp_2 * math.sin(theta) * magnitude

#         r = perp_1.magnitude() * magnitude
#         comp_3_mag = math.sqrt(1 - r**2)

#         comp_3 = dir.normalized() * comp_3_mag

#         new_dir = comp_1 + comp_2 + comp_3

#         x.append(new_dir.tolist()[0])
#         y.append(new_dir.tolist()[1])
#         z.append(new_dir.tolist()[2])

# ax.scatter(x, y, z, color='blue')

# ax.plot(
#     [0, dir.tolist()[0]], 
#     [0, dir.tolist()[1]], 
#     [0, dir.tolist()[2]], 
#     color='green'
# )
# ax.plot(
#     [0, perp_1.tolist()[0]], 
#     [0, perp_1.tolist()[1]], 
#     [0, perp_1.tolist()[2]], 
#     color='red'
# )
# ax.plot(
#     [0, perp_2.tolist()[0]], 
#     [0, perp_2.tolist()[1]], 
#     [0, perp_2.tolist()[2]], 
#     color='red'
# )

# plt.xlim([-1, 1])
# plt.ylim([-1, 1])
# ax.set_zlim([-1, 1])

# plt.savefig(
#     'directions.png',
#     bbox_inches="tight", 
#     dpi=300,
# )

# plt.show()


# for magnitude in np.arange(0.1, 10.0, 0.1):
#     for theta in np.arange(0., 2 * math.pi, 0.1):
#         new_dir = perp_1 * magnitude * math.cos(theta) + \
#             perp_2 * magnitude * math.sin(theta) + vel
#         new_dir = new_dir.normalized() * vel_magnitude
#         directions.append(new_dir)


# --- run the simulation --- 

# from simulation import Simulation
# simulation = Simulation()
# simulation.reset()