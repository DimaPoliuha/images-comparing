import math
import numpy as np
from PIL import Image, ImageFilter


class ImageWrapper:

    def __init__(self, image_path, image_name):
        self.name = image_name

        image = Image.open(image_path)
        grayscaled_image = image.convert('L')
        self.image = grayscaled_image

        self.sigma = 1.6
        self.k = math.sqrt(2)
        self.count_gaussian_per_octave = 3

        self.gaussian_pyramid = self.getGaussianPyramid()
        self.differences_of_gaussian = self.getDifferencesOfGaussian()
        t = 0
        i = 0
        # for layer in self.differences_of_gaussian:
        #     for image_arr in layer:
        #         image = Image.fromarray(image_arr)
        #         image.save(f"dev_dataset/compressed/dog/{i}{t}.jpg")
        #         i += 1
        #     t += 1

        # image = Image.open(image_path)
        # grayscaled_image = image.convert('L')
        # resized_image = grayscaled_image.resize((256, 256), Image.ANTIALIAS)
        # sigma = 1.6
        #
        # filtered_image = resized_image.filter(ImageFilter.GaussianBlur(sigma=sigma))
        #
        # smaller_image = grayscaled_image.resize((128, 128), Image.ANTIALIAS)
        # filtered_smaller_image = smaller_image.filter(ImageFilter.GaussianBlur(sigma=sigma))
        # filtered_smaller_image = filtered_smaller_image.resize((256, 256), Image.ANTIALIAS)
        #
        # image_arr1 = np.array(filtered_image)
        # image_arr2 = np.array(filtered_smaller_image)
        # dog = image_arr2 - image_arr1


        # image = Image.fromarray(dog)
        # image.save(f"dev_dataset/compressed/DoG.jpg")

        # filtered_image.save(f"dev_dataset/compressed/{image_name}.jpg")
        # self.compress_image()

    def getGaussianPyramid(self):
        pyramid = []
        layer = []
        radius = self.sigma
        for i in range(10):
            size = int(512 / (2 ** i))
            temp_img = self.image.resize((size, size), Image.BILINEAR)
            # temp_img = self.image.resize((size, size), Image.ANTIALIAS)
            for j in range(self.count_gaussian_per_octave + 2):
                radius = radius * self.k
                # print(radius)
                filtered_image = temp_img.filter(ImageFilter.GaussianBlur(radius=radius))
                # filtered_image.save(f"dev_dataset/compressed/{i}{j}.jpg")
                img_arr = np.array(filtered_image)
                layer.append(img_arr)
            radius = radius / self.k ** 2

            pyramid.append(layer)
            # layer[2].save(f"dev_dataset/compressed/{i}.jpg")
            layer = []

        return pyramid

    def getDifferencesOfGaussian(self):
        differences_of_gaussian = []
        differences_layer = []
        for layer in self.gaussian_pyramid:
            for i in range(self.count_gaussian_per_octave + 1):
                difference = layer[i+1] - layer[i]
                differences_layer.append(difference)
            differences_of_gaussian.append(differences_layer)
            differences_layer = []
        return differences_of_gaussian


    # def compress_image(self):
    #     self.image = self.image.resize((100, 100), Image.ANTIALIAS)


class ImagesContainer:

    def __init__(self, images_paths, images_names):
        self.images = [ImageWrapper(images_paths[0], images_names[0]), ImageWrapper(images_paths[1], images_names[1])]
        # self.images = [ImageWrapper(path, name) for (path, name) in zip(images_paths, images_names)]
