"""
Performs segmentation on an image according to the specified segmentation method
Multiple segmentation methods are defined within the script, and more can be added easily
Written for use on CVPPP2017 dataset
"""
import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import skimage.color as color
import skimage.data as data
import skimage.draw as draw
import skimage.filters as filters
import skimage.segmentation as seg
from joblib import load
from scipy import ndimage as ndi
from skimage import io
from skimage.feature import canny
from skimage.util import img_as_ubyte

DATASET_PATH = "/home/carter/Desktop/CVPPP2017_LSC/"

"""
Segment images in a given dataset path with a specified method
Performs segmentation and outputs results to a folder with the name of the segmentation method
:param input_path: the path to the dataset to segment, e.g. /home/carter/Desktop/CVPPP2017_LSC/training/
:param method: the segmentation method to use - should work on a single image. See green_channel_thresh
"""
def segment(input_path, method, params=None):
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
        segmented_img = method(img, *params)
        path = path.replace("rgb", "fg") # Change file name to fg from rgb to match ground truth
        io.imsave(output_path + path, segmented_img)
        #print("segment:", path)

"""
Simple thresholding based on the value of the green channel
:param img: the image to segment
:return: a binary segmented image (0 = bg, 255 = plant)
"""
def green_channel_thresh(img):
    green_channel = img[:,:,1] # get the green channel
    return green_channel > 100 # get pixels where green channel > 100

"""
Per-pixel color based thresholding based on a logistic regression formula
Logistic regression model is trained with train_logistic.py and saved in logistic.joblib
:param img: the image to segment
:param thresh: threshold for deciding whether a pixel is bg or plant -
    higher thresh means less plant
:return: a binary segmented image (0 = bg, 255 = plant)
"""
def logistic_regression(img, thresh=0.5):
    shape = img[:,:,0].shape
    img = img[:,:,:3].reshape(-1, 3)
    clf = load('logistic.joblib')
    temp = clf.predict_proba(img)[:,1]
    return np.where(temp > thresh, 255, 0).reshape(*shape).astype(np.uint8)

"""
Per-pixel color based thresholding based on a naive bayes classifier
Naive Bayes model is trained with train_bayes.py and saved in naive_bayes.joblib
:param img: the image to segment
:return: a binary segmented image (0 = bg, 255 = plant)
"""
def naive_bayes(img):
    shape = img[:,:,0].shape
    img = img[:,:,:3].reshape(-1, 3)
    clf = load('naive_bayes.joblib')
    return clf.predict(img).reshape(*shape).astype(np.uint8)

"""
Smoothed version of logistic_regression model
:param img: the image to segment
:param thresh: thresh parameter to be passed to logistic_regression method
:param min_size: minimum size of clustered pixels to be kept - anything smaller will be filled in
:param sigma: sigma of gaussian filter to apply before performing logistic regression and denoising
"""
def logistic_and_smooth(img, thresh=0.5, min_size=1000, sigma=2):
    shape = img[:,:,0].shape
    img = filters.gaussian(img[:,:,:3], sigma=sigma, multichannel=True, preserve_range=True)
    img = img.reshape(-1, 3)
    clf = load('logistic.joblib')

    # get prediction from logistic regression
    temp = clf.predict_proba(img)[:,1]
    prediction = np.where(temp > thresh, 1, 0).reshape(*shape)

    # if there are enough white pixels total, remove small clusters of pixels
    # otherwise just return the predicted image
    # Remove clusters of 1 smaller than a given size (1000)
    label_objects, _ = ndi.label(prediction)
    sizes = np.bincount(label_objects.ravel())
    mask_sizes = sizes > min_size
    mask_sizes[0] = 0

    # if we didn't just remove the whole image when we removed small clusters
    if np.count_nonzero(img_as_ubyte(mask_sizes[label_objects])) != 0:
        return img_as_ubyte(mask_sizes[label_objects])
    else:
        return prediction.astype(np.uint8)*255

"""
Use slic (k-means clustering) and the per-pixel logistic regression model to first split the image
into a number of segments, then classify the segments which are suffeciently "plant colored" as found
by the logistic regression model as plant and the rest as background
:param img: the image to segment
:param n_segments: how many segments to segment the image into with k-means clustering
:param percent_thresh: (0-1 float) what percentage of each cluster must be plant colored to classify as plant
:param log_thresh: (0-1 float) logistic regresison threshold to pass to logistic_regression method (see logistic_regression)
:param sigma: sigma of gaussian filter to apply before performing k-means and logistic
"""
def slic(img, n_segments=50, percent_thresh=0.5, log_thresh=0.8, sigma=0):
    img_slic = seg.slic(img[:,:,:3], n_segments=n_segments, start_label=1) # need to mess with parameters
    img_log = (logistic_regression(img, thresh=log_thresh)/255).astype(np.uint8)
    final_mask = np.zeros(img.shape[:2]).astype(np.uint8)

    # while we still haven't found any plant colored points
    while np.count_nonzero(final_mask) == 0 and percent_thresh > 0:
        for i in range(n_segments):
            binary_slic = np.where(img_slic==i, 1, 0).astype(np.uint8)
            percent_green = np.count_nonzero(cv2.bitwise_and(binary_slic, img_log)) / (np.count_nonzero(binary_slic)+1)
            if percent_green > percent_thresh: # if there's enough plant color in the cell to meet the threshold
                final_mask = cv2.bitwise_or(final_mask, binary_slic).astype(np.uint8)
        percent_thresh -= 0.05 # lower the threshold until we find some plant color

    # img_slic_rgb = color.label2rgb(img_slic, img, kind='avg')
    # io.imshow(img_slic_rgb)
    # io.show()
    return final_mask*255

def main():
    segment(DATASET_PATH, logistic_and_smooth, [0.1, 100, 0.0])

if __name__ == "__main__":
    main()