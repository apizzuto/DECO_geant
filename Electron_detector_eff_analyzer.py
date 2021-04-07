import numpy as np
import pandas as pd
import matplotlib.pylab as plt
from matplotlib.colors import ListedColormap
import seaborn as sns
import os
plt.style.use("IceCube")
import matplotlib as mpl
import numpy as np

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




    def get_E_deposited(self, en, ang, posz):
        x, y, c = self.read_hit_file(
            "./output/{}/{}_posz_{}_theta_{}_phi_{}_thickiness_{}_highstats.txt".format(self.pid, round(posz, 3), en, float(ang),
                                                                                float(self.phi), self.thichness))

        dE_list = []

        for i in range(len(c)):
            dE_list.append(np.array(c[i]).sum() * 3.62)

        dE_list = np.array(dE_list)

        return dE_list.mean(), dE_list.std()



energy = "10keV"

theta = '90'
phi = '0'
particle_type = 'e-'

dep_thickness = 26.3

z_pos = np.linspace(-1 * dep_thickness/2, dep_thickness/2, 100)

a = DECOLeptonAnalyzer(particle_type, phi, dep_thickness)

E_list = []
err_list = []

for z in z_pos:
    mean_val, std_val = a.get_E_deposited(energy, theta, z)

    E_list.append(mean_val)
    err_list.append(std_val)

f = plt.figure()
plt.errorbar(z_pos, E_list, yerr=err_list)
plt.xlabel("initial z position in um")
plt.ylabel("calibrated E in eV")
plt.show()