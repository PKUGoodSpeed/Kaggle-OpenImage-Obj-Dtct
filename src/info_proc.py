import os
import numpy as np
import pandas as pd

DATA_PATH = '../data'
TRAIN_PATH = '../data/train'
VALID_PATH = '../data/valid'

df = pd.read_csv(os.path.join(DATA_PATH, 'label_mapping.csv'))
annotations = pd.read_csv(os.path.join(DATA_PATH, 'train-annotations-bbox.csv'))

mapping = dict([(key, val) for key, val in df[['code', 'clsId']].values])

"""Create txt files for train and valid"""
def infoproc(path):
    for f in os.listdir(path):
        img_id = f.split('.')[0]
        spec = annotations[annotations.ImageID == img_id]
        with open(os.path.join(path, img_id + '.txt'), 'w') as fout:
            for label, xmin, xmax, ymin, ymax in spec[["LabelName", "XMin", "XMax", "YMin", "YMax"]].values:
                if label not in mapping:
                    print("WARNING: {} is not in the label mapping!!".format(label))
                c = mapping[label]
                x = (xmax + xmin)/2.
                y = (ymax + ymin)/2.
                width = xmax - xmin
                height = ymax - ymin
                fout.write("{0} {1} {2} {3} {4}\n".format(
                    str(c), str(x), str(y), str(width), str(height)))
        print("Greating info file: " + os.path.join(path, img_id + '.txt'))


if __name__ == "__main__":
    infoproc(TRAIN_PATH)
    infoproc(VALID_PATH)