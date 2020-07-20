import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import patches


def affine_transform(t, points):
    points1 = []
    for x in points:
        v = np.array([0,0,1])
        v[:2] = x
        points1.append(np.dot(t, v)[:2])
    return points1

def init():
    print("Start")



body = np.array([[20,0],
               [162,0],
               [162,250],
               [20,250]])
wheel1 = np.array([[0,25],
                   [20,25],
                   [20,105],
                   [0,105]])
wheel2 = np.array([[162,25],
                   [182,25],
                   [182,105],
                   [162,105]])
wheel3 = np.array([[0,145],
                   [20,145],
                   [20,225],
                   [0,225]])
wheel4 = np.array([[162,145],
                   [182,145],
                   [182,225],
                   [162,225]])
bumper = np.array([[20,250],
                   [162,250],
                   [91,300]])


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
vl = n * [1]
vr = n * [2]


x, y, theta = 0, 0, np.pi/2
T = []
for i in range(n):
    T.append(np.array([[np.cos(theta-np.pi/2), -np.sin(theta-np.pi/2), x],
                       [np.sin(theta-np.pi/2), np.cos(theta-np.pi/2), y],
                       [0, 0, 1]]))
    v = (vl[i] + vr[i])/2
    omega = (-vl[i] + vr[i])/(2*R)
    x += v*np.cos(theta)*dt
    y += v*np.sin(theta)*dt
    theta += omega*dt
    

def animate(i):
    for obj in objs:
        obj.set_xy(affine_transform(T[i], obj.get_xy()))

anim = FuncAnimation(fig1, animate, init_func=init,
                               frames=50, interval=10, repeat = False, blit=False)



