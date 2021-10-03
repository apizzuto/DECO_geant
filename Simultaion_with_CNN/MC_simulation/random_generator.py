#!/usr/bin/env python

import numpy as np
from math import *
import matplotlib.pyplot as plt
plt.style.use("IceCube")


"""
E is in unit of GeV

def check_in_range(E, theta, rand):
    val = pow(E, -2.7) * (np.cos(theta)**3)
    
    if rand < val:
        return True
    else:
        return False
"""
def check_in_range(E, theta, rand):
    val = pow(E, -2.7) * ( 1/ (1 + 1.11 * E * np.cos(theta) /115) + 0.054 / ( 1 + 1.11 * E * np.cos(theta) /850) ) * pow(E / (E + 2/cos(theta)), 2.7) * cos(theta) * sin(theta)

    if rand < val:
        return True
    else:
        return False


def get_rand_ini(E_min, E_max):
    E_min = E_min + 0.105658
    E_max = E_max + 0.105658

    factor = 1.1 * pow(E_min, -2.7)

    checker = False


    zenith_dir = 0
    energy = 0

    while not checker: # and not zenith_dir > pi/4:
        energy = np.random.random() * (E_max - E_min) + E_min
        zenith_dir = np.random.random() * (np.radians(60))
        curr = np.random.random() * factor

        checker = check_in_range(energy, zenith_dir, curr)

    """---------azimuth part---------"""
    azimuth_dir = np.random.random() * 2 * pi

    

    return energy - 0.105658, zenith_dir, azimuth_dir




"""
E_min = 0.15  # GeV
E_max = 100  # GeV

energy_list = []
zenith_list = []
azimuth_list = []
for i in range(1000):
    print("working on " + str(i))
    ene, zen, azi = get_rand_ini(E_min, E_max)
    energy_list.append(ene)
    zenith_list.append(zen)
    azimuth_list.append(azi)

energy_list = np.array(energy_list)

f = plt.figure()
plt.hist(np.log10(energy_list), bins=50, density=True)

plt.legend()
plt.yscale('log')
plt.xlabel("log10(E/GeV)")
plt.ylabel("normalized # events weighted by E^3")

f2 = plt.figure()
plt.hist(zenith_list, bins=50, density=True)
zen_list = np.linspace(0, pi/2, 100)
flux = np.power(np.cos(zen_list), 3) / (float(2)/3)
plt.plot(zen_list, flux, label='normalized cos^3')
plt.legend()
plt.xlabel("zenith angle (rad)")
plt.ylabel("# events")

f3 = plt.figure()
plt.hist(azimuth_list, bins=50)
plt.xlabel("azimuth angle")
plt.ylabel("# events")

plt.show()
"""


