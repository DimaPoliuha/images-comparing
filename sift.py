import math
import numpy as np
from PIL import Image, ImageFilter
np.seterr(all='ignore')
# TODO check


class SIFT:
    def __init__(self, image):
        self.image = image
        # self.sigma = 1.6
        self.sigma = 0.8
        self.k = math.sqrt(2)
        self.octaves_count = 4
        self.count_scales_per_octave = 3
        self.threshold = 0.015

        self.gaussian_pyramid = self.get_gaussian_pyramid()
        self.differences_of_gaussian = self.get_differences_of_gaussian()
        # self.save_dog()
        self.extremes = self.get_local_extremum()
        print(len(self.extremes))
        self.discard_low_contrast_points_initial()
        self.extremes = self.key_point_interpolation()
        self.discard_low_contrast_points()
        self.discard_points_on_edges()
        print(len(self.extremes))

    def get_gaussian_pyramid(self):
        pyramid = []
        layer = []
        radius = self.sigma
        for i in range(self.octaves_count):
            size = int(256 / (2 ** i))
            temp_img = self.image.image.resize((size, size), Image.BILINEAR)
            for j in range(self.count_scales_per_octave + 2):
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
            for i in range(self.count_scales_per_octave + 1):
                difference = layer[i+1] - layer[i]
                differences_layer.append(difference)
            differences_of_gaussian.append(differences_layer)
            differences_layer = []
        return differences_of_gaussian

    def check_extremum(self, octave, x, y, scale, type_check):
        val = octave[scale][x, y]
        for k in range(-1, 2):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if k == i == j == 0:
                        continue
                    if type_check == 'max':
                        # val = val * 0.95
                        if val <= octave[scale + k][x + i, y + j]:
                            return False
                    elif type_check == 'min':
                        # val = val * 1.05
                        if val >= octave[scale + k][x + i, y + j]:
                            return False
                    else:
                        raise Exception('Unknown type check')
        return True

    def get_local_extremum(self):
        extremes = []
        for octave_index, octave in enumerate(self.differences_of_gaussian):
            shape = octave[0].shape[0]
            for scale in range(1, len(octave) - 1):
                for x in range(1, shape - 1):
                    for y in range(1, shape - 1):
                        if self.check_extremum(octave, x, y, scale, 'max'):
                            extremes.append((octave_index, scale, x, y))
                        if self.check_extremum(octave, x, y, scale, 'min'):
                            extremes.append((octave_index, scale, x, y))
        return extremes

    def discard_low_contrast_points_initial(self):
        for extrema_index, extrema in enumerate(self.extremes):
            octave, scale, x, y = extrema[0], extrema[1], extrema[2], extrema[3]
            if self.differences_of_gaussian[octave][scale][x, y] < 0.8 * self.threshold:
                self.extremes.pop(extrema_index)

    def key_point_interpolation(self):
        interpolated_key_points = []

        for extrema in self.extremes:
            t = 0
            shape = self.differences_of_gaussian[extrema[0]][extrema[1]].shape[0]
            while t < 5:
                octave_i, scale_i, m, n = extrema[0], extrema[1], extrema[2], extrema[3]
                # print(m, n, scale_i, ' shape: ', shape)
                if 0 < m < shape - 1 and 0 < n < shape - 1 and 0 < scale_i < self.count_scales_per_octave:
                    alpha, omega = self.quadratic_interpolation(extrema)

                    delta_min = 0.5
                    delta_o = delta_min * 2 ** (octave_i - 1)

                    sigma, x, y = (
                        (delta_o / delta_min) * self.sigma * 2 ** ((alpha[0] + scale_i) / self.count_scales_per_octave),
                        delta_o * (alpha[1] + m),
                        delta_o * (alpha[2] + n)
                    )
                    if max(*alpha) < 0.6:
                        interpolated_key_points.append(
                            (octave_i, scale_i, m, n, sigma, x, y, omega)
                        )
                        break
                    extrema = (octave_i, int(round(scale_i + alpha[0])), int(round(m + alpha[1])), int(round(n + alpha[2])))
                t += 1

        return interpolated_key_points

    def quadratic_interpolation(self, extrema):
        octave_i, sc_i, m, n = extrema[0], extrema[1], extrema[2], extrema[3]
        oct = self.differences_of_gaussian[octave_i]
        g = np.array([
            (int(oct[sc_i + 1][m, n]) - int(oct[sc_i - 1][m, n])) / 2,
            (int(oct[sc_i][m + 1, n]) - int(oct[sc_i][m - 1, n])) / 2,
            (int(oct[sc_i][m, n + 1]) - int(oct[sc_i][m, n - 1])) / 2
        ])
        h_11 = int(oct[sc_i + 1][m, n]) + int(oct[sc_i - 1][m, n]) - 2 * int(oct[sc_i][m, n])
        h_22 = int(oct[sc_i][m + 1, n]) + int(oct[sc_i][m - 1, n]) - 2 * int(oct[sc_i][m, n])
        h_33 = int(oct[sc_i][m, n + 1]) + int(oct[sc_i][m, n - 1]) - 2 * int(oct[sc_i][m, n])
        h_12 = (int(oct[sc_i + 1][m + 1, n]) - int(oct[sc_i + 1][m - 1, n]) - int(oct[sc_i - 1][m + 1, n]) + int(oct[sc_i - 1][m - 1, n])) / 4
        h_13 = (int(oct[sc_i + 1][m, n + 1]) - int(oct[sc_i + 1][m, n - 1]) - int(oct[sc_i - 1][m, n + 1]) + int(oct[sc_i - 1][m, n - 1])) / 4
        h_23 = (int(oct[sc_i][m + 1, n + 1]) - int(oct[sc_i][m + 1, n - 1]) - int(oct[sc_i][m - 1, n + 1]) + int(oct[sc_i][m - 1, n - 1])) / 4
        H = np.array([
            [h_11, h_12, h_13],
            [h_12, h_22, h_23],
            [h_13, h_23, h_33]

        ])
        H = H + 0.00001 * np.random.rand(3, 3) # add just a little noise to data
        inverse_H = np.linalg.inv(H)
        alpha = - inverse_H @ g
        omega = oct[sc_i][m, n] - 0.5 * g.transpose() @ inverse_H @ g
        return alpha, omega

    def discard_low_contrast_points(self):
        for extrema_index, extrema in enumerate(self.extremes):
            if abs(extrema[-1]) < self.threshold:
                self.extremes.pop(extrema_index)

    def discard_points_on_edges(self):
        c_edge = 10
        check = (c_edge + 1) ** 2 / c_edge
        for extrema_index, extrema in enumerate(self.extremes):
            octave_i, sc_i, m, n = extrema[0], extrema[1], extrema[2], extrema[3]
            oct = self.differences_of_gaussian[octave_i]
            h_11 = int(oct[sc_i][m + 1, n]) + int(oct[sc_i][m - 1, n]) - 2 * int(oct[sc_i][m, n])
            h_22 = int(oct[sc_i][m, n + 1]) + int(oct[sc_i][m, n - 1]) - 2 * int(oct[sc_i][m, n])
            h_12 = (int(oct[sc_i][m + 1, n + 1]) - int(oct[sc_i][m + 1, n - 1]) - int(oct[sc_i][m - 1, n + 1]) + int(
                oct[sc_i][m - 1, n - 1])) / 4
            H = np.array([
                [h_11, h_12],
                [h_12, h_22]
            ])
            # TODO check
            tr_H = H.trace() ** 2 / np.linalg.det(H)
            if tr_H >= check:
                self.extremes.pop(extrema_index)

    def save_dog(self):
        t = 0
        i = 0
        for layer in self.differences_of_gaussian:
            for image_arr in layer:
                image = Image.fromarray(image_arr)
                image.save(f"dev_dataset/dog/{i}{t}.jpg")
                i += 1
            t += 1
