import numpy as np

class DECOLeptonAnalyzer():
    r'''This class is for making plots like the ones in the 
    notebook that read in a bunch of simulated files
    and make analysis level plots'''
    
    def __init__(self, pid):
        self.pid = pid
        self.energies = np.logspace()


    def bethe_bloch_plot(self):
        pass

    def track_length_vs_angle_violinplot(self):
        pass

    def check_if_all_simulated(self):
        pass

    def hillas_length_histogram(self):
        pass

    def hillas_width_histogram(self):
        pass

    