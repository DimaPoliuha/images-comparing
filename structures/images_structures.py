from PIL import Image


class ImageWrapper:

    def __init__(self, image_path, image_name):
        self.name = image_name
        self.image_obj = Image.open(image_path)
        self.compress_image()

    def compress_image(self):
        if self.name == '15.jpg':
            self.image_obj = self.image_obj.resize((100, 100), Image.ANTIALIAS)


class ImagesContainer:

    def __init__(self, images_paths, images_names):
        self.images = [ImageWrapper(path, name) for (path, name) in zip(images_paths, images_names)]
