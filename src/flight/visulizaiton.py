import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

import orhelper
from orhelper import FlightDataType, FlightEvent

from openRocket_flight import *

# quaternion rotation
def q_mult(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
    z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
    return w, x, y, z

def q_conjugate(q):
    w, x, y, z = q
    return (w, -x, -y, -z)

def qv_mult(q1, v1):
    q2 = (0.0,) + v1
    return q_mult(q_mult(q1, q2), q_conjugate(q1))[1:]
################################################################

flight_run = openRocket_flight("Houbolt_Jr.ork","utat_test.rse")
flight_run.run()

# ANIMATION FUNCTION
def update(num):
    global line
    line.set_data(np.array([[0,x[num]],[0,y[num]]]))
    line.set_3d_properties(np.array([0,z[num]]))
    txt.set_text(str(round(flight_run.simulation_information.TYPE_TIME[num],2))+"s")
    return line

################################################################
######################## Input data ############################
################################################################
# THE DATA POINTS  x,y,z is the head location of the rocket
'''
pitch = flight_run.euler_angles[:834,0]
yaw = flight_run.euler_angles[:834,1]
roll = flight_run.euler_angles[:834,2]
x = np.cos(yaw)
y = np.sin(yaw)
z = np.sin(pitch)
multiplyer = np.cos(pitch)
x = x * multiplyer
y = y * multiplyer
'''
qw = flight_run.quaternion[0,:834]
qx = flight_run.quaternion[1,:834]
qy = flight_run.quaternion[2,:834]
qz = flight_run.quaternion[3,:834]
x,y,z = qv_mult((qw,qx,qy,qz),(0,0,1))

################################################################

# GET SOME MATPLOTLIB OBJECTS
fig = plt.figure()
ax = Axes3D(fig)
ax.quiver([0,0,0],[0,0,0],[0,0,0],[2,0,0],[0,2,0],[0,0,2],pivot='middle',arrow_length_ratio=0.05)
ax.set_axis_off()
# NOTE: Can't pass empty arrays into 3d version of plot()
line = plt.plot(np.array([0,1]), np.array([0,1]), np.array([0,1]), lw=2, c='g', marker='o')[0] # For line plot

# Setting the axes properties
ax.set_xlim3d([-1, 1])
ax.set_xlabel('X')
ax.set_ylim3d([-1, 1])
ax.set_ylabel('Y')
ax.set_zlim3d([-1, 1])
ax.set_zlabel('Z')
txt = ax.text(1, -1, -1, "txt")

# Creating the Animation object
line_ani = animation.FuncAnimation(fig, update, frames=len(x), interval=15, blit=False)

plt.show()