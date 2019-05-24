import os
import argparse
from structures.images_structures import ImagesContainer


def argument_parsing():
    parser = argparse.ArgumentParser(description='First test task on images similarity.')
    parser.add_argument('--path', required=True, help='folder with images')
    args = parser.parse_args()
    return args.path


def compare(files_paths, filenames):
    container = ImagesContainer(files_paths, filenames)
    # for i in range(len(container.images)):
    #     for j in range(i + 1, len(container.images)):
    #         compare_imgs(i, j)


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
