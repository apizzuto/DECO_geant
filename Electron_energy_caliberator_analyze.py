import numpy as np
import pandas as pd
import matplotlib.pylab as plt
from matplotlib.colors import ListedColormap
import seaborn as sns
import os
plt.style.use("IceCube")
import matplotlib as mpl

class DECOLeptonAnalyzer():
    r'''This class is for making plots like the ones in the
    notebook that read in a bunch of simulated files
    and make analysis level plots'''

    def __init__(self, pid, phi, thickness):
        self.pid = pid

        self.thichness = thickness

        self.phi = phi


    def read_hit_file(self, filename):
        f = open(filename, 'r')

        xhits, yhits, charge = [], [], []

        # skip first 2 lines
        f.readline()
        f.readline()

        x, y, c = [], [], []

        flag = 1
        while 1:

            temp = f.readline().split()

            if len(temp) < 1 or temp[0] == '#':
                break

            if temp[0] == '===':
                continue
            if temp[0] == '---':
                if flag == 1:
                    flag = 0
                else:
                    xhits.append(x)
                    yhits.append(y)
                    charge.append(c)
                    x, y, c = [], [], []

            else:
                x.append(float(temp[1][:-1]))
                y.append(float(temp[2][:-1]))
                c.append(float(temp[3][:-1]))

        if len(x) > 0:
            xhits.append(x)
            yhits.append(y)
            charge.append(c)

        return xhits, yhits, charge




    def get_E_deposited(self, en, ang):
        x, y, c = self.read_hit_file(
            "./output/{}/{}_theta_{}_phi_{}_thickiness_{}_highstats.txt".format(self.pid, en, float(ang),
                                                                                float(self.phi), self.thichness))

        dE_list = []

        for i in range(len(c)):
            dE_list.append(np.array(c[i]).sum() * 3.62)


        return np.array(dE_list)





energy = np.logspace(4, 5, 10)

energy_list = []

for ene in energy:
    energy_list.append(str(round(ene/pow(10, 6), 3))+"MeV")

theta = '45'
phi = '0'
particle_type = 'e-'

thickness = 26.3

a = DECOLeptonAnalyzer(particle_type, phi, thickness)

for i in range(len(energy)):
    dE_list = a.get_E_deposited(energy_list[i], theta)

    f = plt.figure()

    plt.hist(dE_list, bins=30, label=str(energy_list[i]))

    plt.xlabel("calibrated deposited energy in eV")

    plt.ylabel("# events (1000 in total)")

    plt.legend()

    plt.show()

