import dicom
from PIL import Image, ImageGrab
import numpy as np
import time
import datetime
import cv2
import math
import scipy.ndimage as ndi
import matplotlib.patches as mpatches
from skimage import data, segmentation, measure, morphology, color, filters, io
from matplotlib import pyplot as plt
import pywt
import os


# from tensorflow.models.tutorials.image.cifar10 import  cifar10


# 归一化处理
def function_z(image_array):
    data = (image_array - image_array.min()) / (image_array.max() - image_array.min()) * 255
    dataarray = data.astype(np.uint8)
    return dataarray

#显示图像
def showPET(petImage,flg=False) :
    image_array = petImage.pixel_array
    img = Image.fromarray(function_z(image_array),"L")
    if flg == True:
       img.show()
    return img

# 小波变换
def wavelet1(image_arr):
    print("开始小波变换")
    # Load image
    original = image_arr

    # Wavelet transform of image, and plot approximation and details
    titles = ['Approximation', ' Horizontal detail',
              'Vertical detail', 'Diagonal detail']
    coeffs2 = pywt.dwt2(original, 'bior1.3')

    LL, (LH, HL, HH) = coeffs2
    fig = plt.figure()

    for i, a in enumerate([LL, LH, HL, HH]):
        ax = fig.add_subplot(2, 2, i + 1)
        ax.imshow(a, origin='image', interpolation="nearest", cmap=plt.cm.gray)
        ax.set_title(titles[i], fontsize=12)

    fig.suptitle("dwt2 coefficients", fontsize=14)

    # Now reconstruct and plot the original image
    reconstructed = pywt.idwt2(coeffs2, 'bior1.3')
    fig = plt.figure()
    plt.imshow(reconstructed, interpolation="nearest", cmap=plt.cm.gray)

    # Check that reconstructed image is close to the original
    np.testing.assert_allclose(original, reconstructed, atol=1e-13, rtol=1e-13)

    # Now do the same with dwtn/idwtn, to show the difference in their signatures

    coeffsn = pywt.dwtn(original, 'bior1.3')
    fig = plt.figure()
    for i, key in enumerate(['aa', 'ad', 'da', 'dd']):
        ax = fig.add_subplot(2, 2, i + 1)
        ax.imshow(coeffsn[key], origin='image', interpolation="nearest",
                  cmap=plt.cm.gray)
        ax.set_title(titles[i], fontsize=12)

    fig.suptitle("dwtn coefficients", fontsize=14)

    # Now reconstruct and plot the original image
    reconstructed = pywt.idwtn(coeffsn, 'bior1.3')
    fig = plt.figure()
    plt.imshow(reconstructed, interpolation="nearest", cmap=plt.cm.gray)

    # Check that reconstructed image is close to the original
    np.testing.assert_allclose(original, reconstructed, atol=1e-13, rtol=1e-13)

    plt.show()



    # 得到Hu值


def getHu(filePath=r'C:\Users\FEITENG\Desktop\毕设\testpatient\1\ct_050'):
    meta = dicom.read_file(filePath)
    pixel = meta.pixel_array
    slope = meta.get('RescaleSlope')
    intercept = meta.get('RescaleIntercept')
    Hu = pixel * slope + intercept
    return Hu



    # 得到SUV值


def getEntropy(img):
    tmp = []
    for i in range(256):
        tmp.append(0)
    val = 0
    k = 0
    res = 0
    # img = np.array(image)
    for i in range(len(img)):
        for j in range(len(img[i])):
            val = img[i][j]
            tmp[val] = float(tmp[val] + 1)
            k = float(k + 1)
    for i in range(len(tmp)):
        tmp[i] = float(tmp[i] / k)
    for i in range(len(tmp)):
        if (tmp[i] == 0):
            res = res
        else:
            res = float(res - tmp[i] * (math.log(tmp[i]) / math.log(2.0)))
    print("图片信息熵为：%f" % (res))


