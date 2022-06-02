import numpy as np
from math import *
from Simulator_interface import DECOSimulator
from random_muon_generator import get_rand_ini_muon
from random_e_gamma_generator import get_rand_ini_e_gamma

# energy range and particle type setup
E_min = 0.01  # GeV
E_max = 100  # GeV
dep_thickness = 26.3 #um
pos = [0, 0, dep_thickness/2]
particle_type = 'mu+'

# total number of events to be simulated
num = 2000

for i in range(num):
    print("working on " + str(i) + " out of " + str(num))

    # get a random muon. Can also use electron or muon generator to generate isotropic zenith angle and uniform energy
    ene, zen, azi = get_rand_ini_muon(E_min, E_max)

    zenith = str(degrees(zen))
    azimuth = str(degrees(azi))

    energy = str(ene) + "GeV"

    want_charge_plot = "false"

    # qdc parameters, electronic noise, bias voltage, gain factor, pixel size, and seed (random if not specified)
    a = DECOSimulator(particle_type, energy, pos, zenith, phi=azimuth,
                          depletion_thickness=str(dep_thickness), qdc_resolution=0, qdc_smearing=0, qdc_slope=0,
                          electronics_noise=0, bias_v=-25, gain=1.0, pixel_size=0.9, seed=10086)

    # run one event fer this setup
    a.run_simulation(1, want_charge_plot)


