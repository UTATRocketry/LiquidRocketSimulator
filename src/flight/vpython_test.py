from vpython import *
from openRocket_flight import *

flight_run = openRocket_flight("Houbolt_Jr.ork", "utat_test.rse")
flight_run.run()

'''Creating Animated Simulation for Rocket Altitude'''

rocket_parts = []
scene = canvas(title='Rocket Altitude Simulation')
rocket_parts.append(cylinder(pos=vector(0, 0, 0), size=vector(0.5, 0.1, 0.1), color=color.red, axis=vector(0, 1, 0)))
rocket_parts.append(cone(pos=rocket_parts[0].pos + rocket_parts[0].size.x * rocket_parts[0].axis * 2, color=color.red,
                         size=vector(rocket_parts[0].size.y, rocket_parts[0].size.y, rocket_parts[0].size.y),
                         axis=vector(0, 1, 0)))
rocket_parts.append(
    triangle(v0=vertex(pos=rocket_parts[0].pos + 0.5 * rocket_parts[0].size.y * vector(1, 0, 0), color=color.red),
             v1=vertex(pos=rocket_parts[0].pos + 1.5 * rocket_parts[0].size.y * vector(1, 0, 0), color=color.red),
             v2=vertex(pos=rocket_parts[0].pos + 0.5 * rocket_parts[0].size.y * vector(1, 2, 0), color=color.red)))
rocket_parts.append(
    triangle(v0=vertex(pos=rocket_parts[0].pos + 0.5 * rocket_parts[0].size.y * vector(-1, 0, 0), color=color.red),
             v1=vertex(pos=rocket_parts[0].pos + 1.5 * rocket_parts[0].size.y * vector(-1, 0, 0), color=color.red),
             v2=vertex(pos=rocket_parts[0].pos + 0.5 * rocket_parts[0].size.y * vector(-1, 2, 0), color=color.red)))
rocket_parts.append(
    triangle(v0=vertex(pos=rocket_parts[0].pos + 0.5 * rocket_parts[0].size.y * vector(0, 0, 1), color=color.red),
             v1=vertex(pos=rocket_parts[0].pos + 1.5 * rocket_parts[0].size.y * vector(0, 0, 1), color=color.red),
             v2=vertex(pos=rocket_parts[0].pos + 0.5 * rocket_parts[0].size.y * vector(0, 2, 1), color=color.red)))
rocket_parts.append(
    triangle(v0=vertex(pos=rocket_parts[0].pos + 0.5 * rocket_parts[0].size.y * vector(0, 0, -1), color=color.red),
             v1=vertex(pos=rocket_parts[0].pos + 1.5 * rocket_parts[0].size.y * vector(0, 0, -1), color=color.red),
             v2=vertex(pos=rocket_parts[0].pos + 0.5 * rocket_parts[0].size.y * vector(0, 2, -1), color=color.red)))
launch_pad = box(pos=vector(0, -0.5/2-0.05, 0), color=vector(0.8, 0.8, 0.8), size=vector(2, 0.01, 2))

rocket = compound(rocket_parts, pos=vector(0, 0, 0))
attach_trail(rocket)
scene.camera.follow(rocket)

x = flight_run.kinematics_dynamics.TYPE_POSITION_X
y = flight_run.kinematics_dynamics.TYPE_POSITION_Y
z = flight_run.kinematics_dynamics.TYPE_ALTITUDE

for t in range(len(x)):
    rate(100)
    rocket.pos = vector(x[t], z[t], y[t])
    t += 1

print("Rocket altitude simulation completed.")

