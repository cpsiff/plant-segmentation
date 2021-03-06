"""
Train a per-pixel naive bayes model to predict whether a pixel belongs to a plant or not
Uses the rgb values of the pixel
Trains on each pixel in the given dataset at once
Save trained classifier to naive_bayes.joblib
"""
from sklearn.naive_bayes import GaussianNB
from skimage import io
from joblib import dump
import numpy as np
import os
import re

DATASET_PATH = "/home/carter/Desktop/CVPPP2017_LSC/training/" # dataset to train on

rgb_paths = []
for subfolder in os.listdir(DATASET_PATH):
    for f in os.listdir(DATASET_PATH + subfolder):
        if "_rgb.png" in f:
            rgb_paths.append(subfolder + "/" + f)

X = np.array([])
y = np.array([])

for rgb_path in rgb_paths:
    fg_path = re.sub('rgb', 'fg', rgb_path)

    rgb_img = io.imread(DATASET_PATH + rgb_path)
    if X.size != 0:
        X = np.concatenate((X, rgb_img[:,:,:3].reshape(-1, 3)))
    else:
        X = rgb_img[:,:,:3].reshape(-1, 3)

    fg_img = io.imread(DATASET_PATH + fg_path)
    y = np.concatenate((y, fg_img.reshape(-1)))

print("training...")
clf = GaussianNB()
# print("selecting random indexes")
#random_indexes = np.random.choice(y.shape[0], 100000, replace=False)
clf.fit(X,y) # train sklearn naive bayes model

dump(clf, 'naive_bayes.joblib') # save trained model to file
