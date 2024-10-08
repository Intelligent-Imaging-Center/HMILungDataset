
import os
from pathlib import Path
import sys

def generate_file_list(dir, end):
    list = [os.path.join(dir,f) for f in os.listdir(dir) if f.endswith(end)]
    list.sort()
    return list

def get_file_name(path):
    return Path(path).stem

dir = "./source"
data = "./data-xian-bad"
label = "./label-xian-bad"
target_data = "./data-xian-48"
target_label = "./label-xian-48"
startN = int(sys.argv[1])

# # remove chinese chhhhharacter before
# for f in os.listdir(data): 
#     if f.endswith('hdr') or f.endswith('dat'):
#         os.rename(os.path.join(data,f),os.path.join(data,f[5:]))

# obtain file list
file_list = generate_file_list(data, 'hdr')
for f in file_list:
    filename = get_file_name(f)
    os.rename(os.path.join(data,filename+".hdr"), os.path.join(target_data,str(startN)+".hdr"))
    os.rename(os.path.join(data,filename+".dat"), os.path.join(target_data,str(startN)+".dat"))
    os.rename(os.path.join(label,filename+".tif"), os.path.join(target_label,str(startN)+".tif"))
    startN += 1
