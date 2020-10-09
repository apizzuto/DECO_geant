r'''Class that handles various inputs and systematic parameters
    and simulates muons'''

class DECOMuonSimulator():
    r'''Simulator class for muons that uses allpix
    and GEANT'''

    def __init__(self, pid, energy, theta, **kwargs):
        self.pid = pid #Particle id, ie mu+, e-
        self.energy = energy
        self.theta = theta
        self.phi = kwargs.pop('phi', 0.)
        self.depletion_thickness = kwargs.pop('depletion_thickness', 26.3e-6)
        # Set other possible systematics with kwargs, including
        # electric fields, pixel size, etc.

    def write_conf_file(self):
        # USE THE PARAMETERS TO REWRITE CONF FILE
        pass

    def write_detector_file(self):
        # USE THE PARAMETERS TO REWRITE DETECTOR FILE
        pass

    def set_output_file_name(self):
        # write unique file name depending on parameters
        self.outfile = 'foo'
        pass

    def get_output_file_name(self):
        try:
            return self.outfile
        except:
            self.set_output_file_name()
            return self.outfile

    def run_simulation(self, n_events=100):
        # Run the allpix simulation
        pass

    def check_if_simulated(self):
        # Check to see if simulation has already been run for
        # this set of parameters
        pass

    def source_local_env(self):
        # Run source scripts for ROOT and GEANT if the 
        # simulation doesn't work
        pass