#! /usr/bin/env python
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import patches

def rotation_matrix(theta):
  return np.array([[np.cos(theta), -np.sin(theta)],
                   [np.sin(theta), np.cos(theta)]])


# Kinematics (simple differential drive model)   
T = 3 # Simulation time in s
dt = 0.1 # Simulation timestep in s
n = int(T/dt) 
L = 130 # Front axis length in mm
vm_off = -280.0/3  # actual robot velocity offset in mm/s 
scale = 10    # mapping factor between motor speed and wheel linear velocity
NEG = True   # whether car motion in backward
vml = np.array(n * [40])  # left motor commanded speed (speed range: 20 - 100)
vmr = np.array(n * [40])  # right motor commanded speed (speed range: 20 - 100)
vl = np.add(vml*scale, n * [vm_off]) # Left wheel linear velocity in mm/s
vr = np.add(vmr*scale, n * [vm_off]) # Right wheel linear velocity in mm/s
if NEG:
  vl = -vl
  vr = -vr

x, y, theta = 0, 0, 0
pv, thetav = [], []
for i in range(n):
  pv.append(np.array([x, y]))
  thetav.append(theta)
  v = (vl[i] + vr[i])/2
  omega = float(-vml[i] + vmr[i])/L*3
  x -= v*np.sin(theta)*dt
  y += v*np.cos(theta)*dt
  theta += omega*dt


# Simulation (reference point is the center of the car)
body_points = np.array([[ -52, -105.5],
       [  52, -105.5],
       [  52,   105.5],
       [ -52,   105.5]])
wheel1_points = np.array([[ -80, -91],
       [ -52, -91],
       [ -52,  -24],
       [ -80,  -24]])
wheel2_points = np.array([[  52, -91],
       [  80, -91],
       [  80,  -24],
       [  52,  -24]])
wheel3_points = np.array([[-80, 24],
       [-52, 24],
       [-52,  91],
       [-80,  91]])
wheel4_points = np.array([[ 52, 24],
       [ 80, 24],
       [ 80,  91],
       [ 52,  91]])
bumper_points = np.array([[-52,  105.5],
       [ 52,  105.5],
       [  0, 145.5]])
points0 = [body_points, wheel1_points, wheel2_points, wheel3_points, wheel4_points, bumper_points]

plt.close()
fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal')
plt.axis([-2000,2000,-2000,2000])
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
plt.ion()
plt.show()
