import numpy as np
from math import *
from MuonSimulator import DECOMuonSimulator
from random_generator import get_rand_ini

E_min = 0.01  # GeV
E_max = 100  # GeV
dep_thickness = 26.3 #um
pos = [0, 0, dep_thickness/2]
particle_type = 'mu+'
num = 2000

for i in range(num):
    print("working on " + str(i) + " out of " + str(num))
    ene, zen, azi = get_rand_ini(E_min, E_max)

    zenith = str(degrees(zen))
    azimuth = str(degrees(azi))

    energy = str(ene) + "GeV"

    want_charge_plot = "false"

    a = DECOMuonSimulator(particle_type, energy, pos, zenith, phi=azimuth,
                          depletion_thickness=str(dep_thickness), qdc_resolution=0, qdc_smearing=0, qdc_slope=7,
                          electronics_noise=5, bias_v=-20, dep_v=-10, gain=1.0, pixel_size=0.9)

    a.run_simulation(1, want_charge_plot)

"""
001: 1.4um bias -20 dep -10
002: 1.4um bias -5  dep -10
003: 1.4um bias -50 dep -10
004: 1.4um bias -20 dep -5
005: 1.4um bias -20 dep -50

006: 1.4um bias -10 dep -10

007: 0.9um bias -20 dep -10, 
"""

"""

energy_list = ['10GeV']

#energy = np.logspace(log10(50000), 10, 100)

#energy_list = []

#for ene in energy:
#    energy_list.append(str(round(ene/pow(10, 6), 4))+"MeV")


#angles = ['0', '15', '30', '45', '60', '75']

#phis = ['0', '15', '30', '45', '60', '75', '90']

#energy = ['10GeV']
angles = ['45']
phis = ['45']
particle_type = 'mu+'


want_charge_plot = "false"

for ene in energy_list:
    for ang in angles:
        for azi in phis:
            a = DECOMuonSimulator(particle_type, ene, pos, ang, phi=azi, depletion_thickness=str(dep_thickness))

            a.run_simulation(10, want_charge_plot)
"""