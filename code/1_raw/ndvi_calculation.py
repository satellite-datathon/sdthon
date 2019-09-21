
# coding: utf-8

# In[17]:


import cv2
import numpy as np

from matplotlib import pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[18]:


ban8 = cv2.imread(r'E:\DataSets\phase-01-rev1.12\phase-01\data\sentinel-2a-tile-7680x-10240y\timeseries\7680-10240-B08-2019-05-11.png')


# In[19]:


ban4 = cv2.imread(r'E:\DataSets\phase-01-rev1.12\phase-01\data\sentinel-2a-tile-7680x-10240y\timeseries\7680-10240-B04-2019-05-11.png')


# In[20]:


ndvi = (ban8 - ban4)/(ban8+ban4).astype(np.float64)


# In[30]:


ndvi.shape


# In[21]:


cv2.imwrite('E:\DataSets\man_ndvi.png',ndvi)


# In[22]:


from PIL import Image
img = Image.open('E:\DataSets\man_ndvi.png')
img.save('E:\DataSets\image.tiff')


# In[27]:


plt.imshow(img)

