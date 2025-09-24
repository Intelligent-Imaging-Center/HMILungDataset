# HMILungDataset
This dataset contains a hyperspectral microscopic imaging (HMI) dataset for lung tumors (LUSC). The dataset contains multiple image scenes extracted from pathology slides of 10 patients diagnosed with LUSC. 
**This repository hosts the example data used in the paper. For access to more data, please contact the corresponding author.**

# Folder Structure
In the example data (LUSC-3-8.zip):

RawData - Contains the original HMI images taken from the HMI system and tumor labels provided by pathologists.

ProcessedData - Contains HMI datacube (with SNV and SG) and labels with 4 types(background, non-cell, tumor cell, and non-tumor cell).


In this Repo:

KMeanClassifications: Used to analyze and separate pixels in HMI datacubes into K types (default = 20).

QtLabelCreator: Qt codes and interface for manually selecting interested regions (e.g., background and cell) from K types.

preprocess - Make some preprocessing steps to the original HMI images and create an HMI datacube. Three options are provided (sg = Savitzky-Golay Filter, snv = standard normal variation, x = do nothing). 

tools - frequently used tools such as overlapping different types into one image, changing image size, etc.

# Contact
Corresponding Author 

Yunfeng Nie Yunfeng.Nie@vub.be

Jingang Zhang zhangjg@ucas.ac.cn   

Authors

Zhiliang Yan yz97liang@stu.xidian.edu.cn

Haosong Huang hhuang2@stu.xidian.edu.cn

