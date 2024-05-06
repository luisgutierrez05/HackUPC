import pandas as pd
import numpy as np
import time

PATH = '../data/'
df = pd.read_csv(PATH + 'raw_data.csv')

ROWS = df.shape[0]
COLS = df.shape[1]

from PIL import Image, ImageDraw
import urllib.request

def get_image(URL):
    urllib.request.urlretrieve(URL, "img.png")
    img = Image.open("img.png")
    return img

images = []
for i in range(100):
    for j in range(COLS):
        url = df.iloc[i, j]
        if pd.isna(url):
            continue
        image = get_image(url)
        images.append(image)
        time.sleep(4)