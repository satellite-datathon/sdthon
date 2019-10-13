import cv2
import numpy as np
import pandas as pd
import glob

import os

os.chdir("C:/cygwin64/home/br075246/sdthon/sdthon/data/phase-02/sugarcanetiles")

final = pd.DataFrame()
names = ['harvested', 'date', 'x', 'y']

files = glob.glob('*-*-TCI-*.png')
for k in files:
    klist = k.split("-")
    date = klist[3] + "-" + klist[4] + "-" + klist[5].replace(".png", "")
    x = klist[0]
    y = klist[1]
    
    img = cv2.imread(k)
    img_mask = cv2.imread("../masks/mask-x%s-y%s.png" % (x, y), 0)
    mask_b = np.where(img_mask > 0, 1, 0)
    
    b, g, r = cv2.split(img)
    s_m = (g.astype(int) / (b.astype(int) + g.astype(int) + r.astype(int)))
    s_m = np.where(s_m < 0.32, 1, 0)
    
    img_sugar = np.where(mask_b == 0, s_m, 0)
    h = np.sum(img_sugar)
    print("s1, %s, %s: %s" % (k, date, h))
    
    r = pd.DataFrame([[h, date, x, y]], columns=names)
    final = final.append(r)

final.head()
final.to_csv("../harvested.csv", header=True, index=False)




