import numpy as np
import os
from math import *
from skimage import *
from PIL import Image, ImageEnhance

"""
for HTC A510 we have a 2592x1944 CMOS sensor, we assign Bayer filter as:
green red
blue  green
so for a pixel at (x, y), if x % 2 == 0 and y % 2 == 0 it is blue, if x % 2 == 1 and y % 2 == 1 it is red
"""
def getlabel(posx, posy):

    if posx % 2 == 0 and posy % 2 == 0:
        return 'b'
    elif posx % 2 == 1 and posy % 2 == 1:
        return 'r'
    else:
        return 'g'

"""get the background data"""
def getdata(filename):
    f = open(filename, 'r')

    output = []

    while 1:
        temp = f.readline().split()

        output_temp = []

        if len(temp) < 1:
            break

        for num in temp:
            output_temp.append(float(num))

        output.append(output_temp)

    return np.array(output)


"""check if the event is on the edge of image"""
def pass_edge_check(maxX, maxY, img_shape, crop_size=64):
    """checks if image is on the edge of the sensor"""
    x0, x1, y0, y1 = get_crop_range(maxX, maxY, size=crop_size / 2)
    checks = np.array([x0 >= 0, x1 <= img_shape[0], y0 >= 0, y1 <= img_shape[1]])
    return checks.all() == True


"""check the range to crop 64x64 image"""
def get_crop_range(maxX, maxY, size=32):
    """define region of image to crop"""
    return maxX - size, maxX + size, maxY - size, maxY + size


"""find the brightest pixel, since image crop is centered at the brightest point"""
def get_brightest_pixel(img):
    """get brightest image pixel indices"""
    img = np.array(img)
    return np.unravel_index(img.argmax(), img.shape)


"""read the output file from simulation"""
def read_hit_file(filename):
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


"""Color interpolation using mean algorithm and Bayer filter"""
def color_processing(image_arr):

    new_img = np.zeros((64, 64, 3))

    for i in range(len(image_arr)):
        for j in range(len(image_arr[i])):

            """do not work on edge pixels"""
            if i == 0 or i == len(image_arr) - 1:
                continue
            if j == 0 or j == len(image_arr[i]) - 1:
                continue

            label = getlabel(j, i)

            if label == 'r':
                r = image_arr[i][j]
                g = float(image_arr[i - 1][j] + image_arr[i + 1][j] + image_arr[i][j - 1] + image_arr[i][j + 1])/4
                b = float(image_arr[i-1][j-1] + image_arr[i + 1][j + 1] + image_arr[i + 1][j - 1] + image_arr[i - 1][j + 1])/4

            elif label == 'b':
                r = float(image_arr[i-1][j-1] + image_arr[i + 1][j + 1] + image_arr[i + 1][j - 1] + image_arr[i - 1][j + 1])/4
                g = float(image_arr[i - 1][j] + image_arr[i + 1][j] + image_arr[i][j - 1] + image_arr[i][j + 1])/4
                b = image_arr[i][j]


            elif label == 'g' and getlabel(j - 1, i) == 'r':

                r = float(image_arr[i][j - 1] + image_arr[i][j + 1]) / 2

                g = image_arr[i][j]

                b = float(image_arr[i - 1][j] + image_arr[i + 1][j]) / 2


            elif label == 'g' and getlabel(j - 1, i) == 'b':

                b = float(image_arr[i][j - 1] + image_arr[i][j + 1]) / 2

                g = image_arr[i][j]

                r = float(image_arr[i - 1][j] + image_arr[i + 1][j]) / 2

            else:
                r, g, b = -1, -1, -1
                print("error!!!")
                exit()

            # if r/255 < 0.0031308:
            #     r = r * 12.92
            # else:
            #     r = (1.055 * pow(r/255, 1.0/2.4) - 0.055)*255
            #
            #
            # if g/255 < 0.0031308:
            #     g = g * 12.92
            # else:
            #     g = (1.055 * pow(g/255, 1.0/2.4) - 0.055)*255
            #
            #
            # if b/255 < 0.0031308:
            #     b = b * 12.92
            # else:
            #     b = (1.055 * pow(b/255, 1.0/2.4) - 0.055)*255

            new_img[i][j][0] = r #0.299 * r + 0.587 * g + 0.114 * b
            new_img[i][j][1] = g
            new_img[i][j][2] = b

    return new_img


