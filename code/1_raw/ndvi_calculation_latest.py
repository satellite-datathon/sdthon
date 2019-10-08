
# coding: utf-8

# In[42]:


import cv2
import numpy as np
import glob
from skimage.util import img_as_float

from matplotlib import pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[43]:


def harvested_Area(har):
    harvested = ndvi < 0.32
    harvested = harvested.astype(np.int)
    area = harvested.sum()* 100
    return (area)


# In[44]:


#ban8 = cv2.imread('data/sentinel-2a-tile-7680x-10240y/timeseries/7680-10240-B08-2019-05-11.png')
#ban4 = cv2.imread('data/sentinel-2a-tile-7680x-10240y/timeseries/7680-10240-B04-2019-05-11.png')


# In[45]:


band8_files = glob.glob(r'E:\DataSets\phase-01-rev1.12\phase-01\data\sentinel-2a-tile-7680x-10240y\timeseries\7680-10240-B08*.png')
band4_files = glob.glob(r'E:\DataSets\phase-01-rev1.12\phase-01\data\sentinel-2a-tile-7680x-10240y\timeseries\7680-10240-B04*.png')
band8_files.sort()
band4_files.sort()


# In[46]:


ndvi_mean=[]
dates= []
harv_area = []

for band4_file,band8_file in zip(band4_files, band8_files):
    dates.append(band4_file[-14:-4])
    
    band4 = cv2.imread(band4_file)
    band8 = cv2.imread(band8_file)
    
    ndvi = (band8.astype(float) - band4.astype(float))/(band8.astype(float)+band4.astype(float))
    area = harvested_Area(ndvi) #in mtr squr
    

    image = img_as_float(ndvi)
    image = image[:, :, ::-1]
    
    ndvi_mean.append(ndvi.mean())
    harv_area.append(area/10000) #in hectares

#     plt.imshow(image,cmap='RdYlGn')


# In[48]:


plt.plot(dates[:6], harv_area[:6])


# In[49]:


harv_area
final_list = list(zip(dates,ndvi_mean,harv_area))
final_df = pd.DataFrame(final_list,columns=['date','ndvi','ha_area'])
final_df.head()


# In[ ]:


cv2.imwrite('E:\DataSets\man_ndvi.png',ndvi)


# In[21]:


from PIL import Image
# img = Image.open('E:\DataSets\man_ndvi.png')
# img.save('E:\DataSets\image.tiff')
plt.imshow(ndvi)

