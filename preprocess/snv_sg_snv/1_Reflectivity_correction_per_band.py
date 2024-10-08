import cv2
import numpy as np
from tqdm import tqdm
import os
from spectral.io import envi
from osgeo import gdal
from scipy.signal import savgol_filter

# ------------------------------------------------帮助函数---------------------------------------------------
# https://zhuanlan.zhihu.com/p/620247699#:~:text=%E7%94%A8Python%E5%AE%9E%E7%8E%B0ENVI%E4%B8%AD%E7%9A%84%E2%80%9C%E4%BC%98%E5%8C%96%E7%9A%84%E7%BA%BF%E6%80%A7%E6%8B%89%E4%BC%B8%E2%80%9D%201%201%20%E7%BA%BF%E6%80%A7%E6%8B%89%E4%BC%B8%20%E9%BB%98%E8%AE%A4%E6%8B%89%E4%BC%B8%E5%88%B00-255%E8%BF%99%E4%B8%AA%E8%8C%83%E5%9B%B4%E5%86%85%EF%BC%8C%E4%B8%8B%E5%90%8C%E3%80%82%20def%20linear%28arr%29%3A%20arr_min%2C,3%20%E4%BC%98%E5%8C%96%E7%9A%84%E7%BA%BF%E6%80%A7%E6%8B%89%E4%BC%B8%20%E4%BC%98%E5%8C%96%E7%9A%84%E7%BA%BF%E6%80%A7%E6%8B%89%E4%BC%B8%E7%B1%BB%E4%BC%BC%E4%BA%8E%E7%BA%BF%E6%80%A7%E6%8B%89%E4%BC%B8%EF%BC%8C%E4%BD%86%E6%8F%90%E4%BE%9B%E4%BA%86%E6%9B%B4%E5%A4%9A%E8%AE%BE%E7%BD%AE%E6%9D%A5%E6%8E%A7%E5%88%B6%E5%9B%BE%E5%83%8F%E4%B8%AD%E7%9A%84%E4%B8%AD%E9%97%B4%E8%B0%83%E3%80%81%E9%98%B4%E5%BD%B1%E5%92%8C%E9%AB%98%E5%85%89%E3%80%82%20%E5%AE%83%E6%A0%B9%E6%8D%AE%E5%9B%9B%E4%B8%AA%E5%80%BC%E8%AE%A1%E7%AE%97%E6%8B%89%E4%BC%B8%E6%9C%80%E5%B0%8F%E5%80%BC%E5%92%8C%E6%9C%80%E5%A4%A7%E5%80%BC%EF%BC%9A%20%E6%9C%80%E5%B0%8F%E7%99%BE%E5%88%86%E6%AF%94%20%EF%BC%9A%E9%BB%98%E8%AE%A4%E5%80%BC%E4%B8%BA%200.025%E3%80%82%20
def optimized_linear(arr):
    a, b = np.percentile(arr, (2.5, 99))
    c = a - 0.1 * (b - a)
    d = b + 0.5 * (b - a)
    arr = (arr - c) / (d - c) * 255
    arr = np.clip(arr, 0, 255)
    return np.uint8(arr)

def percent_linear(arr, percent=2):
    arr_min, arr_max = np.percentile(arr, (percent, 100-percent))
    arr = (arr - arr_min) / (arr_max - arr_min) * 255
    arr = np.clip(arr, 0, 255)
    return np.uint8(arr)

def percent_linear_float(arr,percent=2):
    arr_min, arr_max = np.percentile(arr, (percent, 100-percent))
    arr = (arr - arr_min) / (arr_max - arr_min)
    return arr
    
# https://nirpyresearch.com/two-scatter-correction-techniques-nir-spectroscopy-python/
# Assume h x w x band shape
def snv(input_data):
    # Define a new array and populate it with the corrected data  
    output_data = np.zeros_like(input_data)
    output_data= (input_data - np.mean(input_data)) / np.std(input_data)
    return output_data

# -------------------------------------------------参数设置---------------------------------------
# 定义父文件夹路径
# the folder structure should be 
# - data_source_folder
# -- lin1
# --- lin1-1
# --- lin1-2
# --- white

# -- lin2
# --- lin2-1
# --- lin2-2
data_source_folder = "D:/DataSource/HMI-original-data-lin124"
parent_folders = os.listdir(data_source_folder)
parent_folders = [os.path.join(data_source_folder, subfolder) for subfolder in parent_folders]
print("Folder names are following:")
print(parent_folders)

# 定义暗背景图片，输出文件夹
output_datacube_folder = 'D:/Training4/DataSource/data/snv-sg-snv'
no_light_background_path = 'D:/Training-lin1/dark1.tiff'

