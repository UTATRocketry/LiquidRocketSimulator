from vpython import *
from openRocket_flight import *


# quaternion rotation
def q_mult(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    a = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    b = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
    c = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
    return w, a, b, c


def q_conjugate(q):
    w, a, b, c = q
    return w, -a, -b, -c


def qv_mult(q1, v1):
    q2 = (0.0,) + v1
    return q_mult(q_mult(q1, q2), q_conjugate(q1))[1:]


flight_run = openRocket_flight("Houbolt_Jr.ork", "utat_test.rse")
flight_run.run()

###########################################################################

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

scaling_factor = 150  # change to adjust rocket and launch pad sizing within the animation
rocket = compound(rocket_parts, pos=vector(0, 0, 0))
attach_trail(rocket)
rocket.size = scaling_factor * vector(2.5, 5, 2.5)
scene.camera.follow(rocket)

launch_pad = box(pos=vector(0, -2.5 * scaling_factor, 0), color=vector(0.8, 0.8, 0.8),
                 size=scaling_factor * vector(12, 0.5, 12))

x = flight_run.kinematics_dynamics.TYPE_POSITION_X
y = flight_run.kinematics_dynamics.TYPE_POSITION_Y
z = flight_run.kinematics_dynamics.TYPE_ALTITUDE

qw = flight_run.quaternion[0, :834]
qx = flight_run.quaternion[1, :834]
qy = flight_run.quaternion[2, :834]
qz = flight_run.quaternion[3, :834]
rx, ry, rz = qv_mult((qw, qx, qy, qz), (0, 0, 1))

i = 0

for t in range(len(x)):
    rate(100)
    rocket.pos = vector(x[t], z[t], y[t])
    if i < len(rx) and t > 100:
        rocket.rotate(angle=rx[i], axis=vector(1, 0, 0))  # pitch axis
        rocket.rotate(angle=rz[i], axis=vector(0, 1, 0))  # roll axis
        rocket.rotate(angle=ry[i], axis=vector(0, 0, 1))  # yaw axis
        i += 1

print("Rocket altitude simulation completed.")
