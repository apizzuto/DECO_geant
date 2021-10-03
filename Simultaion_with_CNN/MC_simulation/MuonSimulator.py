r'''Class that handles various inputs and systematic parameters
    and simulates muons'''
import os, sys
import subprocess
from pipes import quote
from math import *
import numpy as np

class DECOMuonSimulator():
    r'''Simulator class for muons that uses allpix
    and GEANT'''

    def __init__(self, pid, energy, pos, theta, **kwargs):
        self.pid = pid #Particle id, ie mu+, e-
        self.pos = pos
        self.energy = energy
        self.theta = float(theta)
        self.phi = float(kwargs.pop('phi', 0.))
        self.depletion_thickness = float(kwargs.pop('depletion_thickness', 26.3))
        #todo: NOTE: in unit of um !!!!!!!
        # Set other possible systematics with kwargs, including
        # electric fields, pixel size, etc.

        self.path_to_root = os.getenv('DECO_ROOT_PATH')
        self.path_to_geant = os.getenv('DECO_GEANT_PATH')
        self.path_to_allpix = os.getenv('DECO_ALLPIX_PATH')
        self.base_command = self.path_to_allpix + ' -c ./htc_wildfire/source_measurement.conf -o'

        self.qdc_resolution = int(kwargs.pop('qdc_resolution', 0.))
        self.qdc_smearing = int(kwargs.pop('qdc_smearing', 0.))
        self.qdc_slope = kwargs.pop('qdc_slope', 0.)

        self.electronics_noise = kwargs.pop('electronics_noise', 0.)
        self.bias_v = kwargs.pop('bias_v', -15)
        self.dep_v = kwargs.pop('dep_v', -10)
        self.gain = kwargs.pop('gain', 1.0)

        self.pixel_size = float(kwargs.pop('pixel_size', 1.0))

    def write_source_file(self, n_events, want_plot):

        with open('./htc_wildfire/source_measurement_replace.conf', 'r') as f:
            data = f.readlines()
        data[3] = data[3].format(n_events)

        data[18] = data[18].format(str(self.pos[0]) + " " + str(self.pos[1]) + " " + str(self.pos[2]) + "um")

        theta = radians(self.theta)
        phi = radians(self.phi)

        print(self.theta, self.phi, self.energy)
        dirx = -1*sin(theta)*cos(phi)
        diry = -1*sin(theta)*sin(phi)
        dirz = -1*cos(theta)

        data[20] = data[20].format(str(dirx) + " " + str(diry) + " " + str(dirz))

        if want_plot == 'true':
            data[38] = data[38].format('true' + "\n" + "output_linegraphs = true \n output_plots_step = 10ps \n output_plots_align_pixels = true \n output_plots_use_pixel_units = true")
        else:
            data[38] = data[38].format("false")

        data[50] = data[50].format(str(self.qdc_resolution))
        data[51] = data[51].format(str(self.qdc_smearing))
        data[52] = data[52].format(str(self.qdc_slope))
        data[53] = data[53].format(str(self.gain))
        data[54] = data[54].format(str(self.electronics_noise))
        data[28] = data[28].format(str(self.bias_v))
        data[29] = data[29].format(str(self.dep_v))

        with open('./htc_wildfire/source_measurement.conf', 'w') as wf:
            wf.writelines(data)
            wf.close()


    def write_detector_file(self):

        with open('./htc_wildfire/htc_wildfire_shielded_replace.conf', 'r') as f:
            data = f.readlines()
        data[3] = 'pixel_size = ' + str(self.pixel_size) + "um " + str(self.pixel_size) + "um\n"
        data[4] = data[4].format(self.depletion_thickness)
        with open('./htc_wildfire/htc_wildfire_shielded.conf', 'w') as wf:
            wf.writelines(data)
            wf.close()


    def set_output_file_name(self):
        # write unique file name depending on parameters
        if not os.path.exists("./output"):
            os.system("mkdir ./output")
        if not os.path.exists("./output/" + "qdc_res_" + str(self.qdc_resolution) + "_smear_" +
                              str(self.qdc_smearing) + "_slope_" + str(self.qdc_slope) + "/"):
            os.system("mkdir ./output/" + "qdc_res_" + str(self.qdc_resolution) + "_smear_" +
                      str(self.qdc_smearing) + "_slope_" + str(self.qdc_slope) + "/")
        if not os.path.exists("./output/" + "qdc_res_" + str(self.qdc_resolution) + "_smear_" +
                              str(self.qdc_smearing) + "_slope_" + str(self.qdc_slope) + "/" + str(self.pid)):
            os.system("mkdir ./output/" + "qdc_res_" + str(self.qdc_resolution) + "_smear_" +
                      str(self.qdc_smearing) + "_slope_" + str(self.qdc_slope) + "/" + str(self.pid))

        self.outfile = "qdc_res_" + str(self.qdc_resolution) + "_smear_" + str(self.qdc_smearing) + "_slope_" + str(self.qdc_slope) + "/" +  str(self.pid) + \
                       "/" + "{}_theta_{:.1f}_phi_{:.1f}_thickiness_{:.1f}_highstats.txt".format(self.energy, self.theta, self.phi, self.depletion_thickness)
        pass


    def get_output_file_name(self):
        try:
            return self.outfile
        except:
            self.set_output_file_name()
            return self.outfile


    def run_simulation(self, n_events, want_charge_plot='false'):

        self.source_local_env()
        # Run the allpix simulation

        output_file = self.get_output_file_name()
        self.write_source_file(n_events, want_charge_plot)
        self.write_detector_file()

        my_command = self.base_command[:]

        my_command += ' DepositionGeant4.particle_type="{}"'.format(self.pid)
        my_command += ' -o DepositionGeant4.source_energy="{}"'.format(self.energy)
        my_command += ' -o TextWriter.file_name="' + output_file + '"'

        """check if simulated using file name"""
        if self.check_if_simulated(output_file) is True:
            print("has been simulated")
            return

        with open(os.devnull, 'w') as devnull:
            subprocess.call(my_command, shell=True, stdout=devnull)

        return


    def check_if_simulated(self, filename):
        # Check to see if simulation has already been run for
        # this set of parameters

        if not os.path.exists("./output/" + filename):
            return False

        return True



    def source_local_env(self):
        geant = self.path_to_geant + "/bin/geant4.sh"
        root = self.path_to_root + "/bin/thisroot.sh"

        pass
        # Run source scripts for ROOT and GEANT if the
        # simulation doesn't work








"""
dep_thickness = 26.3 #um
pos = [0, 0, 0]

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

