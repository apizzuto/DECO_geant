#! /usr/bin/env python

import os
import pprint
import shlex
import subprocess
import numpy as np


particles = ['e+', 'mu+', 'gamma']
energies = ['10keV', '31.6keV','100keV', '316keV','1MeV', '3.16MeV','10MeV', '31.6MeV','100MeV', '316MeV',
		'1GeV', '3.16GeV','10GeV']

cos_thetas = np.linspace(0.1, 1., 10)
thetas = np.arccos(cos_thetas)* 180. / np.pi
phis = np.linspace(0., 90., 10)

#Change if not using on local machine
base_command = '/Users/APizzuto/Desktop/allpix/allpix-squared/bin/allpix -c ./source_measurement.conf -o'

for theta in thetas[4:]:
    for phi in phis:
		with open('./detector_replace.conf', 'r') as f:
			data = f.readlines()
		data[-2] = data[-2].format(phi, theta, 0)
		with open('./detector_temp.conf', 'w') as wf:
			wf.writelines(data)
			wf.close()
		for particle in particles:
			for energy in energies:
				my_command = base_command[:]
				print(my_command)
				my_command += ' DepositionGeant4.particle_type="{}"'.format(particle)
				my_command += ' -o DepositionGeant4.source_energy="{}"'.format(energy)
				my_command += ' -o TextWriter.file_name="{}/{}_theta_{:.1f}_phi_{:.1f}_highstats.txt"'.format(particle, energy, theta, phi)
				subprocess.call(my_command, shell=True)
