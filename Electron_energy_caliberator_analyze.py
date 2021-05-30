import numpy as np
import pandas as pd
import matplotlib.pylab as plt
from matplotlib.colors import ListedColormap
import seaborn as sns
import os
plt.style.use("IceCube")
import matplotlib as mpl
from math import *
import sys



def get_dEdx(M, E, Z, type):
    coeff = 2.32 * 14. / 28.0855 * 0.307
    meev = .511
    gamma = E / M + 1
    beta = np.sqrt(1 - (1 / gamma ** 2))
    beta2gamma2 = (beta * gamma) ** 2
    if type != 'e+' and type != 'e-':
        Tmax = (2 * meev * beta2gamma2) / (1 + 2 * gamma * meev / M + (meev / M) ** 2)
    else:
        Tmax = E + M
    I = 10 * 14.0e-6
    hw = np.sqrt(2.32 * 14 / 28.0855) * 28.816e-6
    ln = np.log((2 * meev * beta2gamma2 * Tmax) / I ** 2)
    delta_over_2 = np.log(hw / I) + np.log(np.sqrt(beta2gamma2)) - 0.5

    return coeff * Z ** 2 / beta ** 2 * (0.5 * ln - beta ** 2 - delta_over_2)


def getdE(E_ini, dep_leng, p_type):

    E_curr = E_ini
    remain_dis = dep_leng * pow(10, -6)

    while 1:
        if E_curr <= 0 and remain_dis > 0:
            return E_ini

        if remain_dis <= 0:
            return E_ini - E_curr

        if E_curr < 1e5:
            step_size = 0.001 * 1e-6
        elif E_curr > 1e5 and E_curr < 1e6:
            step_size = 0.01 * 1e-6
        elif E_curr > 1e6 and E_curr < 5 * 1e6:
            step_size = 0.1 * 1e-6
        elif E_curr > 5*1e6 and E_curr < 1e7:
            step_size = 1e-6
        else:
            step_size = 2 * 1e-6

        dE_dx = get_dEdx(Mass, E_curr/pow(10, 6), 1.0, p_type)

        E_curr -= dE_dx*pow(10, 6) * step_size/0.01

        remain_dis -= step_size



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





energy = np.logspace(4, 10, 100)

energy_list = []

for ene in energy:
    energy_list.append(str(ene/pow(10, 6))+"MeV")

theta = '45'
phi = '0'
particle_type = 'mu+'

thickness = 26.3

a = DECOLeptonAnalyzer(particle_type, phi, thickness)

E_calibrate_list = []
err_list = []
E_exp_list = []

for i in range(len(energy)):

    print("working on " + str(round(energy[i]/pow(10, 6), 4)) + "MeV")

    dE_list = a.get_E_deposited(energy_list[i], theta)

    E_calibrate_list.append(dE_list.mean())

    err_list.append(dE_list.std())

    if particle_type == 'mu+' or particle_type == 'mu-':
        Mass = 105.658
    if particle_type == 'e-' or particle_type == 'e+':
        Mass = 0.511

    E_exp_list.append(getdE(energy[i], thickness/2, particle_type))


    f = plt.figure()

    plt.hist(dE_list, bins=int((dE_list.max() - dE_list.min())/1000) + 1, label="initial E = " + str(round(energy[i]/pow(10, 6), 4)) + "MeV \nmean of calibrated E = "
                                      + str(round(dE_list.mean()/pow(10, 6), 4)) +
                                      "MeV \nstd = " + str(round(dE_list.std()/pow(10, 6), 4)) + "MeV")

    plt.xlabel("calibrated deposited energy in eV")

    plt.ylabel("# events (" + str(len(dE_list)) + " in total)")

    plt.legend()

    if not os.path.exists("./Individual_E_Calib_Plots"):
        os.mkdir("./Individual_E_Calib_Plots")
    if not os.path.exists("./Individual_E_Calib_Plots/" + str(particle_type)):
        os.mkdir("./Individual_E_Calib_Plots/" + str(particle_type))

    plt.savefig("./Individual_E_Calib_Plots/" + str(particle_type) + "/Eini_" + str(round(energy[i]/pow(10, 6), 4)) + "MeV.png", bbox_inches='tight')

    plt.close()
    #plt.show()



f = plt.figure()
plt.errorbar(energy, E_calibrate_list, yerr=err_list, label='Calibrated energy with uncertainty')
plt.plot(energy, E_exp_list, label='Expected fully reconstructed energy with uncertainty', linewidth=3)
plt.legend()
plt.xlabel("Initial energy in eV")
plt.ylabel("Calibrated energy in eV")
plt.xscale('log')
plt.show()
