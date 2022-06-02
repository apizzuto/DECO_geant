import numpy as np
from math import *
import matplotlib.pylab as plt
from PIL import Image
import os, sys


def getImage(filename):

    f_reader = open(filename, 'r')
    image = []
    while 1:
        temp = f_reader.readline().split()
        temp_hold = []
        if len(temp) < 1:
            break

        for content in temp:
            temp_hold.append(float(content))

        image.append(temp_hold)

    image = np.array(image)

    return image


def clean_img(filename):

    image = getImage(filename)

    noise_matrix = np.zeros((5, 5)) + threshold

    a = 0.2138
    b = 0.479
    c = 0.985
    aperture = [[0., a, b, a, 0.],
                [a, c, 1., c, a],
                [b, 1., 1., 1., b],
                [a, c, 1., c, a],
                [0., a, b, a, 0.]]

    aperture = np.array(aperture)

    image_pad = np.zeros((len(image) + 4, len(image[0]) + 4))

    for i in range(len(image_pad))[2:-2]:
        for j in range(len(image_pad[0]))[2:-2]:

            image_pad[i][j] = image[i-2][j-2]


    for i in range(len(image_pad))[2:-2]:
        for j in range(len(image_pad[0]))[2:-2]:

            luminance = np.sum(image_pad[i-2:i + 3, j-2:j + 3] * aperture)

            if luminance <= np.sum(noise_matrix * aperture):
                image[i-2][j-2] = 0


    return image


# threshold of image cleaning
threshold = 10


if not os.path.exists("./real_clean_worm_thres" + str(threshold)):
    os.mkdir("./real_clean_worm_thres" + str(threshold))

file_dir = "../CNN_on_training_data/Worm_data/HTC_A510c/"

for filename in os.listdir(file_dir):

    print(filename)

    clean_image = clean_img(file_dir + filename)

    f = open("./real_clean_worm_thres" + str(threshold) + "/" + filename, 'w')

    for i in range(len(clean_image)):
        for j in range(len(clean_image[i])):
            f.write(str(int(clean_image[i][j])) + " ")

        f.write("\n")



