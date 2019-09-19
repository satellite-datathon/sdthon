
# coding: utf-8

# In[2]:


import cv2
import numpy as np
#import pycocotools
from matplotlib import pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[10]:


img = cv2.imread(r'E:\DataSets\phase-01-rev1.12\phase-01\data\sentinel-2a-tile-7680x-10240y\timeseries\7680-10240-TCI-2017-12-27.png')


# In[11]:


plt.hist(img.ravel(),256,[0,256]); plt.show()


# In[12]:


color = ('b','g','r')
for i,col in enumerate(color):
    histr = cv2.calcHist([img],[i],None,[256],[0,256])
    plt.plot(histr,color = col)
    plt.xlim([0,256])
plt.show()


# In[2]:


img_mask = cv2.imread(r'E:\DataSets\phase-01-rev1.12\phase-01\data\sentinel-2a-tile-7680x-10240y\masks\sugarcane-region-mask.png',0)


# In[26]:


#mask image calculation
masked_image = cv2.bitwise_and(img,img,mask = img_mask)
#img.shape
#img_mask.shape


# In[30]:


# Calculate histogram with mask and without mask
# Check third argument for mask
hist_full = cv2.calcHist([img],[2],None,[256],[0,256])
hist_mask = cv2.calcHist([img],[2],img_mask,[256],[0,256])

plt.subplot(221), plt.imshow(img, 'gray')
plt.subplot(222), plt.imshow(img_mask,'gray')
plt.subplot(223), plt.imshow(masked_image, 'gray')
plt.subplot(224), plt.plot(hist_full), plt.plot(hist_mask)
plt.xlim([0,256])

plt.show()


# In[ ]:


mask = np.asfortranarray(mask.astype(np.uint8))
mask = pycocotools.mask.encode(mask)          
area = float(pycocotools.mask.area(mask))


# In[6]:


img_mask


# In[7]:


mask_b = img_mask > 0


# mask_b

# In[17]:


mask_new = np.zeros((512,512))
for leng in np.arange(img_mask.shape[0]):
    for wid in np.arange(img_mask.shape[1]):
        if img_mask[leng,wid] > 0:
            mask_new[leng,wid] = 1
        else:
            mask_new[leng,wid] = 0


# In[20]:


mask_final = mask_new.astype(np.uint8)


# In[29]:


1 - (np.sum(mask_final)/(512*512))

