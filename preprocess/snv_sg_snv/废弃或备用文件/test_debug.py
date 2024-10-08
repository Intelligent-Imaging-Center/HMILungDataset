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
    return np.array(iio.imread(file), dtype = np.uint8)

def process_tif_img(img):
    if(len(img.shape)>2):
        r_img = img[:,:,0]
        r_img[r_img==255]=1
        return r_img
    else:
        return img

def read_process_tif_img(file):
    return process_tif_img(read_tif_img(file))


prediction = np.load("../HybridSNv2/prediction_red.npy")
graph_ill_cell_label =  np.zeros((prediction.shape[0],prediction.shape[1],3), dtype=np.uint8)
graph_ill_cell_label[:,:,0] = np.where(prediction==1,255,0)
graph_ill_cell_label[:,:,1] = np.where(prediction==2,255,0)
graphim = Image.fromarray(graph_ill_cell_label)
graphim.save("../Prediction/6-1/output.png")