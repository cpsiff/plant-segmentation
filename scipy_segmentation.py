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

DATASET_PATH = "/home/carter/Desktop/CVPPP2017_LSC/training/"
OUTPUT_PATH = "/home/carter/Desktop/simple_threshold/"

# Get the partial paths (e.g. A4/plant0574_fg.png) of every image in dataset
image_paths = [] # Segmentation ground truth (_fg.png)
for subfolder in os.listdir(DATASET_PATH):
    for f in os.listdir(DATASET_PATH + subfolder):
        if "_rgb.png" in f:
            image_paths.append(subfolder + "/" + f)

# Go through each image
for path in image_paths:
    img = io.imread(DATASET_PATH + path)
    green_channel = img[:,:,1] # Just the green channel
    segmented_img = green_channel > 100 # Pixels where green channel > 100
    path = path.replace("rgb", "fg") # Change file name to fg from rgb to match ground truth
    io.imsave(OUTPUT_PATH + path, segmented_img)
    print(path)
# %%
