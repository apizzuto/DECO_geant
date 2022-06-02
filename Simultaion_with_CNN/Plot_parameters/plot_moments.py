import matplotlib.pylab as plt
from math import *
import numpy as np
plt.style.use("IceCube")
import os, sys

def getdata(filename):
    f = open(filename, 'r')

    output = []

    while 1:
        temp = f.readline().split()

        if len(temp) < 1:
            break

        for num in temp:
            if float(num) != 0:
                output.append(float(num))

    return np.array(output)




count = 0
x_sig_real = []
x_mean_real = []
for filename in os.listdir("../MC_z_clean_img/real_clean_image_thres10/"):
    output = getdata("../MC_z_clean_img/real_clean_image_thres10/" + filename)
    x_sig_real.append(np.sqrt(np.power(output, 2).mean() - output.mean()**2))
    x_mean_real.append(output.mean())
    count += 1
    print(count)


def getdata_sim(file_dir):

    count = 0
    x_sig_sim = []
    x_mean_sim = []

    for filename in os.listdir(file_dir):
        output = getdata(file_dir + "/" + filename)
        x_sig_sim.append(np.sqrt(np.power(output, 2).mean() - output.mean()**2))
        x_mean_sim.append(output.mean())
        count += 1
        print(count)

    return x_sig_sim, x_mean_sim, count


folder_dir = "qdc_res_0_smear_0_slope_4"
source_dir = "mu+_2Dimages_fac2"
file_dir = "../MC_z_clean_img/sim_clean_image_thres10/" + str(folder_dir) + "/" + str(source_dir)
x_sig_sim5, x_mean_sim5, count5 = getdata_sim(file_dir)


folder_dir = "qdc_res_0_smear_0_slope_3"
source_dir = "mu+_2Dimages_fac2"
file_dir = "../MC_z_clean_img/sim_clean_image_thres10/" + str(folder_dir) + "/" + str(source_dir)
x_sig_sim25, x_mean_sim25, count25 = getdata_sim(file_dir)


folder_dir = "qdc_res_0_smear_0_slope_5"
source_dir = "mu+_2Dimages_fac2"
file_dir = "../MC_z_clean_img/sim_clean_image_thres10/" + str(folder_dir) + "/" + str(source_dir)
x_sig_sim100, x_mean_sim100, count100 = getdata_sim(file_dir)


f = plt.figure()

plt.hist(x_sig_real, bins=np.linspace(0, 80, 41), weights=np.zeros(len(x_sig_real)) + (1 / count), label='real events', alpha=0.5)

plt.hist(x_sig_sim5, bins=np.linspace(0, 80, 41), weights=np.zeros(len(x_sig_sim5)) + (1 / count5), label='simulation with bias voltage -5V', histtype='step', lw=5)
plt.hist(x_sig_sim25, bins=np.linspace(0, 80, 41), weights=np.zeros(len(x_sig_sim25)) + (1 / count25), label='simulation with bias voltage -25V', histtype='step', lw=5, color='black')
plt.hist(x_sig_sim100, bins=np.linspace(0, 80, 41), weights=np.zeros(len(x_sig_sim100)) + (1 / count100), label='simulation with bias voltage -100V', histtype='step', lw=5)

plt.legend()
plt.xlabel(r"$\sigma_L$")
plt.ylabel("# images normalized")




f2 = plt.figure()

plt.hist(np.array(x_sig_real)/np.array(x_mean_real), bins=np.linspace(0.5, 1.5, 41), weights=np.zeros(len(x_sig_real)) + (1 / count), label='real events', alpha=0.5)

plt.hist(np.array(x_sig_sim5)/np.array(x_mean_sim5), bins=np.linspace(0.5, 1.5, 41), weights=np.zeros(len(x_sig_sim5)) + (1 / count5), label='simulation with bias voltage -5V', histtype='step', lw=5)
plt.hist(np.array(x_sig_sim25)/np.array(x_mean_sim25), bins=np.linspace(0.5, 1.5, 41), weights=np.zeros(len(x_sig_sim25)) + (1 / count25), label='simulation with bias voltage -25V', histtype='step', lw=5, color='black')
plt.hist(np.array(x_sig_sim100)/np.array(x_mean_sim100), bins=np.linspace(0.5, 1.5, 41), weights=np.zeros(len(x_sig_sim100)) + (1 / count100), label='simulation with bias voltage -100V', histtype='step', lw=5)

plt.legend()
plt.xlabel(r"$\frac{\sigma_L}{<L>}$")
plt.ylabel("# images normalized")

plt.show()


