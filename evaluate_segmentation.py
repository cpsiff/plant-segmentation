"""
Tests the accuracy of segmentation using Jaccard score and f1 score
Writes results to a file and saves a histogram of jaccard and f1 score distributions
Written for use on CVPPP2017 dataset, works on any dataset with the same file structure
"""
import os
from PIL import Image
import numpy as np
from sklearn.metrics import jaccard_score
from sklearn.metrics import f1_score
from datetime import datetime
import matplotlib.pyplot as plt

# Path to CVPPP Dataset "training" folder
GROUND_TRUTH_PATH = "/home/carter/Desktop/CVPPP2017_LSC/training/"
# Path to data that we want to evaluate
# Similarly should be path to folder containing A1, A2, A3, A4... subfolders
# Output files should be in the same location and have the same name as the ground truth
# e.g. "GROUND_TRUTH_PATH/A4/plant0441_fg.png" should correspond to test "EVAL_DATA_PATH/A4/plant0441_fg.png"
EVAL_DATA_PATH = "/home/carter/Desktop/CVPPP2017_LSC/logistic_and_smooth/"

"""
Write jaccard and f1 scores to file at EVAL_DATA_PATH/evaluation_results.txt
:param jaccard_scores: 1d numpy array of jaccard scores to write
:param f1_scores: 1d numpy array of f1 scores to write
"""
def write_to_file(jaccard_scores, f1_scores):
    with open(EVAL_DATA_PATH + "evaluation_results.txt", "w") as file:
        file.write(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "\n")
        file.write("Mean Jaccard Score: " + str(np.mean(jaccard_scores)) + "\n")
        file.write("Mean f1 score: " + str(np.mean(f1_scores)) + "\n\n")
        file.write("Jaccard scores: " + str(jaccard_scores) + "\n")
        file.write("f1 scores: " + str(f1_scores))

"""
Plot distribution of given jaccard and f1 scores as a histogram
Save result to EVAL_DATA_PATH/eval.png
:param jaccard: 1d numpy array of jaccard scores
:param f1: 1d numpy array of f1 scores
"""
def plot_histogram(jaccard, f1):
    fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)

    # We can set the number of bins with the `bins` kwarg
    axs[0].hist(jaccard, bins=20)
    axs[0].set_title("Mean Jaccard Score: " + str(np.mean(jaccard))[:4])
    axs[0].set_ylabel("# of occurences")
    axs[0].set_xlabel("Jaccard Score")
    axs[1].hist(f1, bins=20)
    axs[1].set_title("Mean f1 Score: " + str(np.mean(f1))[:4])
    axs[1].set_xlabel("f1 Score")
    fig.savefig(EVAL_DATA_PATH + "eval.png")

"""
Run the evaluation, write resulting jaccard and f1 scores to a file and save histogram
of scores to file. 
Scores are saved to eval_data_path/evaluation_results.txt
Histogram is saved to eval_data_path/eval.png
:param ground_truth_path: path to the ground truth folders (GROUND_TRUTH_PATH global when running directly)
:param eval_data_path: path to the eval folders (EVAL_DATA_PATH global when running direcly)
"""
def evaluate(ground_truth_path, eval_data_path):
    # Get the partial paths (e.g. A4/plant0574_fg.png) of every image in dataset
    image_paths = [] # Segmentation ground truth (_fg.png)
    for subfolder in os.listdir(ground_truth_path):
        for f in os.listdir(ground_truth_path + subfolder):
            if "_fg.png" in f:
                image_paths.append(subfolder + "/" + f)

    # Calculate jaccard score and f1 score for each pair of ground truth and test images
    jaccard_scores = []
    f1_scores = []
    for img in image_paths:
        print("eval:", img)
        # read in images as flat numpy array
        ground_truth = np.array(Image.open(ground_truth_path + "/" + img)).flatten()
        test = np.array(Image.open(eval_data_path + "/" + img)).flatten()
        # normalize value to be 0 or 1
        ground_truth = ground_truth/np.max(ground_truth)
        test = test/np.max(test)
        test[np.isnan(test)] = 0
        jaccard_scores.append(jaccard_score(ground_truth, test))
        f1_scores.append(f1_score(ground_truth, test))

    write_to_file(jaccard_scores, f1_scores)
    plot_histogram(jaccard_scores, f1_scores)

    return (jaccard_scores, f1_scores)

def main():
    evaluate(GROUND_TRUTH_PATH, EVAL_DATA_PATH)

if __name__ == "__main__":
    main()
