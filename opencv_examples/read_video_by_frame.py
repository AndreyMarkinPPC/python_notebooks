import cv2
import youtube_dl
import pafy
import argparse
import pandas as pd
import os

# parser = argparse.ArgumentParser()
# 
# parser.add_argument("-f", "--input-file", required = True)
# args = parser.parse_args()
# print(args)
if True:
    data = pd.read_csv("videos/input/videos.csv")
    for video in data["ytid"]:
        url = 'https://youtu.be/%s' %(video)
        if os.path.isdir("videos/%s/" %(video)):
            print("%s is already fetched, skipping..." %(video))
        else:
            try:
                vPafy = pafy.new(url)
                play = vPafy.getbest(preftype="webm")
                cap = cv2.VideoCapture(play.url)
                seconds = 1
                fps = cap.get(cv2.CAP_PROP_FPS) # Gets the frames per second
                multiplier = fps * seconds
                # print(multiplier)
                # print(cap.get(cv2.CAP_PROP_FPS))
                ret = True
                print("running for video %s" %(video))
                os.mkdir("videos/%s/" %(video))
                while (ret):
                    frameId = int(round(cap.get(1)))
                    ret,frame = cap.read()
                    if frameId % multiplier == 0:
                        # print("saving...")
                        if frameId / multiplier < 10:
                            cv2.imwrite("videos/%s/frame_0%d.jpg" % (str(video), int(frameId / multiplier)), frame)
                        else:
                            cv2.imwrite("videos/%s/frame_%d.jpg" % (str(video), int(frameId / multiplier)), frame)
            except OSError as error:
                print(error)
