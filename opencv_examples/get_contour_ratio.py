import argparse
import cv2
import numpy as np
import os

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", required = True)
args = parser.parse_args()

def get_countour_ratio(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh_a = cv2.adaptiveThreshold(gray, 255,
                               cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY, 11, 2)
    return 1 - np.count_nonzero(thresh_a) / (thresh_a.shape[0] * thresh_a.shape[1])

dir_path = args.file
if os.path.isfile(dir_path):
    contours = get_countour_ratio(dir_path)
    # contours.to_csv(path.split(".")[0] + ".csv", index = False)
elif os.path.isdir(dir_path):
    print("running on a folder...")
    files = os.listdir(dir_path)
    contours = [(file, get_countour_ratio(os.path.join(dir_path, file))) \
                for file in files \
                if file.endswith(".jpg") \
                if os.path.getsize(os.path.join(dir_path, file)) > 0]
    # pd.concat(contours).to_csv(path + "/contours.csv", index = False)

print(contours)
