import os
import argparse


def argument_parsing():
    parser = argparse.ArgumentParser(description='First test task on images similarity.')
    parser.add_argument('--path', required=True, help='folder with images')
    args = parser.parse_args()
    return args.path


if __name__ == '__main__':
    images_path = argument_parsing()
    if os.path.exists(images_path):
        filenames = os.listdir(images_path)
        if filenames:
            file_paths = [f'{images_path}/{filename}' for filename in filenames]
            print(file_paths)
        else:
            print('Empty directory')
    else:
        print(f'Path {images_path} doesn\'t exist')
