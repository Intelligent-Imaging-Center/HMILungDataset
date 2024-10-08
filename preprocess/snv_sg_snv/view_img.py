import os
from pathlib import Path
import sys
import imageio.v2 as iio
import numpy as np
from PIL import Image

def generate_file_list(dir, end):
    list = [os.path.join(dir,f) for f in os.listdir(dir) if f.endswith(end)]
    list.sort()
    return list

def get_file_name(path):
    return Path(path).stem

# read and process label tif image, only keep red channel and change[0, 255] to [0, 1]
def read_tif_img(file):
    print(file)
    return np.array(iio.imread(file), dtype = np.uint8)

def process_tif_img(img):
    print("source img has following value ", np.unique(img))
    if(len(img.shape)>2):
        r_img = img[:,:,0]
        r_img[r_img>=1]=1
        return r_img
    else:
        img[img>=1]=1
        return img

def read_process_tif_img(file):
    return process_tif_img(read_tif_img(file))


source_dir = "../labelPrepare/label"

# obtain file list
file_list = generate_file_list(source_dir, 'tif')

# Processing files, 2 for ill cell, 1 for not ill cell, 0 for other

for f in file_list:
    filename = get_file_name(f)
    print(filename)
    # Value 0 1 2
    label = read_process_tif_img(os.path.join(source_dir,filename+".tif"))
    print(label.shape)
    print(np.unique(label))

