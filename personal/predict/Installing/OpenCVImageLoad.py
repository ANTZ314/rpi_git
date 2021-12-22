"""
Got from:
https://www.udemy.com/deeplearning/learn/v4/questions/2515064
"""
import cv2
import numpy as np
import os
from tqdm import tqdm
from keras import utils
 
 
def get_images(path, img_shape=(128, 128)):
 
 main_path = path
 y = np.ones((1, 1))
 
 list = sorted(os.listdir(main_path))
 
 for folder in list:
 
 label = int(folder)
 n_channels = 1 # Number of channels in your image
 img_shape_stack = (1, img_shape[0], img_shape[1], n_channels)
 image_collection = np.zeros(img_shape_stack)
 
 sub_list = sorted(os.listdir(os.path.join(main_path,folder)))
 
 for i in tqdm(range(0, len(sub_list))):
 l = 0
 read_image = cv2.imread(sub_list[i], cv2.IMREAD_GRAYSCALE) # Change IMREAD_GRAYSCALE to IMREAD_* according to what your images are
 image_resized = cv2.resize(read_image, img_shape, interpolation=cv2.INTER_CUBIC)
 
 image = np.float32(image_resized)
 image = cv2.normalize(image, image, alpha=-1, beta=1, norm_type=cv2.NORM_MINMAX) #Change alpha, beta according to the preprocessing you desire
 image = np.reshape(image, img_shape_stack)
 
 image_collection = np.vstack((image_collection, image))
 y = np.vstack((y,label))
 
 
 
 y = utils.to_categorical(y,num_classes=len(list))
 
 return image_collection[1:], y[1:]
 
  
# Path to your directory where images are:
# Images belonging to each class must be separated in different folders named their class label value
# FOR EXAMPLE, THE IMAGE_SUPER_DIRECTORY WILL CONTAIN FOLDERS LIKE 1,2,3,4 for 4 classes
 
path = "/usr/local/data/sejacob/ANOMALY/data/image_super_directory"
image_collection,y = get_images(path,img_shape=(128,128))
