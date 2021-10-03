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
            if float(num) > 10:
                output.append(float(num))


    return np.array(output), np.array(output).max()


output_total_cnn = np.array([])
output_max_cnn = []
output_sum = []
model = 'Dalvik_1.4.0_(Linux;_U;_Android_2.3.4;_HTC_A510c_Build_GRJ22)'
count_real = 0

for filename in os.listdir("../CNN_on_training_data/track_by_device_full/" + str(model) + "/track/"):
    if filename.endswith(".txt"):

        output, max_lum = getdata("../CNN_on_training_data/track_by_device_full/" + str(model) + "/track/" + filename, False)
        output_max_cnn.append(max_lum)
        output_sum.append(output.sum())
        output_total_cnn = np.concatenate((output_total_cnn, output))
        count_real += 1

def getdata_sim(file_dir, source_dir):
    E_min = 0
    zen_min = 0
    zen_max = 90

    output_total_sim2 = np.array([])
    output_max_sim2 = []
    output_sum_sim2 = []

    count_1 = 0

    for filename in os.listdir("./classification/" + str(file_dir) + "/" + str(source_dir) + "/track/"):
        if filename.endswith(".txt"):

            print count_1

            count_1 += 1

            energy = float(filename.split("_")[0][:-3])
            zenith = float(filename.split("_")[2])

            if energy >= E_min and zenith >= zen_min and zenith <= zen_max:

                output, max_lum = getdata("./classification/" + str(file_dir) + "/" + str(source_dir) + "/track/" + filename, True)
                output_max_sim2.append(max_lum)
                output_sum_sim2.append(output.sum())
                if output.sum() > 20000:
                    print filename
                output_total_sim2 = np.concatenate((output_total_sim2, output))

    return output_total_sim2, output_max_sim2 ,output_sum_sim2, count_1


# file_dir = "qdc_res_0_smear_0_slope_1"
# source_dir = "mu+_2Dimages_fac1_dev0_condev0"
# output_total_sim1, output_max_sim1 ,output_sum_sim1, count1 = getdata_sim(file_dir, source_dir)
#
#
# file_dir = "qdc_res_0_smear_0_slope_4"
# source_dir = "mu+_2Dimages_fac1_dev0_condev0"
# output_total_sim2, output_max_sim2 ,output_sum_sim2, count2 = getdata_sim(file_dir, source_dir)

file_dir = "qdc_res_0_smear_0_slope_7"
source_dir = "mu+_2Dimages_fac1.5_dev0_condev0"
output_total_sim3, output_max_sim3 ,output_sum_sim3, count3 = getdata_sim(file_dir, source_dir)


f = plt.figure()

#plt.hist(output_total_sim1, bins=np.linspace(0, 255, 86), density=True, lw=3, label='0', histtype='step')
hist, edge = np.histogram(output_total_cnn, bins=np.linspace(0, 255, 86)) # , density=True, lw=3, label='sim', histtype='step')
# hist1, edge1 = np.histogram(output_total_sim1, bins=np.linspace(0, 255, 86)) # , density=True, lw=3, label='sim', histtype='step')
# hist2, edge2 = np.histogram(output_total_sim2, bins=np.linspace(0, 255, 86)) #, density=True, lw=3, label='real track events', histtype='step')
hist3, edge3 = np.histogram(output_total_sim3, bins=np.linspace(0, 255, 86)) #, density=True, lw=3, label='real track events', histtype='step')

# plt.plot(edge1, np.insert(hist1, 0, hist1[0])/float(count1), '-', drawstyle='steps', label='simulated events dep = -10')
# plt.plot(edge2, np.insert(hist2, 0, hist2[0])/float(count2), '-', drawstyle='steps', label='simulated events dep = -5')
plt.plot(edge, np.insert(hist, 0, hist[0])/float(count_real), '-', drawstyle='steps', label='real track events')
plt.plot(edge3, np.insert(hist3, 0, hist3[0])/float(count3), '-', drawstyle='steps', label='sim')

plt.legend()
plt.xlabel("charge / luminance on pixel")
plt.yscale('log')
plt.ylabel("# normalized")

#, histtype='step'

f2 = plt.figure()

# plt.hist(output_max_sim1, bins=np.linspace(0, 255, 86), density=True, alpha=0.5, label='sim, dep = -10')
# plt.hist(output_max_sim2, bins=np.linspace(0, 255, 86), density=True, alpha=0.5, label='sim, dep = -5')
plt.hist(output_max_sim3, bins=np.linspace(0, 255, 86), density=True, alpha=0.5, label='sim')
plt.hist(output_max_cnn, bins=np.linspace(0, 255, 86), density=True, lw=3, label='real track events', histtype='step')
plt.legend()
plt.xlabel("largest charge / brightest luminance on pixel")
plt.ylabel("# normalized")
plt.yscale('log')


f3 = plt.figure()

# plt.hist(output_sum_sim1, bins=np.linspace(0, 20000, 101), density=True, alpha=0.5, label='sim, dep = -10')
# plt.hist(output_sum_sim2, bins=np.linspace(0, 20000, 101), density=True, alpha=0.5, label='sim, dep = -5')
plt.hist(output_sum_sim3, bins=np.linspace(0, 20000, 101), density=True, alpha=0.5, label='sim')
plt.hist(output_sum, bins=np.linspace(0, 20000, 101), density=True, lw=3, label='real track events', histtype='step')
plt.legend()
plt.xlabel("Luminance summation")
plt.ylabel("# normalized")
#plt.yscale('log')

plt.show()

