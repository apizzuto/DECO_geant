import numpy as np


class DECOLeptonAnalyzer():
    r'''This class is for making plots like the ones in the
    notebook that read in a bunch of simulated files
    and make analysis level plots'''

    def __init__(self, pid):
        self.pid = pid
        #self.energies = np.logspace()

    def read_hit_file(self, filename):
        f = open(filename, 'r')

        xhits, yhits, charge = [], [], []

        # skip first 2 lines
        f.readline()
        f.readline()

        x, y, c = [], [], []

        while 1:

            temp = f.readline().split()

            if len(temp) < 1 or temp[0] == '#':
                break

            if temp[0] == '===':
                f.readline()
                if int(temp[1]) != 1:
                    xhits.append(x)
                    yhits.append(y)
                    charge.append(c)
                x, y, c = [], [], []

            else:
                x.append(float(temp[1][:-1]))
                y.append(float(temp[2][:-1]))
                c.append(float(temp[3][:-1]))

        return xhits, yhits, charge

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


#a = DECOLeptonAnalyzer('e+')

#x, y, c = a.read_hit_file('./htc_wildfire/output/e+/1GeV_theta_30.0_phi_0.0_highstats.txt')
