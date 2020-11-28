# CS639 Computer Vision Final Project Fall 2020
Plant-background image segmentation
Marianne Bjorner and Carter Sifferman

## Scripts
### segment.py
Performs segmentation on an image according to the specified segmentation method. Multiple segmentation methods are defined within the script, and more can be added easily. Written for use on CVPPP2017 dataset, could be adapted to others by changing the way files are read.

### evaluate_segmentation.py
Tests the accuracy of segmentation using Jaccard score and f1 score. Writes results to a file and saves a histogram of jaccard and f1 score distributions. Written for use on CVPPP2017 dataset, could be adapted to others by changing the way files are read.

### train_bayes.py
Output to naive_bayes.joblib

### train_logistic.py
Output to logistic.joblib

### runFluorescentMethod.m
Performs segmentation according to altered [MultiLeafTracking](https://github.com/xiyinmsu/PlantVision) method on CVPPP2017 dataset. Original method developed for fluorescent imagery and videos.
