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

    def __init__(self, pid, energy_levels, en_float, theta_list, phi_list, thickness):
        self.pid = pid

        self.thichness = thickness

        self.col_names = ['Energy', 'Theta (degrees)', 'Phi', 'Deposited Charge ($N_{e^{-}}$)',
                     'Energy (GeV)', 'Track Length (pixels)', 'Charge per unit length']

        self.energy_levels = energy_levels

        self.en_float = en_float

        self.theta_list = theta_list

        self.phi_list = phi_list

        self.data_list = self.data_processing()


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

    """
    return the distance by L2 norm of (x_max_diff, y_max_diff)
    """
    def track_length(self, x, y):
        x_dist_sq = np.power((np.max(x) - np.min(x)) * 0.9, 2.)
        y_dist_sq = np.power((np.max(y) - np.min(y)) * 0.9, 2.)
        return np.power(x_dist_sq + y_dist_sq, 0.5)

    """
    dE/dx in unit of MeV/cm
    """
    def get_dEdx(self, M, E, Z, type):
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



    def data_processing(self):

        self.check_if_all_simulated()

        data_list = pd.DataFrame(columns=self.col_names)

        counter = 0
        curr_energy = 0
        for en in self.energy_levels:
            for theta in self.theta_list:
                for phi in self.phi_list:
                    x, y, c = self.read_hit_file("./output/{}/{}_theta_{}_phi_{}_thickiness_{}_highstats.txt".format(self.pid, en, float(theta), float(phi), self.thichness))
                    try:
                        for j in range(len(x)):
                            charge = np.sum(c[j])
                            length = self.track_length(x[j], y[j])
                            dQ_dX = charge / np.power(length ** 2 + self.thichness ** 2, 0.5)
                            data_list.loc[counter] = [en, theta, phi, charge, self.en_float[curr_energy], length, dQ_dX]
                            counter += 1
                    except:
                        continue
            curr_energy += 1
        return data_list


    def plot_single(self, en, theta, phi):
        x, y, c = self.read_hit_file(
            "./output/{}/{}_theta_{}_phi_{}_thickiness_{}_highstats.txt".format(self.pid, en, float(theta),
                                                                                float(phi), self.thichness))

        for j in range(50):
            # try:
            image = np.zeros((4500, 4500))
            for i in range(len(x[j])):
                image[int(y[j][i]), int(x[j][i])] = c[j][i]


            med_x = np.median(x[j])
            med_y = np.median(y[j])
            size = 50.

            title = "1 GeV $\mu^{+}$"
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
            ax.set_title(title)

            ax.grid(color="#ffffff")
            cb = fig1.colorbar(im, orientation="vertical",
                               shrink=0.8,
                               fraction=0.05,
                               pad=0.15)
            label = "Pixel Luminance"
            cb.set_label(label)
            ax.text(med_x + size * 0.3, med_y + size * 0.7,
                    "Simulation", fontsize=24, color='w', weight='heavy')
            plt.show()

    def bethe_bloch_plot(self):

        me = .511
        E_array = np.logspace(-2., 4., 100)
        BB = []

        for E in E_array:

            if self.pid == 'mu+' or self.pid == 'mu-':
                BB.append(self.get_dEdx(206.7 * me, E, 1., self.pid))
            elif self.pid == 'e+' or self.pid == 'e-':
                BB.append(self.get_dEdx(me, E, 1., self.pid))



        BB = np.array(BB)

        #todo: may change this /2 if counting hole charge is possible
        BB = BB * 1e6 / 2 * (1. / 3.62) * 1e-4  # convert from MeV / cm to electron charge per um


        fig, ax = plt.subplots(figsize=(9, 6))


        my_cmap = ListedColormap(sns.color_palette("Blues", 50))
        fig.set_facecolor('white')

        h = plt.hist2d(np.log10(self.data_list['Energy (GeV)']), np.log10(self.data_list['Charge per unit length']),
                       bins=[np.linspace(-1., 5., 14), np.linspace(1.5, 3.5, 35)], cmin=1., cmap=my_cmap)
        plt.colorbar(label="Number of Events")
        plt.title(str(self.pid) + " Losses")
        plt.plot(np.log10(E_array), np.log10(BB), c='r', label="Bethe-Bloch", lw=3)
        plt.ylabel(r'$\log (\frac{dQ}{dx} \times \frac{0.9 \mu m}{q_{e}})$', fontsize=26)
        plt.xlabel('$\log$( $E_{' + str(self.pid) + '}$ / MeV) ')
        #plt.xlim(-2, 4.2)
        #plt.ylim(1.5, 3.25)
        plt.show()


    def check_if_all_simulated(self):

        missing_list = []
        for en in self.energy_levels:
            for theta in self.theta_list:
                for phi in self.phi_list:

                    curr_file_name = "./output/{}/{}_theta_{}_phi_{}_thickiness_{}_highstats.txt".format(
                        self.pid, en, float(theta), float(phi), self.thichness)

                    if not os.path.exists(curr_file_name):
                        missing_list.append(curr_file_name)

        if len(missing_list) == 0:
            print("find all required files:")
            return

        else:
            print("missing following files:\n")
            for i in range(len(missing_list)):
                print(missing_list[i])

            print("\nmissing files exist, stop analyzing")

            exit()
            return


    def track_length_vs_angle_violinplot(self):
        fig, ax = plt.subplots(figsize=(8, 6))

        my_pal = {'100MeV': sns.color_palette('colorblind')[0],
                  '10GeV': sns.color_palette('colorblind')[2]}

        curr_data = pd.DataFrame(columns=self.col_names)

        index = 0
        for i in range(self.data_list.__len__()):
            if self.data_list.loc[i]['Energy'] == '100MeV' or self.data_list.loc[i]['Energy'] == '10GeV':
                if self.data_list.loc[i]['Track Length (pixels)'] <= 250:
                    curr_data.loc[index] = self.data_list.loc[i]
                    index += 1

        sns.violinplot(x="Theta (degrees)", y="Track Length (pixels)", hue="Energy",
                       data=curr_data, palette=my_pal, split=True)

        plt.axhline(0., c='r', xmin=0.03, xmax=0.14, lw=3)
        plt.axhline((26.3 / 0.9) * np.tan(15. * np.pi / 180.), c='r', xmin=0.18, xmax=0.32, lw=3)
        plt.axhline((26.3 / 0.9) * np.tan(30. * np.pi / 180.), c='r', xmin=0.35, xmax=0.48, lw=3)
        plt.axhline((26.3 / 0.9) * np.tan(45. * np.pi / 180.), c='r', xmin=0.52, xmax=0.64, lw=3)
        plt.axhline((26.3 / 0.9) * np.tan(60. * np.pi / 180.), c='r', xmin=0.68, xmax=0.82, lw=3)
        plt.axhline((26.3 / 0.9) * np.tan(75. * np.pi / 180.), c='r', xmin=0.85, xmax=0.98, lw=3)

        plt.legend(loc=2)
        #plt.ylim(2, 150.)
        #plt.yscale('symlog')
        plt.show()


    def hillas_length_histogram(self):
        pass

    def hillas_width_histogram(self):
        pass


energy_levels = ['10keV', '31.6keV', '100keV', '316keV', '1MeV', '3.16MeV',
               '10MeV', '31.6MeV', '100MeV', '316MeV', '1GeV', '3.16GeV', '10GeV']
en_float = np.logspace(-2., 4, 13)

theta_list = ['0', '15', '30', '45', '60', '75']

#phi_list = ['0', '15', '30', '45', '60', '75', '90']

phi_list = ['0']

thickness = 26.3

a = DECOLeptonAnalyzer('e-', energy_levels, en_float, theta_list, phi_list, thickness)

#a.track_length_vs_angle_violinplot()
a.bethe_bloch_plot()

#a.plot_single('1GeV', '75')
#x, y, c = a.read_hit_file('./output/mu+/100KeV_theta_45.0_phi_30.0_thickiness_26.3_highstats.txt')