band_min = 440
band_max = 750
step = 5
total_band = (band_max-band_min) // step + 1

red = 660
green = 540
blue = 470

red_band = (red-band_min)//step + 1
green_band = (green - band_min)//step+1
blue_band = (blue - band_min)//step+1

red_band_string = str(red_band)
green_band_string = str(green_band)
blue_band_string = str(blue_band)

# 创建输出文件夹
if not(os.path.exists(output_datacube_folder)):
    os.mkdir(output_datacube_folder)
    
# ----------------------------------------------主程序-------------------------------------------
# 检测输入文件夹是否正确，开始运行反射率矫正与HDR合并
if int(input("Click 1 to continue, other to exit\n")) == 1:
    no_light_background_image = cv2.imread(no_light_background_path, cv2.IMREAD_GRAYSCALE)
    # 遍历每个病理切片文件夹，对每个被选出的区域进行运算
    # slide_folder: lin1
    for slide_folder in parent_folders:
        # 构建白板图像输入路径
        # whiteboard path lin1/white
        whiteboard_input_path = os.path.join(slide_folder,"white")
        # 生成区域文件夹列表
        area_folders = os.listdir(slide_folder)
        area_folders.remove("white")
        area_folders = [os.path.join(slide_folder, subfolder) for subfolder in area_folders]

        # area_folder: lin1-1
        for area_folder in area_folders:
            spectral_cube = None
            spectral_cube_built = False
            output_ds = None
            driver = gdal.GetDriverByName("ENVI")
            # 对每个区域，读取各波段图片，进行反射率矫正，投射至【0，2】空间，转至【0，255】空间
            input_path = area_folder
            print("input path is ", input_path)
            # area_name = input_path.split("/")[-1]
            area_name = os.path.basename(input_path)
            output_envi_file = output_datacube_folder + "/" + area_name
            # 循环处理每张图像
            for i in range(band_min, band_max, step):
                # 构造文件名
                data_path = input_path + f'/{i}nm.tiff'
                whiteboard_path = whiteboard_input_path + f'/w{i}nm.tiff'
                # 读入图像数据
                data_image = cv2.imread(data_path, cv2.IMREAD_GRAYSCALE)
                whiteboard_image = cv2.imread(whiteboard_path, cv2.IMREAD_GRAYSCALE)
                wd = whiteboard_image - no_light_background_image
                # 对数据进行相应处理
                reflectance = (data_image - no_light_background_image) / (wd + 1e-3)
                # print("band ", i , " max is ", np.max(reflectance), " min is ", np.min(reflectance))
                if(spectral_cube_built == False):
                    spectral_cube_built = True
                    height, width = reflectance.shape
                    spectral_cube = np.zeros((height, width, total_band), dtype=np.float64)
                     # 保存高光谱数据立方体为一个ENVI文件
                    output_ds = driver.Create(output_envi_file, width, height, total_band, gdal.GDT_Byte)  # 使用适当的数据类型
                reflectance = percent_linear_float(reflectance)
                spectral_cube[:, :, (i-band_min)//5] = reflectance
            # print("Reflectance max is ", np.max(spectral_cube), " min is ", np.min(spectral_cube))
            for i in range(0,total_band):
                spectral_cube[:,:,i] = snv(spectral_cube[:,:,i])
            
            # 对数据立方体进行SG操作，之后进行snv,最后拉伸至【0，255】
            spectral_cube =  savgol_filter(spectral_cube, 11, 2, axis=2)
            # print("SG max is ", np.max(spectral_cube), " min is ", np.min(spectral_cube))

            # print("SNV max is ", np.max(spectral_cube), " min is ", np.min(spectral_cube))
            for i in range(0,total_band):
                # spectral_cube[:,:,i] = optimized_linear(spectral_cube[:,:,i])
                spectral_cube[:,:,i] = percent_linear(spectral_cube[:,:,i])
            # print("normalized max is ", np.max(spectral_cube), " min is ", np.min(spectral_cube))
            
            # 将数据立方体写入ENVI文件
            for i in range(0,total_band):
                output_ds.GetRasterBand(i + 1).WriteArray(spectral_cube[:, :, i])

            # 完善头文件信息
            # 加载原始的ENVI头文件
            header_file = output_envi_file + '.hdr'
            metadata = envi.read_envi_header(header_file)

            # 添加"wavelength units"以及其值"nm"
            metadata['default bands'] = '{'+red_band_string+', ' +green_band_string +', '+blue_band_string+'}'
            metadata['wavelength units'] = 'nm'
            wavelengths = list(range(band_min, band_max+1, step))
            metadata['wavelength'] = wavelengths

            # 保存修改后的ENVI头文件 直接覆盖原文件
            envi.write_envi_header(header_file, metadata)




