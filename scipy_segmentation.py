# %%
import numpy as np
import matplotlib.pyplot as plt
import skimage.data as data
import skimage.segmentation as seg
import skimage.filters as filters
import skimage.draw as draw
import skimage.color as color
from skimage import io
import os

DATASET_PATH = "/home/carter/Desktop/CVPPP2017_LSC/"

"""
Segment images in a given dataset path with a given method
Performs segmentation and outputs results to a folder with the name of the segmentation method
:param input_path: the path to the dataset to segment, e.g. /home/carter/Desktop/CVPPP2017_LSC/training/
:param method: the segmentation method to use - should work on a single image. See green_channel_thresh
"""
def segment(input_path, method):
    output_path = input_path + method.__name__ + "/"
    input_path += "training/"
    # Get the partial paths (e.g. A4/plant0574_fg.png) of every image in dataset
    image_paths = [] # Segmentation ground truth (_fg.png)
    for subfolder in os.listdir(input_path):
        for f in os.listdir(input_path + subfolder):
            if "_rgb.png" in f:
                image_paths.append(subfolder + "/" + f)

    # Create folder structure to hold output images
    if not os.path.isdir(output_path):
        os.mkdir(output_path)
    for subfolder in os.listdir(input_path):
        if not os.path.isdir(output_path + subfolder):
            os.mkdir(output_path + subfolder)

    # Go through each image
    for path in image_paths:
        img = io.imread(input_path + path)
        segmented_img = method(img)
        path = path.replace("rgb", "fg") # Change file name to fg from rgb to match ground truth
        io.imsave(output_path + path, segmented_img)
        print(path)

"""
Simple thresholding based on the value of the green channel
:param img: the image to segment
:retrurn: a binary segmented image
"""
def green_channel_thresh(img):
    green_channel = img[:,:,1] # get the green channel
    return green_channel > 100 # get pixels where green channel > 100

"""
Local thresholdig using the scipy's build in threshold_local
:param img: the image to segment
:return: a binary segmented image
"""
def local_thresh(img):
    green_channel = img[:,:,1]
    thresh = filters.threshold_local(green_channel,block_size=51, offset=10) 
    return green_channel > thresh


def main():
    segment(DATASET_PATH, green_channel_thresh)

if __name__ == "__main__":
    main()
# %%