"""Add background from data events"""
def background_addition(image_arr):


    back_num = len([f for f in os.listdir("../CNN_on_training_data/back_by_device/" + model + "/") if f.endswith('.txt')])

    index_back = np.random.randint(0, back_num - 1)

    back_arr = getdata("../CNN_on_training_data/back_by_device/" + model + "/" + str(index_back) + ".txt")

    image_arr += back_arr

    for i in range(len(image_arr)):
        for j in range(len(image_arr[i])):
            if image_arr[i][j] > 255:
                image_arr[i][j] = 255
            image_arr[i][j] = int(image_arr[i][j])

    return image_arr


"""color temperature table for white balancing"""
kelvin_table = {
    1000: (255,56,0),
    1500: (255,109,0),
    2000: (255,137,18),
    2500: (255,161,72),
    3000: (255,180,107),
    3500: (255,196,137),
    4000: (255,209,163),
    4500: (255,219,186),
    5000: (255,228,206),
    5500: (255,236,224),
    6000: (255,243,239),
    6500: (255,249,253),
    7000: (245,243,255),
    7500: (235,238,255),
    8000: (227,233,255),
    8500: (220,229,255),
    9000: (214,225,255),
    9500: (208,222,255),
    10000: (204,219,255)}


"""white balance"""
def convert_temp(image, temp):
    r, g, b = kelvin_table[temp]
    matrix = ( r / 255.0, 0.0, 0.0, 0.0,
               0.0, g / 255.0, 0.0, 0.0,
               0.0, 0.0, b / 255.0, 0.0 )
    return image.convert('RGB', matrix)


"""get the image output"""
def make_image(file_dir, filename):

    x, y, c = read_hit_file(file_dir)

    for i in range(len(c[0])):

        if c[0][i] > threshold_e:
            c[0][i] = np.random.normal(c[0][i], smearing)
            if c[0][i] < 0:
                c[0][i] = 1
        else:
            c[0][i] = 0


    image = np.zeros((1944, 2592))
    for i in range(len(x[0])):
        image[len(image) - int(y[0][i]) - 1][int(x[0][i])] = c[0][i]

    image = image * conversion_factor

    maxY, maxX = get_brightest_pixel(image)

    if pass_edge_check(maxX, maxY, (2592, 1944)) == True:

        x0, x1, y0, y1 = get_crop_range(maxX, maxY)

        image = image[y0:y1, x0:x1]

        for i in range(len(image)):
            for j in range(len(image[i])):
                if image[i][j] < 0:
                    image[i][j] = 0

                if image[i][j] > 255:
                    image[i][j] = 255.0

        image = color_processing(image)

        image = Image.fromarray(np.uint8(np.array(image)), mode='RGB')

        image = convert_temp(image, 5000)

        image = np.array(image)

        image_gray = np.zeros((64, 64))

        for i in range(len(image)):
            for j in range(len(image[i])):
                image_gray[i][j] = 0.299 * image[i][j][0] + 0.587 * image[i][j][1] + 0.114 * image[i][j][2]

        image = image_gray

        image = background_addition(image)

        if not os.path.exists("./output/" + file_qdc + "/" + str(particle_type) + "_2Dimages_fac" + str(conversion_factor) + "/"):
            os.mkdir("./output/" + file_qdc + "/" + str(particle_type) + "_2Dimages_fac" + str(conversion_factor) + "/")

        f = open("./output/" + file_qdc + "/" + str(particle_type) + "_2Dimages_fac" + str(conversion_factor) + "/" + filename, 'w')

        for i in range(len(image)):
            for k in range(len(image[i])):
                f.write(str(int(image[i][k])) + " ")
            f.write("\n")
        f.close()


particle_type = "mu+"

conversion_factor = 2

threshold_e = 0

smearing = 0

file_qdc = "qdc_res_0_smear_0_slope_0"
model = 'A510_ISO881'


for filename in os.listdir("./output/" + file_qdc + "/" + str(particle_type) + "/"):

    if os.path.exists("./output/" + file_qdc + "/" + str(particle_type) + "_2Dimages_fac" + str(conversion_factor) + "/" + filename):
        pass
    else:
        print("working on " + str(filename))
        make_image("./output/" + file_qdc + "/" + str(particle_type) + "/" + filename, filename)

