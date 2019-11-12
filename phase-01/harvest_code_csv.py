from PIL import Image
import cv2
import numpy as np
import pandas as pd

import os
os.chdir("C:/cygwin64/home/br075246/sdthon/sdthon/phase-01")
mask=Image.open("./data/sentinel-2a-tile-7680x-10240y/masks/tileX7680-tileY10240-mask-sugarcane_v0.png")
arr= os.listdir("./data/sentinel-2a-tile-7680x-10240y/timeseries")

final = pd.DataFrame()
names = ['harvested', 'date', 'x', 'y']

for k in arr:
    if "TCI" in k:
        tile= Image.open("./data/sentinel-2a-tile-7680x-10240y/timeseries/"+k)
        date=k[15:25]

        pixels=tile.load()
        overlay=mask.load()

        img = cv2.imread("./data/sentinel-2a-tile-7680x-10240y/timeseries/"+k)
        img_mask = cv2.imread("./data/sentinel-2a-tile-7680x-10240y/masks/tileX7680-tileY10240-mask-sugarcane_v0.png", 0)
        mask_b = np.where(img_mask > 0, 1, 0)
        #img_sugar = np.where(img_mask > 0, img, [0, 0, 0])

        b, g, r = cv2.split(img)
        s_m = (g.astype(int) / (b.astype(int) + g.astype(int) + r.astype(int)))
        s_m = np.where(s_m < 0.32, 1, 0)

        img_sugar = np.where(mask_b == 0, s_m, 0)
        #sugar_m = np.where(img_sugar[0] / (img_sugar[0] + img_sugar[1] + img_sugar[2]) < 0.32, 1, 0)
        h = np.sum(img_sugar)
        print("s1, %s, %s: %s" % (k, date, h))

        sugar = 0
        for y in range(512):
            for x in range(512):
                if overlay[y,x]==(0, 0, 0, 255):
                    red=pixels[y,x][0]
                    green=pixels[y,x][1]
                    blue=pixels[y,x][2]
                    channelPortion=(green/(green+red+blue))
                    if channelPortion <0.32:
                        # if the ratio of green to the rest is less than 0.32, then it has been harvested
                        # if mask is black?
                        pixels[y,x]=(255,0,0)
                        sugar += 1

        print("s2, %s, %s: %s" % (k, date, sugar))
        tile.save("./data/harvested/"+date+".png")

        x = k.split("-")[0]
        y = k.split("-")[1]
        r = pd.DataFrame([[h, date, x, y]], columns=names)
        final = final.append(r)

final.head()
final.to_csv("harvested.csv", header=True, index=False)




