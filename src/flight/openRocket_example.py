import os

import numpy as np
from matplotlib import pyplot as plt

import orhelper
from orhelper import FlightDataType, FlightEvent

from openRocket_flight import *



flight_run = openRocket_flight("Houbolt_Jr.ork","utat_test.rse")
flight_run.run()
plt.plot(flight_run.simulation_information.TYPE_TIME, flight_run.kinematics_dynamics.TYPE_ORIENTATION_THETA)
plt.show()

ax = plt.axes(projection = '3d')
x = flight_run.kinematics_dynamics.TYPE_POSITION_X
y = flight_run.kinematics_dynamics.TYPE_POSITION_Y
z = flight_run.kinematics_dynamics.TYPE_ALTITUDE
ax.plot(x,y,z)
ax.set_xlim3d([-1000, 1000])
ax.set_ylim3d([-1000, 1000])
ax.set_zlim3d([0, 3000])
plt.show()
