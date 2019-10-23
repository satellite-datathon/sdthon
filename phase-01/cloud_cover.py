#!/usr/bin/env python
# coding: utf-8

import cv2
import numpy as np
import glob
from skimage.util import img_as_float
import pandas as pd
import os


os.chdir("../data/phase-02/sugarcanetiles")
b1 = cv2.imread('1536-1024-B01-2016-12-22.png')
b2 = cv2.imread('1536-1024-B02-2016-12-22.png')
b3 = cv2.imread('1536-1024-B03-2016-12-22.png')
b4 = cv2.imread('1536-1024-B04-2016-12-22.png')

band1_files = glob.glob('*-*-B01*.png')
band2_files = glob.glob('*-*-B02*.png')
band3_files = glob.glob('*-*-B03*.png')
band4_files = glob.glob('*-*-B04*.png')
print(len(band1_files))

tiles = pd.read_csv("../../1_raw/tiles.csv")

def get_band(x, y, b):
    band_files = glob.glob('%s-%s-B0%s-*.png' % (x, y, b))
    band_files.sort()
    return(band_files) 

def get_mask(x, y):
    mask_file = glob.glob('../masks/mask-x%s-y%s.png' % (x, y))[0]
    return(mask_file)

def clip(a):
    if (a >= 0) & (a <= 1):
        return a
    elif a > 1:
        return 1
    else:
        return 0

# https://stackoverflow.com/questions/39109045/numpy-where-with-multiple-conditions/39111919
# http://www.pythonfmask.org/en/latest/
def gen_ngdr(x, y):
    b1_files = get_band(x, y, 1)
    b2_files = get_band(x, y, 2)
    b3_files = get_band(x, y, 3)
    b4_files = get_band(x, y, 4)

    mask_file = get_mask(x, y)
    img_mask = cv2.imread(mask_file, 0)
    mask_b = np.where(img_mask > 0, 1, 0)

    final = pd.DataFrame()
    names = ['cloud', 'cloud_m', 'date', 'x', 'y']

    for b1_file, b2_file, b3_file, b4_file in zip(b1_files, b2_files, b3_files, b4_files):
        klist = b1_file.split("-")
        date = klist[3] + "-" + klist[4] + "-" + klist[5].replace(".png", "")

        band1 = cv2.imread(b1_file)
        band2 = cv2.imread(b2_file)

        b1 = img_as_float(band1)
        b2 = img_as_float(band2)

        # try values of 0.27 and 0.115 b/c recommended values of 0.175 and 0.39 were producing low values of cloud cover
        bRatio = (b1 - 0.115) / (0.27 - .115)
        ngdr = (b1 - b2)/(b1 + b2)

        cloud_mask = np.where((bRatio > 1) | ((bRatio > 0) & (ngdr > 0)), 1, 0)
        cloud_mask_less_mask = np.where(mask_b == 0, cloud_mask[:,:,2], 0)

        c = np.sum(cloud_mask[:,:,0])
        cloud_mask_less_mask = np.where(cloud_mask_less_mask == 0, np.nan, cloud_mask_less_mask)
        cc_m = np.nanmean(cloud_mask_less_mask)

        total_pixels = 262144 #- np.sum(mask_b)
        perc_cloud = round(100 * c / total_pixels)

        if c > 0:
            print("s1, %s, %s, cloud: %s, perc cloud: %s" % (b1_file, date, c, perc_cloud))

        r = pd.DataFrame([[c, cc_m, date, x, y]], columns=names)
        final = final.append(r)

    return(final)


# this is the tile from phase-01
x = 7680
y = 10240
df = gen_ngdr(x, y)
df.iloc[0,:]
df.to_csv("../../../phase-01/cloud_cover.csv", header=True, index=False)

"""
def get_df_from_tile(tile):
   x = tile['tile_x']
   y = tile['tile_y']
   ngdr_df = gen_ngdr(x, y)
   print(x, y)
   ngdr_df.iloc[0,:]
   return(ngdr_df)

tile = tiles.iloc[0,:]
ngdr_df = get_df_from_tile(tile)
df = ngdr_df 
df

for i in range(1, tiles.shape[0]):
    print(i)
    tile = tiles.iloc[i,:]
    ngdr_df = get_df_from_tile(tile)
    df = df.append(ngdr_df)

df.head()
df.shape
df.tail()
"""

#df.to_csv("../../2_processed/phase-02_cloud_cover.csv", header=True, index=False)


