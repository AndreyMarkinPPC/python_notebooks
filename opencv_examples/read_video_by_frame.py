import cv2
import youtube_dl
import pafy

url = 'https://youtu.be/feRrKiZRw04'
vPafy = pafy.new(url)
play = vPafy.getbest(preftype="webm")
cap = cv2.VideoCapture(play.url)
seconds = 1
fps = cap.get(cv2.CAP_PROP_FPS) # Gets the frames per second
multiplier = fps * seconds
print(multiplier)
print(cap.get(cv2.CAP_PROP_FPS))
ret = True
while (ret):
    frameId = int(round(cap.get(1)))
    ret,frame = cap.read()
    if frameId % multiplier == 0:
        # print("saving...")
        if frameId / multiplier < 10:
            cv2.imwrite("videos/sample_video/frame_0%d.jpg" % int(frameId / multiplier) , frame)
        else:
            cv2.imwrite("videos/sample_video/frame_%d.jpg" % int(frameId / multiplier) , frame)
