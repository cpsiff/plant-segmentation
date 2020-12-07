# CS639 Computer Vision Final Project Fall 2020
Plant-background image segmentation
Marianne Bjorner and Carter Sifferman

## Scripts
### segment.py
Performs segmentation on an image according to the specified segmentation method. Multiple segmentation methods are defined within the script, and more can be added easily. Written for use on CVPPP2017 dataset.

### evaluate_segmentation.py
Tests the accuracy of segmentation using Jaccard score and f1 score. Writes results to a file and saves a histogram of jaccard and f1 score distributions. Written for use on CVPPP2017 dataset, works on any dataset with the same file structure

### train_bayes.py
Train a per-pixel naive bayes model to predict whether a pixel belongs to a plant or not. Uses the rgb values of the pixel and trains on each pixel in the given dataset at once. Save trained classifier to naive_bayes.joblib

### train_logistic.py
Train a per-pixel logistic regression model to predict whether a pixel belongs to a plant or not. Uses the rgb values of the pixel and trains on each pixel in the given dataset at once. Save trained classifier to logistic.joblib

### fix_imgs.py
Fix binary png images so that they're in a consistent binary format. Used for ground truth (_fg) images which can be saved by some image programs as 8 bit RGB pngs
rather than binary ones.

### tune_slic.py
Tune the parameters of the slic method in segment.py to get the best jaccard score. Results are saved in DATASET_PATH/slic/optimization.txt

### tune_logistic_smooth.py
Tune the parameters of the logistic_and_smooth method in segment.py to get the best jaccard score. Results are saved in DATASET_PATH/logistic_and_smooth/optimization.txt

### runFluorescentMethod.m
Performs segmentation according to altered [MultiLeafTracking](https://github.com/xiyinmsu/PlantVision) method on CVPPP2017 dataset. Original method developed for fluorescent imagery and videos.
