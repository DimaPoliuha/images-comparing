from PIL import Image


class ImageWrapper:

    def __init__(self, image_path, image_name):
        self.name = image_name
        self.image_obj = Image.open(image_path)


class ImagesContainer:

    def __init__(self, images_paths, images_names):
        self.images = [ImageWrapper(path, name) for (path, name) in zip(images_paths, images_names)]
