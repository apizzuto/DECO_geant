#!/usr/bin/env python

import numpy as np
from math import *


"""Weight function corresponds to isotropic zenith angle distribution with detector effective area effect"""
def checker(ang):

    checker = np.random.random()

    val = cos(ang) * (1 - cos(ang))/2

    if checker <= val:
        return True

    else:
        return False


def get_rand_ini_e_gamma():

    while 1: # and not zenith_dir > pi/4:

        zen_ang = np.random.random() * pi / 2

        if checker(zen_ang) == True:

            """---------azimuth part---------"""
            azimuth_dir = np.random.random() * 2 * pi

            return zen_ang, azimuth_dir



