import os
import numpy as np
import pandas as pd
from sys import argv
from datetime import datetime
from skimage.io import imread
from multiprocessing import Pool
from imageai.Detection import ObjectDetection


IMAGE_PATH = '../data/challenge2018_test'
OUTPUT_PATH = '../output/'


def usage():
    print("Usage: python " + argv[0] + " model_file")


def getRev():
    import json
    mapping = json.load(open('../data/imagenet_encoding.json', 'r'))
    return dict([(key, val) for val, key in mapping.items()])


def getImageIds():
    return pd.read_csv('../data/sample_submission.csv')["ImageId"].tolist()


def predict(img_id, detector, output_dir, rev):
    img_file = os.path.join(IMAGE_PATH, img_id + ".jpg")
    if not os.path.exist(img_file):
        print("Error: " + img_file + "does not exist!")
        return ""
    print("Processing image file: " + img_file + " ...")
    H, W, _ = imread(img_file).shape()
    output_file = os.path.join(output_dir, img_id + "_detected.jpg")
    detections = detector.detectObjectsFromImage(
        input_image=img_file, output_image_path=output_file, minimum_percentage_probability=40)
    pred_str = ""
    for obj in detections:
        if obj['name'] not in rev:
            continue
        pred_str += rev[obj['name']] + " " + str(obj['percentage_probability'] / 100.) + " "
        ym, yM, xm, xM = obj["box_points"]
        pred_str += str(xm*1. / W) + " " + str(xM * 1. / W) + " " + str(ym * 1. / H) + " " + str(yM * 1. / H) + " "
    return pred_str[: -1]


def main():
    if len(argv) < 2:
        usage()
        return
    model_weight_path = argv[1]
    detector = ObjectDetection()
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath(model_weight_path)
    detector.loadModel()

    rev = getRev()
    label = str(datetime.now())
    output_dir = os.path.join(OUTPUT_PATH, label)
    subm_file = os.path.join(output_dir, "sumb.csv")
    imgIds = getImageIds()
    predictions = [predict(img_id, detector, output_dir, rev) for img_id in imgIds]
    subm = pd.DataFrame({
        "ImageId": imgIds,
        "PredictionString": predictions
    })
    subm.to_csv(subm_file, index=False)
    print("DONE!")
