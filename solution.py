import os
import argparse
from structures.images_structures import ImagesContainer


def argument_parsing():
    """
    Command line arguments parsing
    :return: images path
    """
    parser = argparse.ArgumentParser(description='First test task on images similarity.')
    parser.add_argument('--path', required=True, help='folder with images')
    args = parser.parse_args()
    return args.path


def compare(files_paths, filenames):
    """
    Collects all images, detects key points and compare images
    :param files_paths:
    :param filenames:
    :return:
    """
    container = ImagesContainer(files_paths, filenames)
    container.compute_images_key_points()
    container.compare_images()


if __name__ == '__main__':
    images_path = argument_parsing()
    if os.path.exists(images_path):
        filenames = os.listdir(images_path)
        if filenames:
            files_paths = [f'{images_path}/{filename}' for filename in filenames]
            compare(files_paths, filenames)
        else:
            print('Empty directory')
    else:
        print(f'Path {images_path} doesn\'t exist')
