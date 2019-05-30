import numpy as np
from PIL import Image
import sift


class ImageWrapper:

    def __init__(self, image_path, image_name):
        self.name = image_name

        image = Image.open(image_path)
        grayscaled_image = image.convert('L')
        self.image = grayscaled_image


class ImagesContainer:

    def __init__(self, images_paths, images_names):
        # self.images = [ImageWrapper(images_paths[15], images_names[15]), ImageWrapper(images_paths[14], images_names[14])]
        self.images = [ImageWrapper(path, name) for (path, name) in zip(images_paths, images_names)]
        self.sift = [sift.SIFT(image) for image in self.images]
        self.compare_imgs()

    def compare_imgs(self):
        out_str = ''
        # (octave_i, scale_i, m, n, sigma, x, y, omega)
        imgs_info = [(self.sift[i].extremes, self.sift[i].image.name) for i in range(len(self.sift))]

        c_match = 0.6
        # c_match = 0.4

        for k in range(len(imgs_info)):
            for t in range(k + 1, len(imgs_info)):
                points_left = [(point[5], point[6]) for point in imgs_info[k][0]]
                points_right = [(point[5], point[6]) for point in imgs_info[t][0]]
                distances = []
                matches = 0
                for i in range(len(points_left)):
                    for j in range(len(points_right)):
                        distances.append(self.calculate_distance(points_left[i], points_right[j]))
                    distances.sort()
                    first_neighbour = distances[0]
                    second_neighbour = distances[1]
                    if first_neighbour < c_match * second_neighbour:
                        matches += 1
                    distances = []

                if matches >= 0.5 * len(self.sift[k].extremes):
                    out_str += (f'{imgs_info[k][1]}\t\t{imgs_info[t][1]}\n'
                                f'{len(self.sift[k].extremes)}\t{round(matches / len(self.sift[k].extremes), 2)}\t{len(self.sift[t].extremes)}\n\n')
        with open('results.txt', 'w') as f:
            f.write(out_str)

    def calculate_distance(self, a, b):
        return ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5
