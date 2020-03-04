import os
import sys
import argparse

def main(path):
    """Remove the middle level directories
    
    Arguments:
        path {string} -- path of the upper directory
    """
    for dir_name in os.listdir(path):
        for file_name in os.listdir(os.path.join(path, dir_name)):
            os.rename(os.path.join(path, dir_name, file_name), os.path.join(path, file_name))
        os.rmdir(os.path.join(path, dir_name))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", help="path of the directory to flatten")
    args = parser.parse_args()
    main(args.file_path)