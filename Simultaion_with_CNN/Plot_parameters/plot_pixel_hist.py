import matplotlib.pylab as plt
from math import *
import numpy as np
plt.style.use("IceCube")
import os, sys

def getdata(filename, if_sim):
    f = open(filename, 'r')

    output = []

    while 1:
        temp = f.readline().split()

        if len(temp) < 1:
            break

        for num in temp:
            if float(num) > 0:
                output.append(float(num))

    return np.array(output), np.array(output).max()


output_total_cnn = np.array([])
output_max_cnn = []
output_sum = []
count_real = 0

for filename in os.listdir("../MC_z_clean_img/real_clean_image_thres10/"):
    if filename.endswith(".txt"):

        output, max_lum = getdata("../MC_z_clean_img/real_clean_image_thres10/" + filename, False)
        output_max_cnn.append(max_lum)
        output_sum.append(output.sum())
        if output.sum() > 10000:
            print(filename)
        output_total_cnn = np.concatenate((output_total_cnn, output))
        count_real += 1

def getdata_sim(file_dir):

    output_total_sim2 = np.array([])
    output_max_sim2 = []
    output_sum_sim2 = []

    count_1 = 0

    for filename in os.listdir(file_dir):
        if filename.endswith(".txt"):

            print(count_1)

            count_1 += 1


            output, max_lum = getdata(file_dir + "/" + filename, True)
            output_max_sim2.append(max_lum)
            output_sum_sim2.append(output.sum())

            output_total_sim2 = np.concatenate((output_total_sim2, output))

    return output_total_sim2, output_max_sim2 ,output_sum_sim2, count_1


folder_dir = "qdc_res_0_smear_0_slope_4"
source_dir = "mu+_2Dimages_fac2"
file_dir = "../MC_z_clean_img/sim_clean_image_thres10/" + str(folder_dir) + "/" + str(source_dir)
output_total_sim5, output_max_sim5 ,output_sum_sim5, count5 = getdata_sim(file_dir)



folder_dir = "qdc_res_0_smear_0_slope_3"
source_dir = "mu+_2Dimages_fac2"
file_dir = "../MC_z_clean_img/sim_clean_image_thres10/" + str(folder_dir) + "/" + str(source_dir)
output_total_sim25, output_max_sim25 ,output_sum_sim25, count25 = getdata_sim(file_dir)


folder_dir = "qdc_res_0_smear_0_slope_5"
source_dir = "mu+_2Dimages_fac2"
file_dir = "../MC_z_clean_img/sim_clean_image_thres10/" + str(folder_dir) + "/" + str(source_dir)
output_total_sim100, output_max_sim100 ,output_sum_sim100, count100 = getdata_sim(file_dir)




f = plt.figure()

plt.hist(output_total_cnn, bins=np.linspace(0, 255, 86), weights=np.zeros(len(output_total_cnn)) + (1 / count_real), alpha=0.5, label='real events')

plt.hist(output_total_sim5, bins=np.linspace(0, 255, 86), weights=np.zeros(len(output_total_sim5)) + (1 / count5), histtype='step', label='simulation with bias voltage -5V', lw=5)
plt.hist(output_total_sim25, bins=np.linspace(0, 255, 86), weights=np.zeros(len(output_total_sim25)) + (1 / count25), histtype='step', label='simulation with bias voltage -25V', lw=5, color='black')
plt.hist(output_total_sim100, bins=np.linspace(0, 255, 86), weights=np.zeros(len(output_total_sim100)) + (1 / count100), histtype='step', label='simulation with bias voltage -100V', lw=5)

plt.legend()
plt.xlabel("Luminance on pixel")
plt.yscale('log')
plt.ylabel("# pixels normalized")




f2 = plt.figure()

plt.hist(output_max_cnn, bins=np.linspace(0, 255, 26), weights=np.zeros(len(output_max_cnn)) + (1 / count_real), alpha=0.5, label='real events')

plt.hist(output_max_sim5, bins=np.linspace(0, 255, 26), weights=np.zeros(len(output_max_sim5)) + (1 / count5), histtype='step', label='simulation with bias voltage -5V', lw=5)
plt.hist(output_max_sim25, bins=np.linspace(0, 255, 26), weights=np.zeros(len(output_max_sim25)) + (1 / count25), histtype='step', label='simulation with bias voltage -25V', lw=5, color='black')
plt.hist(output_max_sim100, bins=np.linspace(0, 255, 26), weights=np.zeros(len(output_max_sim100)) + (1 / count100), histtype='step', label='simulation with bias voltage -100V', lw=5)

plt.legend()
plt.xlabel("Brightest luminance on pixel")
plt.ylabel("# images normalized")
#plt.yscale('log')






f3 = plt.figure()



plt.hist(output_sum, bins=np.logspace(3, 4.5, 41), weights=np.zeros(len(output_sum)) + (1 / count_real), alpha=0.5, label='real events')

plt.hist(output_sum_sim5, bins=np.logspace(3, 4.5, 41), weights=np.zeros(len(output_sum_sim5)) + (1 / count5), histtype='step', label='simulation with bias voltage -5V', lw=5)
plt.hist(output_sum_sim25, bins=np.logspace(3, 4.5, 41), weights=np.zeros(len(output_sum_sim25)) + (1 / count25), histtype='step', label='simulation with bias voltage -25V', lw=5, color='black')
plt.hist(output_sum_sim100, bins=np.logspace(3, 4.5, 41), weights=np.zeros(len(output_sum_sim100)) + (1 / count100), histtype='step', label='simulation with bias voltage -100V', lw=5)

plt.xscale('log')
plt.legend()
plt.xlabel("Luminance summation")
plt.ylabel("# images normalized")





plt.show()

