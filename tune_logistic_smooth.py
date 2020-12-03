import evaluate_segmentation
import segment
import numpy as np

DATASET_PATH = "/home/carter/Desktop/CVPPP2017_LSC/"

for thresh in [0.08, 0.1, 0.12]:
    for min_size in [100, 150, 200]:
        for sigma in [1.0]:
            label = str(thresh) + " / " + str(min_size) + " / " + str(sigma)

            print("segmenting", label)
            segment.segment(DATASET_PATH, segment.logistic_and_smooth, params=[thresh, min_size, sigma])

            print("evaluating", label)
            jaccard, f1 = evaluate_segmentation.evaluate(DATASET_PATH+"training/", DATASET_PATH+"logistic_and_smooth/")
            
            with open(DATASET_PATH + "logistic_and_smooth/" + "optimization.txt", "a") as file:
                file.write(label)
                file.write(" Jaccard: " + str(np.mean(jaccard)) + "\n")