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

        xhits.append(x)
        yhits.append(y)
        charge.append(c)

        return xhits, yhits, charge

    """
    return the distance by L2 norm of (x_max_diff, y_max_diff)
    """
    def track_length(self, x, y):
        x_dist_sq = np.power(np.max(x) - np.min(x), 2.)
        y_dist_sq = np.power(np.max(y) - np.min(y), 2.)
        return np.power(x_dist_sq + y_dist_sq, 0.5)

    """
    
    """
    def get_dEdx(self, M, E, Z):
        coeff = 2.32 * 14. / 28.0855 * 0.307
        meev = .511
        gamma = E / M + 1
        beta = np.sqrt(1 - (1 / gamma ** 2))
        beta2gamma2 = (beta * gamma) ** 2
        Tmax = (2 * meev * beta2gamma2) / (1 + 2 * gamma * meev / M + (meev / M) ** 2)
        I = 10 * 14.0e-6
        hw = np.sqrt(2.32 * 14 / 28.0855) * 28.816e-6
        ln = np.log((2 * meev * beta2gamma2 * Tmax) / I ** 2)
        delta_over_2 = np.log(hw / I) + np.log(np.sqrt(beta2gamma2)) - 0.5

        return coeff * Z ** 2 / beta ** 2 * (0.5 * ln - beta ** 2 - delta_over_2)

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


a = DECOLeptonAnalyzer('e+')

x, y, c = a.read_hit_file('./output/e+/1GeV_theta_70.0_phi_120.0_thickiness_30.0_highstats.txt')
