import numpy as np
from osgeo import gdal
from spectral.io import envi
from tqdm import tqdm
import os

data_source_folder = "../HMI-original-data"


parent_folder = 'G:\\HMI\\lin1-lin10\\lin1\\'

for x in range(1, 6):
    # 构建文件名
    file_name = f'lin1-{x}\\202403-RF2'
    file_name1 = f'/lin1-{x}'
    # 构建单波段图像输入路径
    input_folder = os.path.join(parent_folder, file_name)
    # 创建一个空的高光谱数据立方体
    spectral_cube = None

    # 获取文件列表并按照波段顺序排序
    file_list = [f"{input_folder}\\{wavelength}nm_RC.tiff" for wavelength in range(420, 751, 5)]

    # 逐个读取并填充数据立方体
    for i, file_name in tqdm(enumerate(file_list)):
        image = gdal.Open(file_name)
        band = image.GetRasterBand(1)
        data = band.ReadAsArray()
        if spectral_cube is None:
            width = image.RasterXSize
            height = image.RasterYSize
            spectral_cube = np.zeros((height, width, len(file_list)), dtype=data.dtype)
        spectral_cube[:, :, i] = data

    # 保存高光谱数据立方体为一个ENVI文件
    driver = gdal.GetDriverByName("ENVI")
    output_envi_file = input_folder + file_name1
    output_ds = driver.Create(output_envi_file, width, height, len(file_list), gdal.GDT_Byte)  # 使用适当的数据类型

    # 将数据立方体写入ENVI文件
    for i in tqdm(range(len(file_list))):
        output_ds.GetRasterBand(i + 1).WriteArray(spectral_cube[:, :, i])

    # 完善头文件信息
    # 加载原始的ENVI头文件
    header_file = output_envi_file + '.hdr'
    metadata = envi.read_envi_header(header_file)

    # 添加"wavelength units"以及其值"nm"
    metadata['default bands'] = '{49, 25, 11}'
    metadata['wavelength units'] = 'nm'
    wavelengths = list(range(420, 751, 5))
    metadata['wavelength'] = wavelengths

    # 保存修改后的ENVI头文件 直接覆盖原文件
    envi.write_envi_header(header_file, metadata)