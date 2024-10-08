import os
from pathlib import Path
import sys
import numpy as np
from PIL import Image
import skimage.io as io
def generate_file_list(dir, end):
    list = [os.path.join(dir,f) for f in os.listdir(dir) if f.endswith(end) or f.endswith('png')]
    list.sort()
    return list

def get_file_name(path):
    return Path(path).stem

# read and process label tif image, only keep red channel and change[0, 255] to [0, 1]
def read_tif_img(file):
    return io.imread(file)

def process_tif_img(img):
    if(len(img.shape)>2):
        r_img = img[:,:,0]
        r_img[r_img==255]=1
        return r_img
    else:
        return img
    
def read_process_tif_img(file):
    return process_tif_img(read_tif_img(file))


source_dir = "../RawData/prepare-ill-cell/cell"
target_dir = "../RawData/prepare-ill-cell/cellR"
if not(os.path.exists(target_dir)):
    os.mkdir(target_dir)

# obtain file list
file_list = generate_file_list(source_dir, 'tif')

for f in file_list:
    print(f)
    filename = get_file_name(f)
    filename_ext = f.split('/')[-1]
    source_label = read_process_tif_img(os.path.join(source_dir,filename_ext))
    print("source cell label has unique value ",np.unique(source_label))
    source_label[source_label!=0]=255
    im = Image.fromarray(source_label)
    im.save(os.path.join(target_dir,filename+".tif"))
