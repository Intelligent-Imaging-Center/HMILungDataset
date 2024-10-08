import os
from pathlib import Path
import sys
import numpy as np
from PIL import Image
import skimage.io as io
import tqdm

def generate_file_list(dir, end):
    list = [os.path.join(dir,f) for f in os.listdir(dir) if f.endswith(end) or f.endswith('tif')]
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


# source_dir = "D:/Training7/NoPreciseLabel/label"
# target_dir = "D:/Training7/NoPreciseLabel/label_color"
source_dir = "D:/Training7/EssayImages/workflow_input"
target_dir = "D:/Training7/EssayImages/workflow_output"
source_color = [255,0,0]
target_color = [0,0,255]
if not(os.path.exists(target_dir)):
    os.mkdir(target_dir)

# obtain file list
file_list = generate_file_list(source_dir, 'png')

for f in tqdm.tqdm(file_list):
    filename = get_file_name(f)
    source_label = read_tif_img(f)
    source_label = source_label[:,:,0:3]
    print(np.unique(source_label))
    print(np.shape(source_label))
    image = np.zeros((source_label.shape[0],source_label.shape[1],3), dtype="uint8")
    if (len(source_label.shape) == 2):
        image[np.where((source_label==255))] = target_color
    else:
        image[np.where((source_label==[255,0,0]).all(axis=2))] = [0,255,0]
        image[np.where((source_label==[0,255,0]).all(axis=2))] = [255,0,0]
        image[np.where((source_label==[0,0,255]).all(axis=2))] = [0,0,255]
        image[np.where((source_label==[255,255,255]).all(axis=2))] = [255,255,255]
    im = Image.fromarray(image)
    im.save(os.path.join(target_dir,filename+".png"))
