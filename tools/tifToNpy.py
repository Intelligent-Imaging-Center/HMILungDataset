import os
from pathlib import Path
import sys
import numpy as np
from PIL import Image
import skimage.io as io
import tqdm 
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
    if(len(img.shape)>2):
        r_img = img[:,:,0]
        r_img[r_img==255]=1
        return r_img
    else:
        return img

def read_process_tif_img(file):
    return process_tif_img(read_tif_img(file))

source_dir = "D:/Training7/GeneratedLabel/direct"
target_dir = "D:/Training7/final/twoTypes/prediction_hybrid"
# source_dir = "D:/Training7/label"
# target_dir = "D:/Training7/GeneratedLabel/1-8/comparison/label"
# target_dir = source_dir
if not(os.path.exists(target_dir)):
    os.mkdir(target_dir)

# obtain file list
file_list = generate_file_list(source_dir, 'tif')
for f in tqdm.tqdm(file_list):
    filename = get_file_name(f)
    filename_without_ext = f.split('.')[0]
    png_img = io.imread(f)
    if(len(png_img.shape)>2):
        output = np.zeros((png_img.shape[0],png_img.shape[1]),dtype=np.uint8)
        output += 5
        output = np.where(np.all(png_img==[0,0,0],axis=2), 0, output)
        output = np.where(np.all(png_img==[255,0,0],axis=2), 1, output)
        output = np.where(np.all(png_img==[0,255,0],axis=2), 2, output)
        output = np.where(np.all(png_img==[0,0,255],axis=2), 3, output)
        output = np.where(np.all(png_img==[255,255,255],axis=2), 1, output)
        assert 5 not in np.unique(output)
        assert 1 in np.unique(output)
    else:
        output=png_img
        output[output==255]=1
    np.save(os.path.join(target_dir,filename+".npy"), output)
    print(np.unique(output))
    # output[png_img[:,:]==[0,0,0]] = [0,0,0]
    # output[png_img[:,:]==[255,0,0]] = 1
    # output[png_img[:,:]==[0,255,0]] = 2
    # output[png_img[:,:]==[0,0,255]] = 3
    # im = Image.fromarray(output_tif)
    # im.save(os.path.join(target_dir,filename+".tif"))
    print(f, " Done")
