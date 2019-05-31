import numpy as np
from PIL import Image, ImageFilter

import sift


class ImageWrapper:
    """
    Wrapper for the image to keep image obj and image name
    """

    def __init__(self, image_path, image_name):
        self.name = image_name
        self.path = image_path
        self.image = self.process_image()
        self.key_points = []

    def process_image(self):
        """
        Reads image and grayscale it
        :return: grayscale image
        """
        image = Image.open(self.path)
        grayscale_image = image.convert('L')
        return grayscale_image

    def set_key_points(self, key_points):
        """
        Setter for fey points array
        :param key_points:
        :return:
        """
        self.key_points = key_points


class ImagesContainer:
    """
    Container to store images and provide comparing logic
    """

    def __init__(self, images_paths, images_names):
        self.images = [ImageWrapper(path, name) for (path, name) in zip(images_paths, images_names)]

    def compute_images_key_points(self):
        """
        Computes key points for every image using SIFT key point extraction
        :return:
        """
        sift_detector = sift.SIFT()
        for image in self.images:
            image.set_key_points(sift_detector.get_key_points(image.image))

    def compare_images(self):
        """
        Provides images comparison logic
        :return:
        """
        c_match = 0.6
        mse_threshold = 2500

        for k in range(len(self.images)):
            points_left = self.images[k].key_points
            for t in range(k + 1, len(self.images)):
                images_mse = self.calculate_mse(self.images[k].image, self.images[t].image)

                # the lower mean squared error - more similar images
                # check if MSE lower than MSE threshold value and continue comparison
                if images_mse < mse_threshold:
                    points_right = self.images[t].key_points

                    matches = 0
                    # similarity threshold
                    # 25% of points from first image
                    matches_threshold = len(points_left) / 4
                    for i in range(len(points_left)):
                        distances = []
                        for j in range(len(points_right)):
                            # calculate distances between key point from first image and key points from second images
                            distances.append(self.calculate_distance_between_points(points_left[i], points_right[j]))

                        # find first and second neighbours to this key point from first image
                        distances.sort()
                        first_neighbour = distances[0]
                        second_neighbour = distances[1]

                        # check if this point is similar on two images
                        if first_neighbour < c_match * second_neighbour:
                            matches += 1
                            # if matches more, or same as matching threshold -> this images are similar
                            if matches >= matches_threshold:
                                print(f'{self.images[k].name}\t{self.images[t].name}')
                                break
                    if matches >= len(points_left) / 4:
                        break

    @staticmethod
    def calculate_distance_between_points(a, b):
        """
        Calculates distance between two points
        :param a:
        :param b:
        :return: distance
        """
        return ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5

    @staticmethod
    def calculate_mse(left_image, right_image):
        """
        Calculates mean squared error between two images
        :param left_image:
        :param right_image:
        :return: mse value
        """

        # crop and smooth the first image
        cropped_img = left_image.resize((256, 256), Image.BILINEAR)
        filtered_image = cropped_img.filter(ImageFilter.SMOOTH_MORE)
        left_image = np.array(filtered_image)

        # crop and smooth the second image
        cropped_img = right_image.resize((256, 256), Image.BILINEAR)
        filtered_image = cropped_img.filter(ImageFilter.SMOOTH_MORE)
        right_image = np.array(filtered_image)

        # sum of the squared difference between the two images
        err = np.sum((left_image.astype("float") - right_image.astype("float")) ** 2)
        err /= float(left_image.shape[0] * left_image.shape[1])

        return err
