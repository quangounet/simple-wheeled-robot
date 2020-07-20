import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import patches
from matplotlib import transforms
from time import sleep


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
plt.axis([0,1000,0,1000])

body_obj = ax1.add_patch(patches.Polygon(body, color='gray'))
wheel1_obj = ax1.add_patch(patches.Polygon(wheel1, color='goldenrod'))
wheel2_obj = ax1.add_patch(patches.Polygon(wheel2, color='goldenrod'))
wheel3_obj = ax1.add_patch(patches.Polygon(wheel3, color='goldenrod'))
wheel4_obj = ax1.add_patch(patches.Polygon(wheel4, color='goldenrod'))
bumper_obj = ax1.add_patch(patches.Polygon(bumper, color='gray'))
objs = [body_obj, wheel1_obj, wheel2_obj, wheel3_obj, wheel4_obj, bumper_obj]


def init():
    return

def animate(i):
    t = np.eye(3)
    t[1,2] = 10
    for obj in objs:
        obj.set_transform(transforms.Affine2D(np.dot(t,obj.get_transform().get_matrix())))
    return

    
anim = FuncAnimation(fig1, animate, init_func=init,
                               frames=50, interval=10, repeat = False, blit=False)






def init():
    artists.append(ax1.add_patch(patches.Polygon(body)))
    artists.append(ax1.add_patch(patches.Polygon(wheel1)))
    artists.append(ax1.add_patch(patches.Polygon(wheel2)))
    artists.append(ax1.add_patch(patches.Polygon(wheel3)))
    artists.append(ax1.add_patch(patches.Polygon(wheel4)))
    artists.append(ax1.add_patch(patches.Polygon(bumper)))
    return artists

def animate(i):
    artists[0]=ax1.add_patch(patches.Polygon(body+10*i))
    artists[1]=ax1.add_patch(patches.Polygon(wheel1))
    artists[2]=ax1.add_patch(patches.Polygon(wheel2))
    artists[3]=ax1.add_patch(patches.Polygon(wheel3))
    artists[4]=ax1.add_patch(patches.Polygon(wheel4))
    artists[5]=ax1.add_patch(patches.Polygon(bumper))

anim = FuncAnimation(fig1, animate, init_func=init,
                               frames=5, interval=20, blit=True)






fig = plt.figure()
ax = plt.axes(xlim=(0, 4), ylim=(-2, 2))
line, = ax.plot([], [], lw=3)

def init():
    line.set_data([], [])
    return line,

def animate(i):
    x = np.linspace(0, 4, 1000)
    y = np.sin(2 * np.pi * (x - 0.01 * i))
    line.set_data(x, y)
    return line,

anim = FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=20, blit=True)

