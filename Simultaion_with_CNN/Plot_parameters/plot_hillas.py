import numpy as np
import os, sys
import matplotlib.pylab as plt
plt.style.use('IceCube')
import matplotlib.pyplot as plt
from math import *

# from Brent, calculate Hillas parameters of events
#charge_coords = [[x_coords], [y_coords], [charges]]
def hillas(charge_coords):
    #print(charge_coords.shape)
    x = 0
    y = 0
    x2 = 0
    y2 = 0
    xy = 0
    CHARGE = 0
    #print(charge_coords.shape)
    CHARGE = np.sum(charge_coords[2])
    x = np.sum(charge_coords[0] * charge_coords[2])
    y = np.sum(charge_coords[1] * charge_coords[2])
    x2 = np.sum(charge_coords[0] ** 2 * charge_coords[2])
    y2 = np.sum(charge_coords[1] ** 2 * charge_coords[2])
    xy = np.sum(charge_coords[0] * charge_coords[1] * charge_coords[2])
    x /= CHARGE
    y /= CHARGE
    x2 /= CHARGE
    y2 /= CHARGE
    xy /= CHARGE
    S2_x = x2 - x ** 2
    S2_y = y2 - y ** 2
    S_xy = xy - x * y
    d = S2_y - S2_x
    a = (d + np.sqrt(d ** 2 + 4 * S_xy ** 2)) / (2 * S_xy)
    b = y - a * x
    width = np.sqrt((S2_y + a ** 2 * S2_x - 2 * a * S_xy) / (1 + a ** 2))
    length = np.sqrt((S2_x + a ** 2 * S2_y + 2 * a * S_xy) / (1 + a ** 2))
    miss = np.abs(b / np.sqrt(1 + a ** 2))
    dis = np.sqrt(x ** 2 + y ** 2)
    q_coord = (x - charge_coords[0]) * (x / dis) + (y - charge_coords[1]) * (y / dis)
    q = np.sum(q_coord * charge_coords[2]) / CHARGE
    q2 = np.sum(q_coord ** 2 * charge_coords[2]) / CHARGE
    azwidth = q2 - q ** 2

    return [width, length, miss, dis, azwidth]


# convert a 64x64 charge deposited plot or real deco image into shape of [[x_coords], [y_coords], [charges]]
def convert_hillas(filename):
    f = open(filename, 'r')

    y_list = []
    x_list = []
    charge_list = []

    y_pos = 0.0

    while 1:

        temp = f.readline().split()

        if len(temp) < 1:
            break

        x_pos = 0.0

        for num in temp:
            x_list.append(x_pos)
            y_list.append(y_pos)

            if float(num) >= 5.0:
                charge_list.append(float(num))
            else:
                charge_list.append(0.0)

            x_pos += 1.0

        y_pos += 1.0

    y_list = len(y_list) - np.array(y_list) - 1
    x_list = np.array(x_list)
    charge_list = np.array(charge_list)


    return [x_list, y_list, charge_list]


#print hillas(convert_hillas("./output/mu+_2Dimages/1.0004537985GeV_theta_57.0_phi_75.9_thickiness_26.3_highstats.txt"))

"""
extracting cnn classified data
"""
width_list_cnn = []
length_list_cnn = []
count = 0


for filename in os.listdir("../MC_z_clean_img/real_clean_image_thres10/"):
    if filename.endswith(".txt"):
        print(count)
        count += 1
        try :
            result = hillas(convert_hillas("../MC_z_clean_img/real_clean_image_thres10/" + filename))

            width_list_cnn.append(log10(result[0]))
            length_list_cnn.append(log10(result[1]))
            # if log10(result[0]) > 0.4:
            #     print filename
        except:
            pass




"""
extracting simulated data
"""

def getdata_sim(file_dir):
    width_list_sim3 = []
    length_list_sim3 = []
    count = 0

    for filename in os.listdir(file_dir):

        if filename.endswith(".txt"):

            try:
                result = hillas(convert_hillas(file_dir + "/" + filename))

                width_list_sim3.append(log10(result[0]))
                length_list_sim3.append(log10(result[1]))

                count += 1
            except:
                pass

    return width_list_sim3, length_list_sim3, count



folder_dir = "qdc_res_0_smear_0_slope_4"
source_dir = "mu+_2Dimages_fac2"
file_dir = "../MC_z_clean_img/sim_clean_image_thres10/" + str(folder_dir) + "/" + str(source_dir)
width_list_sim5, length_list_sim5, count5 = getdata_sim(file_dir)


folder_dir = "qdc_res_0_smear_0_slope_3"
source_dir = "mu+_2Dimages_fac2"
file_dir = "../MC_z_clean_img/sim_clean_image_thres10/" + str(folder_dir) + "/" + str(source_dir)
width_list_sim25, length_list_sim25, count25 = getdata_sim(file_dir)


folder_dir = "qdc_res_0_smear_0_slope_5"
source_dir = "mu+_2Dimages_fac2"
file_dir = "../MC_z_clean_img/sim_clean_image_thres10/" + str(folder_dir) + "/" + str(source_dir)
width_list_sim100, length_list_sim100, count100 = getdata_sim(file_dir)


f = plt.figure()

plt.hist(width_list_cnn, bins=np.linspace(-0.2, 0.7, 41), weights=np.zeros(len(width_list_cnn)) + (1 / count), label='real events', alpha=0.5)

plt.hist(width_list_sim5, bins=np.linspace(-0.2, 0.7, 41), weights=np.zeros(len(width_list_sim5)) + (1 / count5), label='simulation with bias voltage -5V', histtype='step', lw=5)
plt.hist(width_list_sim25, bins=np.linspace(-0.2, 0.7, 41), weights=np.zeros(len(width_list_sim25)) + (1 / count25), label='simulation with bias voltage -25V', histtype='step', lw=5, color='black')
plt.hist(width_list_sim100, bins=np.linspace(-0.2, 0.7, 41), weights=np.zeros(len(width_list_sim100)) + (1 / count100), label='simulation with bias voltage -100V', histtype='step', lw=5)


plt.legend()
plt.xlabel("log10(width / pixel)")
plt.ylabel("# images normalized")
#plt.xscale('log')
#plt.yscale('log')



f2 = plt.figure()

plt.hist(length_list_cnn, bins=np.linspace(0, 1.5, 31), weights=np.zeros(len(width_list_cnn)) + (1 / count), label='real events', alpha=0.5)

plt.hist(length_list_sim5, bins=np.linspace(0, 1.5, 31), weights=np.zeros(len(width_list_sim5)) + (1 / count5), label='simulation with bias voltage -5V', histtype='step', lw=5)
plt.hist(length_list_sim25, bins=np.linspace(0, 1.5, 31), weights=np.zeros(len(width_list_sim25)) + (1 / count25), label='simulation with bias voltage -25V', histtype='step', lw=5, color='black')
plt.hist(length_list_sim100, bins=np.linspace(0, 1.5, 31), weights=np.zeros(len(width_list_sim100)) + (1 / count100), label='simulation with bias voltage -100V', histtype='step', lw=5)


plt.legend()
plt.xlabel("log10(length / pixel)")
plt.ylabel("# images normalized")
#plt.yscale('log')
#plt.xscale('log')



plt.show()

