# HMILungDataset
This dataset contains a hyperspectral microscopic imaging (HMI) dataset for lung tumor (LUSC). The dataset contains 67 images from 10 patients. 
This repo contain codes used during processing the dataset. The original and processed dataset can be found in Baidu Cloud Disk as follows:
Link: https://pan.baidu.com/s/14JbmjPXcUH5gqFa5K0Qixg?pwd=yreu 
Password: yreu 

# Folder Structure
In the cloud disk:

RawData - Contain the original HMI images taken from hyperspectral camera and tumor labels provided by pathogists.
ProcessedData - Contain HMI datacube (with SNV and SG) and labels with 4 types(background, non-cell, tumor cell and non-tumor cell).


In this Repo:

KMeanClassifications: Used to analyze and separate pixels in HMI datacubes into K types (default = 20).
QtLabelCreator: Qt codes and interface for manually select interested regions (e.g. background and cell) from K types.
preprocess - Make some preprocess steps to the original HMI images and create HMI datacube. Three options are provided (sg = Savitzky Golay Filter, snv = standard normal variation, x = do nothing). 
tools - frequently used tools such as overlapping different types into one image, change image size etc.

# Contact
Corresponding Author 

Yunfeng Nie Yunfeng.Nie@vub.be
Jingang Zhang zhangjg@ucas.ac.cn   

Authors

Zhiliang Yan yz97liang@stu.xidian.edu.cn
Haosong Huang hhuang2@stu.xidian.edu.cn
