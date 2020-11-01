# %%
import os
from PIL import Image
import numpy as np
from sklearn.metrics import jaccard_score
from sklearn.metrics import f1_score
from datetime import datetime

# Path to CVPPP Dataset "training" folder
GROUND_TRUTH_PATH = "/home/carter/Desktop/CVPPP2017_LSC/training/"
# Path to data that we want to evaluate
# Similarly should be link to folder containing A1, A2, A3, A4 folders
# Output files should be in the same location and have the same name as the ground truth
# e.g. "GROUND_TRUTH_PATH/A4/plant0441_fg.png" should correspond to test "EVAL_DATA_PATH/A4/plant0441_fg.png"
EVAL_DATA_PATH = "/home/carter/Desktop/CVPPP2017_LSC/green_channel_thresh/"

def write_to_file(jaccard_scores, f1_scores):
    with open(EVAL_DATA_PATH + "evaluation_results.txt", "w") as file:
        file.write(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "\n")
        file.write("Mean Jaccard Score: " + str(np.mean(jaccard_scores)) + "\n")
        file.write("Mean f1 score: " + str(np.mean(f1_scores)) + "\n\n")
        file.write("Jaccard scores: " + str(jaccard_scores) + "\n")
        file.write("f1 scores: " + str(f1_scores))

def main():
    # Get the partial paths (e.g. A4/plant0574_fg.png) of every image in dataset
    image_paths = [] # Segmentation ground truth (_fg.png)
    for subfolder in os.listdir(GROUND_TRUTH_PATH):
        for f in os.listdir(GROUND_TRUTH_PATH + subfolder):
            if "_fg.png" in f:
                image_paths.append(subfolder + "/" + f)

    # Calculate jaccard score and f1 score for each pair of ground truth and test images
    jaccard_scores = []
    f1_scores = []
    for img in image_paths:
        # read in images as flat numpy array
        ground_truth = np.array(Image.open(GROUND_TRUTH_PATH + "/" + img)).flatten()
        test = np.array(Image.open(EVAL_DATA_PATH + "/" + img)).flatten()
        # normalize value to be 0 or 1
        ground_truth = ground_truth/np.max(ground_truth)
        test = test/np.max(test)
        
        jaccard_scores.append(jaccard_score(ground_truth, test))
        f1_scores.append(f1_score(ground_truth, test))
        print(img)

    write_to_file(jaccard_scores, f1_scores)

if __name__ == "__main__":
    main()
# %%
