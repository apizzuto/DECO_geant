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




    def plot_single(self, en, numerica_e, ang, num_to_do):
        x, y, c = self.read_hit_file(
            "./output/{}/{}_theta_{}_phi_{}_thickiness_{}_highstats.txt".format(self.pid, en, float(ang),
                                                                                float(self.phi), self.thichness))

        for j in range(len(x))[:num_to_do]:

                image = np.zeros((4500, 4500))
                for i in range(len(x[j])):
                    image[int(y[j][i]), int(x[j][i])] = c[j][i]


                med_x = np.median(x[j])
                med_y = np.median(y[j])
                size = 50.

                fig1 = plt.figure(1, figsize=(8, 8))
                ax = fig1.add_subplot(111)
                fig1.set_facecolor('white')

                # my_cmap = ListedColormap(sns.color_palette("Blues", 50))
                # my_cmap = ListedColormap(sns.palplot(sns.cubehelix_palette(8, start=2, rot=0, dark=0, light=.95, reverse=True)))
                my_cmap = mpl.cm.hot

                # image = np.where(image == 0.0, np.nan, image)

                im = ax.imshow(image, cmap=my_cmap,  # interpolation="gaussian",
                               aspect="auto", vmax=100., vmin=0.0)
                ax.set_xlim([med_x - size, med_x + size])
                ax.set_ylim([med_y - size, med_y + size])
                ax.set_xlabel("X (pixels)")
                ax.set_ylabel("Y (pixels)")

                ax.grid(color="#ffffff")
                cb = fig1.colorbar(im, orientation="vertical",
                                   shrink=0.8,
                                   fraction=0.05,
                                   pad=0.15)
                label = "Pixel Luminance"
                cb.set_label(label)
                ax.text(med_x + size * 0.3, med_y + size * 0.7,
                        "Simulation", fontsize=24, color='w', weight='heavy')

                if not os.path.exists("./2Dimages"):
                    os.mkdir("./2Dimages")
                if not os.path.exists("./2Dimages/" + str(particle_type)):
                    os.mkdir("./2Dimages/" + str(particle_type))
                if not os.path.exists("./2Dimages/" + str(particle_type) + "/" + str(round(numerica_e/pow(10, 6), 4)) + "MeV"):
                    os.mkdir("./2Dimages/" + str(particle_type) + "/" + str(round(numerica_e/pow(10, 6), 4)) + "MeV")

                title = str(self.pid) + " initial energy is " + str(round(numerica_e/pow(10, 6), 4)) + "MeV\ntotal charge deposited is "\
                        + str(round(np.array(c[j]).sum(), 3)) + "\ntotal deposited energy is: "\
                        + str(round(np.array(c[j]).sum() * 3.62/pow(10, 6), 3)) + "MeV"

                ax.set_title(title)

                plt.savefig("./2Dimages/" + str(self.pid) + "/" + str(round(numerica_e/pow(10, 6), 4)) + "MeV/" + str(j) + ".png", bbox_inches='tight')

                plt.close()




energy = np.logspace(4, 10, 100)

energy_list = []

for ene in energy:
    energy_list.append(str(ene/pow(10, 6))+"MeV")

theta = '45'
phi = '0'
particle_type = 'e-'

thickness = 26.3

a = DECOLeptonAnalyzer(particle_type, phi, thickness)

E_calibrate_list = []
err_list = []
E_exp_list = []

for i in range(len(energy)):

    print("working on " + str(round(energy[i]/pow(10, 6), 4)) + "MeV")

    a.plot_single(energy_list[i], energy[i], theta, 20)


