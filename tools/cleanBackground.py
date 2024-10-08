import os
from pathlib import Path
import sys
import numpy as np
from PIL import Image
import skimage.io as io
import torch.nn.functional as F
import torch

import cv2
import matplotlib.pyplot as plt
from tqdm import *

def generate_file_list(dir, end):
    list = [os.path.join(dir,f) for f in os.listdir(dir) if f.endswith(end)]
    list.sort()
    return list

def get_file_name(path):
    return Path(path).stem

# read and process label tif image, only keep red channel and change[0, 255] to [0, 1]
def read_tif_img(file):
    return io.imread(file)

def process_tif_img(img):
    # print("tif img has unique value ", np.unique(img))
    # print(img.shape)
    if(len(img.shape)>2):
        r_img = img[:,:,0]
        r_img[r_img!=0]=255
        r_img[img[:,:,1]>0]=0
        return r_img
    else:
        img[img!=0]=255
        return img

def softmax(x):
    max = np.max(x,axis=1,keepdims=True)
    e_x = np.exp(x-max)
    sum = np.sum(e_x,axis=1,keepdims=True)
    return e_x/sum

def read_process_tif_img(file):
    return process_tif_img(read_tif_img(file))


# source_dir = "../../Training7/Result/GeneratedProb/lin1-10-train/Hybrid_BN_A/output"
# target_dir = "../../Training7/Result/GeneratedLabel/lin1-10-train"

source_dir = "backgroundv2"
target_dir = "cleanedBackground"
if not(os.path.exists(target_dir)):
    os.mkdir(target_dir)

# obtain file list
file_list = generate_file_list(source_dir, 'tif')
for f in tqdm(file_list):
    filename = get_file_name(f)
    filename_without_ext = f.split('.')[0]
    background_label = read_process_tif_img(f)
    kernel = np.ones((5,5),np.uint8)

    # for i in range(20):
    #     background_label = cv2.dilate(background_label, kernel, iterations = 1)
    #     background_label = cv2.erode(background_label, kernel, iterations = 1)
    background_label = cv2.morphologyEx(background_label,cv2.MORPH_CLOSE,kernel)
    # for i in range(5):
    background_label = cv2.morphologyEx(background_label,cv2.MORPH_OPEN,kernel)
    im = Image.fromarray(background_label)
    im.save(os.path.join(target_dir,filename+".tif"))