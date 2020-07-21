#! /usr/bin/env python
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import patches
from IPython import embed

def rotation_matrix(theta):
    return np.array([[np.cos(theta), -np.sin(theta)],
                     [np.sin(theta), np.cos(theta)]])


# Kinematics (simple differential drive model)   
T = 5 # Simulation time in s
dt = 0.1 # Simulation timestep in s
n = int(T/dt) 
L = 162 # Front axis length in mm
vl = n * [150] # Left wheel linear velocity in mm/s
vr = n * [200] # Right wheel linear velocity in mm/s
x, y, theta = 0, 0, 0
pv, thetav = [], []
for i in range(n):
    pv.append(np.array([x, y]))
    thetav.append(theta)
    v = (vl[i] + vr[i])/2
    omega = float(-vl[i] + vr[i])/L
    x -= v*np.sin(theta)*dt
    y += v*np.cos(theta)*dt
    theta += omega*dt


# Simulation (reference point is the midlle of the front axis)
body_points = np.array([[ -71, -185],
       [  71, -185],
       [  71,   65],
       [ -71,   65]])
wheel1_points = np.array([[ -91, -160],
       [ -71, -160],
       [ -71,  -80],
       [ -91,  -80]])
wheel2_points = np.array([[  71, -160],
       [  91, -160],
       [  91,  -80],
       [  71,  -80]])
wheel3_points = np.array([[-91, -40],
       [-71, -40],
       [-71,  40],
       [-91,  40]])
wheel4_points = np.array([[ 71, -40],
       [ 91, -40],
       [ 91,  40],
       [ 71,  40]])
bumper_points = np.array([[-71,  65],
       [ 71,  65],
       [  0, 115]])
points0 = [body_points, wheel1_points, wheel2_points, wheel3_points, wheel4_points, bumper_points]

plt.close()
fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal')
plt.axis([-1000,1000,-1000,1000])
plt.grid('on')
body_obj = ax.add_patch(patches.Polygon(body_points, color='gray'))
wheel1_obj = ax.add_patch(patches.Polygon(wheel1_points, color='goldenrod'))
wheel2_obj = ax.add_patch(patches.Polygon(wheel2_points, color='goldenrod'))
wheel3_obj = ax.add_patch(patches.Polygon(wheel3_points, color='goldenrod'))
wheel4_obj = ax.add_patch(patches.Polygon(wheel4_points, color='goldenrod'))
bumper_obj = ax.add_patch(patches.Polygon(bumper_points, color='gray'))
objs = [body_obj, wheel1_obj, wheel2_obj, wheel3_obj, wheel4_obj, bumper_obj]

def animate(i):
    for j in range(len(points0)):
        points = []
        for p in points0[j]:
            p1 = np.dot(rotation_matrix(thetav[i]), p) + pv[i]
            points.append(p1)
        objs[j].set_xy(points)

anim = FuncAnimation(fig, animate, frames=n, interval=dt*1000, repeat = False, blit=False)
plt.show(block = False)
embed()
exit(0)