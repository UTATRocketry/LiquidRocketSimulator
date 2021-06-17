import numpy as np
import math
import matplotlib.pyplot as plt

def temperature(h):
    # h: cur_height; unit: m
    # T: temperature; unit: K
    if (h<11000): # gradient
        a = -0.0065 # a = 6.5K/km
        T0 = 288.15 # K
        T = T0 + a*h # K
    elif (h<20000): # isothermal
        T = 216.66-273.15 # K
    return T

def density(h):
    g0 = 9.80665 # m/s^2
    a = -0.0065 # 6.5K/km
    R = 287 # J/(kg*K)
    T = temperature(h);
    if (h<11000): # gradient
        T1 = 288.15 # ground level temperature
        d = (T/T1)**(-(g0/(a*R)+1))
    elif (h<20000):
        h1 = 11000 # m
        d = e**((-(g0/(R*T))*(h-h1)))
    return d

def gaussian(h):
    # h: cur_height
    a = 37.55331224;
    b = 14.30107053;
    c = 6.7123204;
    return a*np.exp(-np.power(h/1000 - b, 2)/(2*np.power(c, 2)))

def gaussianWithNoise(h):
    # n: numberOfPoints
    n = 1000
    # h: cur_height
    gau = gaussian(h)
    gauArray=np.full((1, n), gau, dtype=int) # 7->gau
    noise = np.random.normal(0,3,n)
    # 0 is the mean of the normal distribution you are choosing from
    # 3 is the standard deviation of the normal distribution
    # n is the number of elements you get in array noise
    return gauArray+noise # signal+noise

def main():
    # parameters
    apogee = flight_run.state_vector_function(flight_run.apogee_time)[3] # m
    m = flight_run.value_of(flight_run.rocket_properties.TYPE_MASS,flight_run.apogee_time) # kg
    h = 250 # m set one layer as 250m
    h_main = 250 # m when the main parachute is deployed
    n = apogee/h # layer
    x0 = 0 # point of entry
    y0 = 0
    wind_direction=np.full((1, 126), 145, dtype=int)# wind directions
    curr_height = apogee
    counter = 1
    x_total = 0
    y_total = 0
    # constants
    g = 9.81 # m/s^2
    # drogue air resistance parameters
    # before the main parachute is deployed: drougue
    diameter1 = 1.70434 # m
    A = math.pi*(diameter1/2)**2 # m^2
    Cd1 = 0.775 # drag constant
    # after the main parachute is deployed: main parachute
    diameter2 = 3.048 # m 120inches
    A2 = math.pi*(diameter2/2)**2;
    Cd2 = 2.2 # drag constant
    ### there is an initial horizontal velocity when the rocket is turning its
    ### direction, will be obtained from the simulation/class (DEVELOPED without considering
    ### horizontal drag)
    while(n>0):
        d = density(curr_height) # kg/m^3 density
        if (curr_height >= h_main):
            v_terminal1 =  math.sqrt(2*m*g/(d*Cd1*A))
            t_layer = h/v_terminal1;
        else: # curr_height < h_main

            v_terminal2 = math.sqrt(2*m*g/(d*Cd2*A2))
            t_layer = h/v_terminal2;

        # update the current height to one layer down
        curr_height = curr_height - h;
        wind_profile = gaussianWithNoise(curr_height)

        # # rocket horizontal velocity with drag
        # length = 367 * 0.01
        # diameter = 15.2 * 0.01
        # rocket_a_xcomponent = (d*0.42*length*diameter)*(V/m # drag force/mass

        # high speed v^2
        x = flight_run.state_vector_function(flight_run.recovery_time[0])[4]
        y = flight_run.state_vector_function(flight_run.recovery_time[0])[5]
        rocket_v_xcomponent = math.sqrt(x**2+y**2)
        wind_xcomponent = np.dot(gaussianWithNoise(curr_height),np.sin(wind_direction[0][counter])) + rocket_v_xcomponent
        wind_ycomponent = np.dot(gaussianWithNoise(curr_height),np.cos(wind_direction[0][counter]))
        position_x = t_layer*wind_xcomponent # distance by wind
        position_y = t_layer*wind_ycomponent
        x_total = x_total+position_x
        y_total = y_total+position_y
        counter = counter + 1
        n = n-1

    xposition_final=x0+x_total # final x coordinate
    yposition_final=y0+y_total # final y coordinate
    print("average total distance:%f\n" % (np.mean(xposition_final)**2+np.mean(yposition_final)**2)**0.5)
    print("terminal_velocity:%f" % v_terminal2)

    colors = np.random.rand(1000)
    plt.scatter(xposition_final,yposition_final, s=1, c=colors, alpha=0.5)
    plt.gca().update(dict(title='Wind Porfile Model', xlabel='x position (m)', ylabel='y position (m)', ylim=(0,10)))
    plt.axis([-1000, 1000, -1000, 1000])
    plt.plot(np.mean(xposition_final),np.mean(yposition_final),color='b',marker='o')
    plt.plot(0,0,color="b",marker='.')
    plt.grid()
    plt.show()

main()
