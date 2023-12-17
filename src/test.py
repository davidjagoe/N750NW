import exifread
import glob
import os
import shutil
import subprocess

from datetime import datetime


def main():
    with open("IMG.jpg", "rb") as image_file:
        tags = exifread.process_file(image_file)
        print(tags)
        

if __name__ == "__main__":
    main()