def getASuv(file,pixel):
    meta = dicom.read_file(file)
    # pixel = meta.pixel_array
    slope = meta.get('RescaleSlope')
    weightKg = meta.get('PatientWeight')
    # 患者身高
    heightCm = meta.get('PatientSize') * 100  # 身高以厘米为单位
    # 患者性别
    sex = meta.get("PatientSex")
    # 示踪剂注射总剂量
    tracerActivity = meta.get('RadiopharmaceuticalInformationSequence')[0].get('RadionuclideTotalDose')
    theDate = meta.get('SeriesDate')
    measureTime = meta.get('RadiopharmaceuticalInformationSequence')[0].get('RadiopharmaceuticalStartTime')
    measureTime = time.strptime(theDate + measureTime[0:6], '%Y%m%d%H%M%S')
    measureTime = datetime.datetime(*measureTime[:6])
    # scanTime=meta.get('SeriesDate')+meta.get('SeriesTime')
    scanTime = meta.get('SeriesTime')
    scanTime = time.strptime(theDate + scanTime, '%Y%m%d%H%M%S')
    scanTime = datetime.datetime(*scanTime[:6])
    halfTime = meta.get('RadiopharmaceuticalInformationSequence')[0].get('RadionuclideHalfLife')
    if (scanTime > measureTime):
        actualActivity = tracerActivity * (2) ** (-(scanTime - measureTime).seconds / halfTime)
    else:
        raise ('time wrong:scanTime should be later than measure')

    if sex == 'F':
        lbmKg = 1.07 * weightKg - 148 * (weightKg / heightCm) ** 2
    else:
        lbmKg = 1.10 * weightKg - 120 * (weightKg / heightCm) ** 2

    suvLbm = pixel * slope * lbmKg * 1000 / actualActivity
    # suv=np.uint8(suvLbm)
    return suvLbm


# suv_arr = getASuv()
# _mask = suv_arr > 2.0
# #suv_arr *= _mask
# suv_arr = _mask
########################################################################
def seg(result):
    image = result
    thresh = filters.threshold_otsu(image)  # 阈值分割
    bw = morphology.closing(image > thresh, morphology.square(3))  # 闭运算

    cleared = bw.copy()  # 复制
    segmentation.clear_border(cleared)  # 清除与边界相连的目标物

    label_image = measure.label(cleared)  # 连通区域标记

    borders = np.logical_xor(bw, cleared)  # 异或
    label_image[borders] = -1

    # image_label_overlay = color.label2rgb(label_image, image=image)  # 不同标记用不同颜色显示

    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(8, 6))
    ax0.imshow(cleared, plt.cm.gray)
    # label_image = Image.fromarray(function_z(label_image),"L")
    # label_image = np.asarray(label_image)
    ax1.imshow(cleared, plt.cm.gray)

    for region in measure.regionprops(label_image):  # 循环得到每一个连通区域属性集

        # 忽略小区域
        # if region.area < 5:
        #     continue
        # 绘制外包矩形
        img = Image.fromarray(result, "L")

        minr, minc, maxr, maxc = region.bbox
        rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                  fill=False, edgecolor='red', linewidth=2)
        box = (minc, minr, maxc, maxr)
        print(box)
        roi = img.crop(box)
        imgdata = np.matrix(roi.getdata(), dtype='float')
        # print("平均SUV:%s" % (imgdata.mean()))
        # print("最大值:%f" % (imgdata.max()))
        # print("极差:%f" % ((imgdata.max() - imgdata.min())))
        # getEntropy(np.array(roi))
        # roi.show()
        ax1.add_patch(rect)

    fig.tight_layout()
    plt.show()


# 将一个目录下的bmp转换成jpg，同时也修改文件名

def bmp2jpg(directory):
    for file in os.listdir(directory):
        str = file[0:7] + '5' + file[8:14] + '.jpg'
        os.rename(os.path.join(directory, file), os.path.join(directory, str))

# file = r'C:\Users\FEITENG\Desktop\GraduationDesign\LymphaticData\柏景亿\src\柏景亿\PT\pt_009'
# img = dicom.read_file(file)
# suv_arr = getASuv(file,img.pixel_array)
# Image.fromarray(function_z(suv_arr)).show()
