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
    print("tif img has unique value ", np.unique(img))
    if(len(img.shape)>2):
        r_img = img[:,:,0]
        r_img[r_img!=0]=1
        r_img[img[:,:,1]>0]=0
        return r_img
    else:
        img[img>=50]=1
        return img

def read_process_tif_img(file):
    return process_tif_img(read_tif_img(file))


input_label_dir = "inputLabel"
background_label_dir = "background"
target_dir = "outputLabel"
# obtain file list
file_list = generate_file_list(background_label_dir, 'tif')
print(file_list)
# make sure number of files to be processed is correct
modifiableNum = 0
for f in file_list:
    filename = get_file_name(f)
    if os.path.exists(os.path.join(input_label_dir,filename+".tif")):
        modifiableNum += 1

if not(os.path.exists(target_dir)):
    os.mkdir(target_dir)

# Processing files, 2 for ill cell, 1 for not ill cell, 0 for other, 3 for background
if int(input("Number of files pair to be overlapped is " + str(modifiableNum) + " if correct enter 1\n")) == 1:
    for f in file_list:
        filename = get_file_name(f)
        print(filename)
        # Value 0 1 2
        background_label = read_process_tif_img(os.path.join(background_label_dir,filename+".tif"))
        print(os.path.join(input_label_dir,filename+".tif"))
        input_label = read_process_tif_img(os.path.join(input_label_dir,filename+".tif"))
        # input_label = np.load(os.path.join(input_label_dir,filename+".npy"))
        print("background shapee ", background_label.shape)
        print("input shape ", input_label.shape)
        print("background value", np.unique(background_label))
        print("input value", np.unique(input_label))
        output_label = np.where(background_label == 1, 3, input_label)
        output_label = output_label.astype(np.uint8)
        print("File " + filename + " has processed unique value " + str(np.unique(output_label)))
        # Graphical, channel overlap
        graph_ill_cell_label =  np.zeros((input_label.shape[0],input_label.shape[1],3), dtype=np.uint8)
        graph_ill_cell_label[:,:,0] = np.where(output_label==1,255,0)
        graph_ill_cell_label[:,:,1] = np.where(output_label==2,255,0)
        graph_ill_cell_label[:,:,2] = np.where(output_label==3,255,0)
        im = Image.fromarray(output_label)
        im.save(target_dir+"/"+filename + ".tif")
        graphim = Image.fromarray(graph_ill_cell_label)
        graphim.save(target_dir+"/"+filename + ".png")
