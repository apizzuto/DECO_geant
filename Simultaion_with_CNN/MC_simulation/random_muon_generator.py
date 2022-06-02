#!/usr/bin/env python

import numpy as np
from math import *


"""Weight function is according to the atmospheric muon flux and detector effective area"""
def check_in_range(E, theta, rand):
    val = pow(E, -2.7) * ( 1/ (1 + 1.11 * E * np.cos(theta) /115) + 0.054 / ( 1 + 1.11 * E * np.cos(theta) /850) ) * pow(E / (E + 2/cos(theta)), 2.7) * cos(theta) * sin(theta)

    if rand < val:
        return True
    else:
        return False


def get_rand_ini_muon(E_min, E_max):
    E_min = E_min + 0.105658
    E_max = E_max + 0.105658

    factor = 1.1 * pow(E_min, -2.7)

    checker = False


    zenith_dir = 0
    energy = 0

    while not checker: # and not zenith_dir > pi/4:
        energy = np.random.random() * (E_max - E_min) + E_min
        zenith_dir = np.random.random() * (np.radians(90))
        curr = np.random.random() * factor

        checker = check_in_range(energy, zenith_dir, curr)

    """---------azimuth part---------"""
    azimuth_dir = np.random.random() * 2 * pi

    

    return energy - 0.105658, zenith_dir, azimuth_dir



