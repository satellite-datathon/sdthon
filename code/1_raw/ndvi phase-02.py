#!/usr/bin/env python
# coding: utf-8

import cv2
import numpy as np
import glob
from skimage.util import img_as_float
import pandas as pd
import os

from matplotlib import pyplot as plt

os.chdir("../../data/phase-02/sugarcanetiles")
files = glob.glob('*-*-B08*.png')
files[:10]

b8 = cv2.imread('1536-1024-B08-2016-12-22.png')
b8.astype(float)[0][0]

b4 = cv2.imread('1536-1024-B04-2016-12-22.png')
b4.astype(float)[0][0]

band8_files = glob.glob('*-*-B08*.png')
band4_files = glob.glob('*-*-B04*.png')
band8_files.sort()
band4_files.sort()

len(band8_files)
len(band4_files)

tiles = pd.read_csv("../../1_raw/tiles.csv")
dates = pd.read_csv("../../1_raw/dates.csv")

def gen_ndvi(band8_files, band4_files, mask_file):
    ndvi_mean=[]
    dates= []
    
    img_mask = cv2.imread(mask_file, 0)
    mask_b = np.where(img_mask > 0, 1, 0)
    
    for band4_file, band8_file in zip(band4_files, band8_files):
        dates.append(band4_file[-14:-4])
    
        band4 = cv2.imread(band4_file)
        band8 = cv2.imread(band8_file)
    
        b8 = img_as_float(band8)
        b4 = img_as_float(band4)
        ndvi = (b8 - b4)/(b8 + b4)

        ndvi_less_mask = np.where(mask_b == 0, ndvi[:,:,0], np.nan)
        ndvi_mean.append(np.nanmean(ndvi_less_mask))

    df = pd.DataFrame([dates, ndvi_mean]).T
    df.columns = ['dates', 'ndvi']
    return(df)


def get_band(x, y, b):
    band_files = glob.glob('%s-%s-B0%s-*.png' % (x, y, b))
    band_files.sort()
    return(band_files)


def get_mask(x, y):
    mask_file = glob.glob('../masks/mask-x%s-y%s.png' % (x, y))[0]
    return(mask_file)


tile = tiles.iloc[0,:]
x = tile['tile_x']
y = tile['tile_y']
band8_files = get_band(x, y, 8)
band4_files = get_band(x, y, 4)
mask_file = get_mask(x, y)
df = gen_ndvi(band8_files, band4_files, mask_file)
df.iloc[0,:]


def get_df_from_tile(tile):
   x = tile['tile_x']
   y = tile['tile_y']
   band8_files = get_band(x, y, 8)
   band4_files = get_band(x, y, 4)
   mask_file = get_mask(x, y)
   print(band8_files)
   print(band4_files)
   ndvi_df = gen_ndvi(band8_files, band4_files, mask_file)
   ndvi_df['x'] = x
   ndvi_df['y'] = y
   print(x, y)
   ndvi_df.iloc[0,:]
   return(ndvi_df)



tile = tiles.iloc[0,:]
ndvi_df = get_df_from_tile(tile)
df = ndvi_df 
df

for i in range(1, tiles.shape[0]):
    print(i)
    tile = tiles.iloc[i,:]
    ndvi_df = get_df_from_tile(tile)
    df = df.append(ndvi_df)


df.head()
df.shape
df.tail()

ndvi_df
df.append(ndvi_df)

df.to_csv("../../2_processed/phase-02_ndvi.csv", header=True, index=False)

