import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import patches


def init():
    print("Start")


p0 = np.array([91, 185])
theta0 = 0
body = np.array([[20,0],
               [162,0],
               [162,250],
               [20,250]]) - p0
wheel1 = np.array([[0,25],
                   [20,25],
                   [20,105],
                   [0,105]]) - p0
wheel2 = np.array([[162,25],
                   [182,25],
                   [182,105],
                   [162,105]]) - p0
wheel3 = np.array([[0,145],
                   [20,145],
                   [20,225],
                   [0,225]]) - p0
wheel4 = np.array([[162,145],
                   [182,145],
                   [182,225],
                   [162,225]]) - p0
bumper = np.array([[20,250],
                   [162,250],
                   [91,300]]) - p0

points0 = [body, wheel1, wheel2, wheel3, wheel4, bumper]


plt.close()
fig1 = plt.figure()
ax1 = fig1.add_subplot(111, aspect='equal')
plt.axis([-1000,1000,-1000,1000])
plt.grid('on')

body_obj = ax1.add_patch(patches.Polygon(body, color='gray'))
wheel1_obj = ax1.add_patch(patches.Polygon(wheel1, color='goldenrod'))
wheel2_obj = ax1.add_patch(patches.Polygon(wheel2, color='goldenrod'))
wheel3_obj = ax1.add_patch(patches.Polygon(wheel3, color='goldenrod'))
wheel4_obj = ax1.add_patch(patches.Polygon(wheel4, color='goldenrod'))
bumper_obj = ax1.add_patch(patches.Polygon(bumper, color='gray'))
objs = [body_obj, wheel1_obj, wheel2_obj, wheel3_obj, wheel4_obj, bumper_obj]

n = 1000
dt = 0.1
R = 100
vl = n * [150]
vr = n * [200]

x, y, theta = 0, 0, theta0
pv, thetav = [], []
for i in range(n):
    pv.append(np.array([x, y]))
    thetav.append(theta)
    v = (vl[i] + vr[i])/2
    omega = (-vl[i] + vr[i])/(2*R)
    x -= v*np.sin(theta)*dt
    y += v*np.cos(theta)*dt
    theta += omega*dt

def rotation_matrix(theta):
    return np.array([[np.cos(theta), -np.sin(theta)],
                     [np.sin(theta), np.cos(theta)]])

def animate(i):
    for j in range(len(points0)):
        points = []
        for p in points0[j]:
            p1 = np.dot(rotation_matrix(thetav[i]), p) + pv[i]
            points.append(p1)
        objs[j].set_xy(points)

anim = FuncAnimation(fig1, animate, init_func=init,
                               frames=50, interval=10, repeat = False, blit=False)



