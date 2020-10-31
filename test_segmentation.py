# %%
import os
from PIL import Image
import numpy as np
from sklearn.metrics import jaccard_score
from datetime import datetime

# Path to CVPPP Dataset "training" folder
DATASET_PATH = "/home/carter/Desktop/CVPPP2017_LSC/training/"
# Path to data that we want to test
# Similarly should be link to folder containing A1, A2, A3, A4 folders
# Output files should be in the same location and have the same name as the ground truth
# e.g. "DATASET_PATH/A4/plant0441_fg.png" should correspond to test "TEST_DATA_PATH/A4/plant0441_fg.png"
TEST_DATA_PATH = "/home/carter/Desktop/CVPPP2017_LSC/green_channel_thresh/"

def write_to_file(scores):
    with open(TEST_DATA_PATH + "evaluation_results.txt", "w") as file:
        file.write(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "\n")
        file.write("Mean Jaccard Score: " + str(np.mean(scores)) + "\n \n")
        file.write(str(scores))

def main():
    # Get the partial paths (e.g. A4/plant0574_fg.png) of every image in dataset
    image_paths = [] # Segmentation ground truth (_fg.png)
    for subfolder in os.listdir(DATASET_PATH):
        for f in os.listdir(DATASET_PATH + subfolder):
            if "_fg.png" in f:
                image_paths.append(subfolder + "/" + f)

    # Calculate jaccard score for each pair of ground truth and test images
    jaccard_scores = []
    for img in image_paths:
        # read in images as flat numpy array
        ground_truth = np.array(Image.open(DATASET_PATH + "/" + img)).flatten()
        test = np.array(Image.open(TEST_DATA_PATH + "/" + img)).flatten()
        # normalize value to be 0 or 1
        ground_truth = ground_truth/np.max(ground_truth)
        test = test/np.max(test)
        
        jaccard_scores.append(jaccard_score(ground_truth, test))
        print(img)

    write_to_file(jaccard_scores)

if __name__ == "__main__":
    main()
# %%
