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
        self.images = [ImageWrapper(images_paths[2], images_names[2]), ImageWrapper(images_paths[4], images_names[4])]
        # self.images = [ImageWrapper(path, name) for (path, name) in zip(images_paths, images_names)]

        self.sift = [sift.SIFT(image) for image in self.images]
