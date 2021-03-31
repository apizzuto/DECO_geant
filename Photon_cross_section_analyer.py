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




    def get_events_num(self, en, ang):
        x, y, c = self.read_hit_file(
            "./output/{}/{}_theta_{}_phi_{}_thickiness_{}_highstats.txt".format(self.pid, en, float(ang),
                                                                                float(self.phi), self.thichness))

        return len(x)

    def plot_cross_section(self, ene_number_list, ene_list, theta):

        num_events = []

        for ene in ene_list:

            num = self.get_events_num(ene, theta)

            num_events.append(num)

        num_event_err = np.sqrt(np.array(num_events))

        f = plt.figure()

        plt.errorbar(ene_number_list, num_events, yerr=num_event_err)

        plt.xscale('log')
        plt.yscale('log')

        plt.xlabel('E in eV')
        plt.ylabel('log(#Events)')

        plt.show()



energy = np.logspace(4, 9, 100)

energy_list = []

for ene in energy:
    energy_list.append(str(round(ene/pow(10, 6), 3))+"MeV")

theta = '45'
phi = '0'
particle_type = 'gamma'

thickness = 26.3

a = DECOLeptonAnalyzer(particle_type, phi, thickness)

a.plot_cross_section(energy, energy_list, theta)

