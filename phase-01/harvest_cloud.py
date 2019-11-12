from PIL import Image, ImageDraw
import glob
import os
import cv2
from matplotlib import pyplot as plt

os.chdir("C:/cygwin64/home/Brendan/sdthon/phase-01/data/sentinel-2a-tile-7680x-10240y/timeseries")
mask=Image.open("C:/cygwin64/home/Brendan/sdthon/phase-01/data/sentinel-2a-tile-7680x-10240y/masks/tileX7680-tileY10240-mask-sugarcane.png")
arr = glob.glob('*-*-TCI*.png')

#for k in arr:
#	harvest_cloud(k)
	
k = arr[2]	
harvest_cloud(k)
#https://stackoverflow.com/questions/43661868/hsi-color-format-in-python-with-opencv-library
#https://theailearner.com/tag/hsi-model/
"""
img = cv2.imread(k)
img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
cv2.imshow('image', img)

color = ('b','g','r')
for i,col in enumerate(color):
    histr = cv2.calcHist([img],[i],None,[256],[0,256])
    plt.plot(histr,color = col)
    plt.xlim([0,256])
plt.show()

hist_full = cv2.calcHist([img],[2],None,[256],[0,256])
plt.plot(hist_full)

h, s, i = cv2.split(img)
"""

def harvest_cloud(k):
    tile = Image.open(k)
    date = k[15:25]
    pixels = tile.load()
    img = cv2.imread(k)
    img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    date=k[15:25]
    overlay=mask.load()
    for y in range(512):
        for x in range(512):
            if overlay[y,x]==(0, 0, 0, 255):
                hue=img[y,x][0]
                saturation=img[y,x][1]
                intensity=img[y,x][2]

                #print("%s %s %s %s %s" % (x, y, hue, saturation, intensity))
                if hue > 50 | intensity > 70:
                    print("hue > 50 | intensity > 70: x=%s, y=%s, h=%s, s=%s, i=%s" % (x, y, hue, saturation, intensity))
                    pixels[y,x]=(255,0,0)
    tile.save('../../cloud'+date+'.png')
    cv2.imwrite('../../cloud/'+date+'_hsi.png', img)

"""
df = pd.DataFrame(h)
plt.hist(df)
df = pd.DataFrame(s)
plt.hist(df)
df = pd.DataFrame(i)
plt.hist(df)
"""
