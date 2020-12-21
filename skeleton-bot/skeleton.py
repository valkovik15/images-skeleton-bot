import string
import random

from PIL import Image, ImageDraw, ImageFont
import numpy as np
from skimage.morphology import binary_erosion, erosion
from skimage.filters import threshold_otsu
from skimage.color import rgb2gray


class Skeletonizer():
    '''Класс, производящий перенос стиля'''

    def __init__(self):
        '''Инициализация структурных элементов'''
        T_1 = (np.array([[True, True, True], [False, True, False], [False, False, False]]),
               np.array([[False, False, False], [False, False, False], [True, True, True]]))
        T_2 = (np.array([[True, False, False], [True, True, False], [True, False, False]]),
               np.array([[False, False, True], [False, False, True], [False, False, True]]))
        T_3 = (np.array([[False, False, False], [False, True, False], [True, True, True]]),
               np.array([[True, True, True], [False, False, False], [False, False, False]]))
        T_4 = (np.array([[False, False, True], [False, True, True], [False, False, True]]),
               np.array([[True, False, False], [True, False, False], [True, False, False]]))
        T_5 = (np.array([[False, True, False], [False, True, True], [False, False, False]]),
               np.array([[False, False, False], [True, False, False], [True, True, False]]))
        T_6 = (np.array([[False, True, False], [True, True, False], [False, False, False]]),
               np.array([[False, False, False], [False, False, True], [False, True, True]]))
        T_7 = (np.array([[False, False, False], [True, True, False], [False, True, False]]),
               np.array([[False, True, True], [False, False, True], [False, False, False]]))
        T_8 = (np.array([[False, False, False], [False, True, True], [False, True, False]]),
               np.array([[True, True, False], [True, False, False], [False, False, False]]))
        self.str_els = [T_1, T_2, T_3, T_4, T_5, T_6, T_7, T_8]

    def skeletonize(self, image, iterations):
        content_image = Image.open(image)
        gray = rgb2gray(np.asarray(content_image))
        thresh = threshold_otsu(gray)
        bin_g = gray > thresh
        step_images = self.skeleton(bin_g, iterations)

        return step_images

    def thinning(self, img, a, b):
        b_e = binary_erosion(img, a)
        b_d = binary_erosion(~img, b)
        sub = np.logical_and(b_e, b_d)
        return self.substract(img, sub)

    def substract(self, a, b):
        return np.logical_and(np.logical_xor(a, b), np.logical_and(a, ~b))

    def skeleton(self, img, n):
        step_images = []
        for i in range(n):
            for j in range(len(self.str_els)):
                a, b = self.str_els[j]
                img = self.thinning(img, np.array(a).astype(np.bool), np.array(b).astype(np.bool))
            image_from_step = Image.fromarray(img).convert(mode='RGB')
            draw = ImageDraw.Draw(image_from_step)
            font = ImageFont.truetype("arial.ttf", 45)
            draw.text((0, 0), 'step = ' + str(i), (255, 0, 0), font=font)
            step_images.append(image_from_step)
        return step_images
