import os
import json
import cv2
import numpy as np
import argparse
import pandas as pd
from tqdm import tqdm


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", required = True)
args = parser.parse_args()

def get_clutter(path):

    # read image
    img = cv2.imread(path)
    # convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # perform adapative thresolding on blurred image
    thresh_a = cv2.adaptiveThreshold(cv2.medianBlur(gray, 7), 255,
                                                                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                                 cv2.THRESH_BINARY, 11, 2)
    return 1 - np.count_nonzero(thresh_a) / (thresh_a.shape[0] * thresh_a.shape[1])


path = args.file
if os.path.isfile(path):
    colours = get_clutter(args.file)
    print(colours)
    # colours.to_csv(path.split(".")[0] + ".csv", index = False)
elif os.path.isdir(path):
    input_dir = os.listdir(path)
    for files_ in tqdm(input_dir, desc="clutter"):
        files = os.listdir(os.path.join(path, files_))
        if "clutter.csv" in files:
            continue
        elif "videos.csv" in files or len(files) == 0:
            continue
        else:
            colours = [(files_, int(file.split("_")[1].split(".")[0]), \
                        get_clutter(os.path.join(path, files_, file))) \
                       for file in files \
                       if file.endswith(".jpg") \
                       if os.path.getsize(os.path.join(path, files_, file)) > 0]
            # pd.concat(colours).to_csv(path + "/colours.csv", index = False)
            colours = pd.DataFrame(colours, columns = ['ytid', 'timestamp', 'clutter_value'])
            colours.to_csv(path + "/" + files_ + "/clutter.csv", index=False)
