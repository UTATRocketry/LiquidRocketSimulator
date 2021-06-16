"""
*** Refer to the openRocket_flight documentation for a more elaborate description of the code's use ***

- This file uses openRocket_flight.py to run an example simulation from the provided data within OpenRocket.

- Ensure that the .ork and .rse files (in this case, Houbolt_Jr.ork and utat_test.rse) are located within the
  'Simulation' folder. The Simulation folder must be located in the same directory as the code.

- When the simulation has been successfully completed, you will see the message,'Simulation finished'.

- When the variables have been successfully classified and organized, you will see the message,'Variables prepared'.

"""

'''Running the simulation'''

from openRocket_flight import *

flight_run = openRocket_flight("Houbolt_Jr.ork", "utat_test.rse")  # Input .ork and .rse files used for the simulation
flight_run.run()  # This command will run the simulation through the openRocket_flight.py file.

'''To access the variables received from the simulation, use the following format: flight_run.UTAT_family.TYPE'''

print(flight_run.kinematics_dynamics.TYPE_AOA)
print(flight_run.rocket_properties.TYPE_REFERENCE_LENGTH)

'''Additional variables that can be accessed within the code. Refer to the code documentation for variable descriptions'''

state_vector = flight_run.state_vector
euler_axis = flight_run.euler_axis
quaternion = flight_run.quaternion
recovery_time = flight_run.recovery_time

'''Example 1: Using the simulation variables from the openRocket_flight.py file to generate a 2D graph'''

plt.plot(state_vector[0], state_vector[3])
plt.show()

'''Example 2: Using the simulation variables from the openRocket_flight.py file to generate a 3D graph'''

ax = plt.axes(projection='3d')
x = state_vector[1]
y = state_vector[2]
z = state_vector[3]

ax.plot(x, y, z)
ax.set_xlim3d([-1000, 1000])
ax.set_ylim3d([-1000, 1000])
ax.set_zlim3d([0, 3000])
plt.show()

flight_run.plot()