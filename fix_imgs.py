import cv2
import os
import io


for img in os.listdir("/home/carter/Desktop/our-data/training/imgs"):
    if "_fg" in img:
        print(img)
        #read image as grey scale
        img_grey = cv2.imread("/home/carter/Desktop/our-data/training/imgs/"+img, cv2.IMREAD_GRAYSCALE)

        # define a threshold, 128 is the middle of black and white in grey scale
        thresh = 128

        # threshold the image
        img_binary = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)[1]

        #save image
        cv2.imwrite("/home/carter/Desktop/our-data/training/imgs/"+img, img_binary) 