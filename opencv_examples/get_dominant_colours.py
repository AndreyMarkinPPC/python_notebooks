import cv2
import numpy as np
import pandas as pd

def get_dominant_colours(path, threshold = 0.001):
    img = cv2.imread(path)
    height, width, _ = np.shape(img)

    # reshape image to be list of rgb pixels
    image = img.reshape((height * width, 3))

    # define data frame
    df = pd.DataFrame(image, columns = ['b', 'g', 'r'])

    # calculate proportions
    df = df.groupby(['r','g', 'b']).size().sort_values(ascending=False)\
            .reset_index(name='count').drop_duplicates()\
            .query('count > 100')
    df["prop"] = df["count"] / sum(df["count"])
    df = df.query("prop > %f" %(threshold))
    return df


print(get_dominant_colours('videos/j8bigiNKox8/frame_07.jpg'))
