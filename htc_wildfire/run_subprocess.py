#! /usr/bin/env python

import os
import pprint
import shlex
import subprocess

particles = ['e+', 'mu+', 'gamma']
#particles = ['e-']
#particles = ['gamma']

energies = ['10keV', '31.6keV','100keV', '316keV','1MeV', '3.16MeV','10MeV', '31.6MeV','100MeV', '316MeV',
		'1GeV', '3.16GeV','10GeV']

#Change if not using on local machine
base_command = '/Users/APizzuto/Desktop/allpix/allpix-squared/bin/allpix -c ./source_measurement.conf -o'

for particle in particles:
    for energy in energies:
        my_command = base_command[:]
        print(my_command)
        my_command += ' DepositionGeant4.particle_type="{}"'.format(particle)
        my_command += ' -o DepositionGeant4.source_energy="{}"'.format(energy)
        #my_command += ' -o ROOTObjectWriter.file_name="{}/{}_theta_120_phi_30.root"'.format(particle, energy)
        my_command += ' -o TextWriter.file_name="{}/{}_theta_75_phi_30_highstats.txt"'.format(particle, energy)
        subprocess.call(my_command, shell=True)
