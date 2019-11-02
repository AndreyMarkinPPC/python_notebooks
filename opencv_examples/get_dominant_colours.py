import argparse
import cv2
import numpy as np
import pandas as pd
import webcolors
import os

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", required = True)
parser.add_argument("-t", "--threshold", required = False, type=float)
args = parser.parse_args()

def get_colour_name(rgb):
    min_colours = {}
    for key, name in webcolors.css21_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - rgb[0]) ** 2
        gd = (g_c - rgb[1]) ** 2
        bd = (b_c - rgb[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_dominant_colours(path, threshold = 0.001, names = False):
    img = cv2.imread(path)
    height, width, _ = np.shape(img)

    # reshape image to be list of rgb pixels
    image = img.reshape((height * width, 3))

    # define data frame
    df = pd.DataFrame(image, columns = ['b', 'g', 'r'])
    # calculate proportions
    df = df.groupby(['r','g', 'b']).size().sort_values(ascending=False)\
            .reset_index(name='count').drop_duplicates()
    df["prop"] = df["count"] / sum(df["count"])
    df = df.query("prop > %f" %(threshold))
    df = df.drop('count', axis = 1)
    df["ytid"] = os.path.dirname(path).split("/")[-1]
    df["frame"] = os.path.basename(path).split("_")[-1].split(".")[0]
    return df


# colours = get_dominant_colours("videos/sample_video/frame_13.jpg", threshold=0.0001)
path = args.file
if os.path.isfile(path):
    colours = get_dominant_colours(args.file, args.threshold)
    colours.to_csv(path.split(".")[0] + ".csv", index = False)
elif os.path.isdir(path):
    print("running on a folder...")
    files = os.listdir(path)
    colours = [get_dominant_colours(os.path.join(path, file), args.threshold) for file in files]
    pd.concat(colours).to_csv(path + "/colours.csv", index = False)

# [get_colour_name([c.r[0], c.g[0], c.g[0]]) for c in colours]
