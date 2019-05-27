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
        self.save_dog()
        # self.get_local_extremum()

    def get_gaussian_pyramid(self):
        pyramid = []
        layer = []
        radius = self.sigma
        # for i in range(10):
        for i in range(8):
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

    def get_local_extremum(self):
        extrems = []
        for layer in self.differences_of_gaussian:
            shape = layer[0].shape[0]
            for img_index in range(1, len(layer) - 1):
                for i in range(1, shape - 1):
                    for j in range(1, shape - 1):
                        if all(layer[img_index][i, j] > x for x in [
                                layer[img_index][i-1, j],
                                layer[img_index][i+1, j],
                                layer[img_index][i, j-1],
                                layer[img_index][i, j+1],
                                layer[img_index][i+1, j+1],
                                layer[img_index][i+1, j-1],
                                layer[img_index][i-1, j+1],
                                layer[img_index][i-1, j-1],

                                layer[img_index-1][i, j],
                                layer[img_index-1][i - 1, j],
                                layer[img_index-1][i + 1, j],
                                layer[img_index-1][i, j - 1],
                                layer[img_index-1][i, j + 1],
                                layer[img_index-1][i + 1, j + 1],
                                layer[img_index-1][i + 1, j - 1],
                                layer[img_index-1][i - 1, j + 1],
                                layer[img_index-1][i - 1, j - 1],

                                layer[img_index + 1][i, j],
                                layer[img_index + 1][i - 1, j],
                                layer[img_index + 1][i + 1, j],
                                layer[img_index + 1][i, j - 1],
                                layer[img_index + 1][i, j + 1],
                                layer[img_index + 1][i + 1, j + 1],
                                layer[img_index + 1][i + 1, j - 1],
                                layer[img_index + 1][i - 1, j + 1],
                                layer[img_index + 1][i - 1, j - 1]
                        ]
                        ):
                            extrems.append(layer[img_index][i, j])
        print(len(extrems))

    def save_dog(self):
        t = 0
        i = 0
        for layer in self.differences_of_gaussian:
            for image_arr in layer:
                image = Image.fromarray(image_arr)
                image.save(f"dev_dataset/dog/{i}{t}.jpg")
                i += 1
            t += 1
