import evaluate_segmentation
import segment
import numpy as np

DATASET_PATH = "/home/carter/Desktop/CVPPP2017_LSC/"

for n_segments in [100, 200]:
    for percent_thresh in [0.1, 0.3]:
        for log_thresh in [0.1, 0.3]:
            for sigma in [0, 10]:
                label = str(n_segments) + " / " + str(percent_thresh) + " / " + str(log_thresh) + " / " + str(sigma)

                print("segmenting", label)
                segment.segment(DATASET_PATH, segment.slic, params=[n_segments, percent_thresh, log_thresh, sigma])

                print("evaluating", label)
                jaccard, f1 = evaluate_segmentation.evaluate(DATASET_PATH+"training/", DATASET_PATH+"slic/")
                
                with open(DATASET_PATH + "slic/" + "optimization.txt", "a") as file:
                    file.write(label)
                    file.write(" Jaccard: " + str(np.mean(jaccard)) + "\n")