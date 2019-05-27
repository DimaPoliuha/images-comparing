import math
import numpy as np
from PIL import Image, ImageFilter


class SIFT:
    def __init__(self, image):
        self.image = image
        self.sigma = 1.6
        self.k = math.sqrt(2)
        self.count_gaussian_per_octave = 3

        self.gaussian_pyramid = self.get_gaussian_pyramid()
        self.differences_of_gaussian = self.get_differences_of_gaussian()

    def get_gaussian_pyramid(self):
        pyramid = []
        layer = []
        radius = self.sigma
        for i in range(10):
            size = int(512 / (2 ** i))
            temp_img = self.image.image.resize((size, size), Image.BILINEAR)
            for j in range(self.count_gaussian_per_octave + 2):
                filtered_image = temp_img.filter(ImageFilter.GaussianBlur(radius=radius))
                radius = radius * self.k
                img_arr = np.array(filtered_image)
                layer.append(img_arr)
            radius = radius / self.k ** 3

            pyramid.append(layer)
            layer = []

        return pyramid

    def get_differences_of_gaussian(self):
        differences_of_gaussian = []
        differences_layer = []
        for layer in self.gaussian_pyramid:
            for i in range(self.count_gaussian_per_octave + 1):
                difference = layer[i+1] - layer[i]
                differences_layer.append(difference)
            differences_of_gaussian.append(differences_layer)
            differences_layer = []
        return differences_of_gaussian
