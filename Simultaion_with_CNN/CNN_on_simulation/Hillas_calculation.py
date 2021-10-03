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
def convert_hillas(filename, is_sim):
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

            if float(num) >= 10.0:
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

model = 'Dalvik_1.4.0_(Linux;_U;_Android_2.3.4;_HTC_A510c_Build_GRJ22)'


for filename in os.listdir("../CNN_on_training_data/track_by_device_full/" + str(model) + "/track/"):
    if filename.endswith(".txt"):
        print(count)
        count += 1
        try :
            result = hillas(convert_hillas("../CNN_on_training_data/track_by_device_full/" + str(model) + "/track/" + filename, False))

            width_list_cnn.append(log10(result[0]))
            length_list_cnn.append(log10(result[1]))
            # if log10(result[0]) > 0.4:
            #     print filename
        except:
            pass




"""
extracting simulated data
"""
file_dir = "qdc_res_0_smear_0_slope_1"
source_dir = 'mu+_2Dimages_fac1_dev0_condev0'

width_list_sim1 = []
length_list_sim1 = []
count = 0

E_min = 0
zen_min = 0

for filename in os.listdir("./classification/" + file_dir + '/' + source_dir + "/track/"):

    if filename.endswith(".txt"):

        energy = float(filename.split("_")[0][:-3])
        zenith = float(filename.split("_")[2])

        try:
            result = hillas(convert_hillas("./classification/" + file_dir + '/' + source_dir + "/track/" + filename, True))

            width_list_sim1.append(log10(result[0]))
            length_list_sim1.append(log10(result[1]))
        except:
            pass


file_dir = "qdc_res_0_smear_0_slope_2"
source_dir = 'mu+_2Dimages_fac1_dev0_condev0'
width_list_sim2 = []
length_list_sim2 = []
count = 0

E_min = 0
zen_min = 0

for filename in os.listdir("./classification/" + file_dir + '/' + source_dir + "/track/"):

    if filename.endswith(".txt"):

        energy = float(filename.split("_")[0][:-3])
        zenith = float(filename.split("_")[2])

        try:
            result = hillas(convert_hillas("./classification/" + file_dir + '/' + source_dir + "/track/" + filename, True))

            width_list_sim2.append(log10(result[0]))
            length_list_sim2.append(log10(result[1]))
        except:
            pass


file_dir = "qdc_res_0_smear_0_slope_7"
source_dir = 'mu+_2Dimages_fac1.5_dev0_condev0'
width_list_sim3 = []
length_list_sim3 = []
count = 0

E_min = 0
zen_min = 0

for filename in os.listdir("./classification/" + file_dir + '/' + source_dir + "/track/"):

    if filename.endswith(".txt"):

        energy = float(filename.split("_")[0][:-3])
        zenith = float(filename.split("_")[2])

        try:
            result = hillas(convert_hillas("./classification/" + file_dir + '/' + source_dir + "/track/" + filename, True))

            width_list_sim3.append(log10(result[0]))
            length_list_sim3.append(log10(result[1]))
        except:
            pass


f = plt.figure()

plt.hist(width_list_cnn, bins=100, density=True, histtype='step', lw=3, label='real track events')
#plt.hist(width_list_train, bins=100, density=True, alpha=0.5, range=(-0.5, 1), label='training')
# plt.hist(width_list_sim1, bins=100, density=True, alpha=0.5, range=(-0.5, 1), label='sim, bias = -20')
# plt.hist(width_list_sim2, bins=100, density=True, alpha=0.5, range=(-0.5, 1), label='sim, bias = -5')
plt.hist(width_list_sim3, bins=100, density=True, alpha=0.5, range=(-0.5, 1), label='sim')
plt.legend()
plt.xlabel("log10(width / pixel)")
plt.ylabel("normalized #")
#plt.xscale('log')

f2 = plt.figure()

plt.hist(length_list_cnn, bins=100, density=True, histtype='step', lw=3, label='real track events')
#plt.hist(length_list_train, bins=100, density=True, alpha=0.5, range=(0, 1.5), label='training')
# plt.hist(length_list_sim1, bins=100, density=True, alpha=0.5, range=(0, 1.5), label='sim, bias = -20')
# plt.hist(length_list_sim2, bins=100, density=True, alpha=0.5, range=(0, 1.5), label='sim, bias = -5')
plt.hist(length_list_sim3, bins=100, density=True, alpha=0.5, range=(0, 1.5), label='sim')
plt.legend()
plt.xlabel("log10(length / pixel)")
plt.ylabel("normalized #")
#plt.xscale('log')

plt.show()

