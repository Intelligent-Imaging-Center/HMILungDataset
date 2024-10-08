import os
from pathlib import Path
import sys
import imageio.v2 as iio
import numpy as np
from PIL import Image
import spectral as spy
import scipy.signal

def generate_file_list(dir, end):
    list = [os.path.join(dir,f) for f in os.listdir(dir) if f.endswith(end)]
    list.sort()
    return list

def get_file_name(path):
    return Path(path).stem


input_dir = "D:/DataSource/datacube-470-700/x-sg-snv"
output_dir =  "D:/BetterLabel/lin1-10/inputImages"
# obtain file list
file_list = generate_file_list(input_dir, 'hdr')

if not(os.path.exists(output_dir)):
    os.mkdir(output_dir)

# Processing files, 2 for ill cell, 1 for not ill cell, 0 for other

for f in file_list:
    filename = get_file_name(f)
    print(f)
    hsi_data = spy.open_image(f).load()
    # hsi_data = percent_linear(hsi_data)
    rgb_data = np.ascontiguousarray(hsi_data[:,:,[41,17,3]])
    rgb_data = rgb_data.astype(np.uint8)
    im = Image.fromarray(rgb_data)
    im.save(output_dir+"/"+filename + ".png")

