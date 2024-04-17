# By Pytel
import numpy as np
import cv2
import matplotlib.pyplot as plt

formats = ['super_pixel', 'bilinear']

def deBayer(img, format='super_pixel'):
    """
    DeBayering of the Bayer pattern image

    Args:
        img : Bayer pattern image
        format : output format of the image
    
    Supported formats:
    - 'super_pixel' - output image has 1/4 of the original resolution
    - 'bilinear' - output image has the same resolution as the input image
    
    img = [
        [G, R, G, R, G, R, ...],
        [B, G, B, G, B, G, ...],
        ...
    ]

    Returns:
        img_out: height, width, channel = frame.shape
    """

    def super_pixel(img):
        G1 = img[0::2, 0::2]
        G2 = img[1::2, 1::2]
        B = img[0::2, 1::2]
        R = img[1::2, 0::2]

        G = G1/2 + G2/2

        img_out = np.zeros((img.shape[0]//2, img.shape[1]//2, 3), dtype=np.uint8)
        img_out[..., 0] = R
        img_out[..., 1] = G
        img_out[..., 2] = B
        return img_out

    print(img.shape)

    if format == 'super_pixel':
        img_out = super_pixel(img)
    elif format == 'bilinear':
        raise NotImplementedError

    return img_out

def RGB_to_YUV(img):
    """
    Convert RGB image to YUV image

    Args:
        img : RGB image

    Returns:
        img_out : YUV image
    """
    img_out = np.zeros_like(img, dtype=np.float32)

    img_out[..., 0] = 0.299 * img[..., 0] + 0.587 * img[..., 1] + 0.114 * img[..., 2]
    img_out[..., 1] = 0.492 * (img[..., 2] - img_out[..., 0])
    img_out[..., 2] = 0.877 * (img[..., 0] - img_out[..., 0])

    return img_out

def intenzity_corecton(img, etalon):
    return img/etalon

def normalize(img):
    img = img - np.min(img)
    img = img / np.max(img) * 255
    return img.astype('uint8')

def plot_imgs(imgs, titles, cmap='gray'):
    for i in range(len(titles)):
        img = imgs[i]
        plt.subplot(1, 2, i+1)
        plt.imshow(img) 
        plt.title(titles[i])
    plt.show()

def histogram(img):
    Y = img.shape[0]
    X = img.shape[1]
    hist = np.zeros([256,1])
    for y in range(Y):
        for x in range(X):
            hist[img[y][x]] +=1
    return hist

def sum_range(array, start=0, stop=0):
    return np.sum(array[start:stop])

def sumed(array):
    ret = np.zeros(array.shape[0])
    sumed = 0
    for i in range(array.shape[0]):
        sumed += array[i]
        ret[i] = sumed
    return ret 

def ekvalize(img):
    q0, p0, qk = 0, 0, 255
    Y = img.shape[0]
    X = img.shape[1]
    ekvalized = np.zeros([Y,X])
    #hist = histogram(img)
    hist = np.histogram(img, bins=256)[0]
    sumed_values = sumed(hist)
    coef = (qk-q0)/(X*Y)
    #for y in range(Y):
    #    for x in range(X):
    #        ekvalized[y][x] = coef * sumed_values[img[y][x]]
    ekvalized = coef * sumed_values[img]
    return ekvalized.astype('uint8')

def equalize_color(RGB_img):
    """Equalize color image
    """
    q0, p0, qk = 0, 0, 255
    width, height, _ = RGB_img.shape
    YUV = cv2.cvtColor(RGB_img, cv2.COLOR_BGR2YUV)
    Y = YUV[..., 0]
    hist = np.histogram(Y, bins=256)[0]
    sumed_values = sumed(hist)
    coef = (qk-q0)/(width*height)
    R, G, B = RGB_img[..., 0], RGB_img[..., 1], RGB_img[..., 2]
    R = coef * sumed_values[R]
    G = coef * sumed_values[G]
    B = coef * sumed_values[B]
    img_out = np.zeros_like(RGB_img)
    img_out[..., 0] = R
    img_out[..., 1] = G
    img_out[..., 2] = B
    img_out = np.clip(img_out, 0, 255)
    return img_out.astype('uint8')