r'''Class that handles various inputs and systematic parameters
    and simulates muons'''
import os, sys
import subprocess
from pipes import quote

class DECOMuonSimulator():
    r'''Simulator class for muons that uses allpix
    and GEANT'''

    def __init__(self, pid, energy, theta, **kwargs):
        self.pid = pid #Particle id, ie mu+, e-
        self.energy = energy
        self.theta = theta
        self.phi = kwargs.pop('phi', 0.)
        self.depletion_thickness = kwargs.pop('depletion_thickness', 26.3)
        #todo: NOTE: in unit of um !!!!!!!
        # Set other possible systematics with kwargs, including
        # electric fields, pixel size, etc.

        self.path_to_root = os.getenv('DECO_ROOT_PATH')
        self.path_to_geant = os.getenv('DECO_GEANT_PATH')
        self.path_to_allpix = os.getenv('DECO_ALLPIX_PATH')
        self.base_command = self.path_to_allpix + ' -c ./htc_wildfire/source_measurement.conf -o'

    def write_source_file(self, n_events):

        with open('./htc_wildfire/source_measurement_replace.conf', 'r') as f:
            data = f.readlines()
        data[3] = data[3].format(n_events)
        with open('./htc_wildfire/source_measurement.conf', 'w') as wf:
            wf.writelines(data)
            wf.close()


    def write_detector_file(self):
        # USE THE PARAMETERS TO REWRITE DETECTOR FILE
        with open('./htc_wildfire/detector_replace.conf', 'r') as f:
            data = f.readlines()
        data[-2] = data[-2].format(self.phi, self.theta, 0)
        with open('./htc_wildfire/detector_temp.conf', 'w') as wf:
            wf.writelines(data)
            wf.close()

        with open('./htc_wildfire/htc_wildfire_shielded_replace.conf', 'r') as f:
            data = f.readlines()
        data[4] = data[4].format(self.depletion_thickness)
        with open('./htc_wildfire/htc_wildfire_shielded.conf', 'w') as wf:
            wf.writelines(data)
            wf.close()


    def set_output_file_name(self):
        # write unique file name depending on parameters
        if not os.path.exists("./output"):
            os.system("mkdir ./output")
        if not os.path.exists("./output/" + str(self.pid)):
            os.system("mkdir ./output/" + str(self.pid))

        self.outfile = str(self.pid) + "/" + "{}_theta_{:.1f}_phi_{:.1f}_thickiness_{:.1f}_highstats.txt".format(self.energy, self.theta, self.phi, self.depletion_thickness)
        pass


    def get_output_file_name(self):
        try:
            return self.outfile
        except:
            self.set_output_file_name()
            return self.outfile


    def run_simulation(self, n_events=100):

        self.source_local_env()
        # Run the allpix simulation

        output_file = self.get_output_file_name()
        self.write_detector_file()
        self.write_source_file(n_events)

        my_command = self.base_command[:]

        my_command += ' DepositionGeant4.particle_type="{}"'.format(self.pid)
        my_command += ' -o DepositionGeant4.source_energy="{}"'.format(self.energy)
        my_command += ' -o TextWriter.file_name="' + output_file + '"'

        """check if simulated using file name"""
        if self.check_if_simulated(output_file) is True:
            print("has been simulated")
            return

        subprocess.call(my_command, shell=True)

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


deco = DECOMuonSimulator('e+', '1GeV', 70.0, phi=120, depletion_thickness=30)
deco.run_simulation(10)

deco2 = DECOMuonSimulator('e+', '10GeV', 30.0)
deco2.run_simulation(10)