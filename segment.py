# %%
import numpy as np
import matplotlib.pyplot as plt
import skimage.data as data
import skimage.segmentation as seg
import skimage.filters as filters
import skimage.draw as draw
import skimage.color as color
from skimage.util import img_as_ubyte
from scipy import ndimage as ndi
from skimage import io
from joblib import load
import os

DATASET_PATH = "/home/carter/Desktop/CVPPP2017_LSC/"

"""
Segment images in a given dataset path with a specified method
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
:return: a binary segmented image
"""
def green_channel_thresh(img):
    green_channel = img[:,:,1] # get the green channel
    return green_channel > 100 # get pixels where green channel > 100

"""
Local thresholding using the scipy's built in threshold_local
:param img: the image to segment
:return: a binary segmented image
"""
def local_thresh(img):
    green_channel = img[:,:,1]
    thresh = filters.threshold_local(green_channel,block_size=51, offset=10) 
    return green_channel > thresh


def logistic_regression(img):
    shape = img[:,:,0].shape
    img = img[:,:,:3].reshape(-1, 3)
    clf = load('logistic.joblib')
    return clf.predict(img).reshape(*shape).astype(np.uint8)

def naive_bayes(img):
    shape = img[:,:,0].shape
    img = img[:,:,:3].reshape(-1, 3)
    clf = load('naive_bayes.joblib')
    return clf.predict(img).reshape(*shape).astype(np.uint8)

def logistic_and_smooth(img):
    shape = img[:,:,0].shape
    img = filters.gaussian(img[:,:,:3], sigma=2, multichannel=True, preserve_range=True)
    img = img.reshape(-1, 3)
    clf = load('logistic.joblib')

    # get prediction from logistic regression
    prediction = clf.predict(img).reshape(*shape)

    # if there are enough white pixels total, remove small clusters of pixels
    # otherwise just return the predicted image
    min_size = 1000
    if np.sum(prediction)/255 > min_size*4:
        # Remove clusters of 1 smaller than a given size (1000)
        label_objects, _ = ndi.label(prediction)
        sizes = np.bincount(label_objects.ravel())
        mask_sizes = sizes > min_size
        mask_sizes[0] = 0
        return img_as_ubyte(mask_sizes[label_objects])
    else:
        return prediction.astype(np.uint8)

def logistic_and_edges(img):
    # detect edges in image (canny?)
    # detect plant colored pixels with logistic regression
    # take intersection of two images (to get edges which are also plant color, presumably)
    # blur??
    # fill in voids with ndi.binary_fill_holes
    return img

def main():
    segment(DATASET_PATH, logistic_and_smooth)

if __name__ == "__main__":
    main()
# %%
