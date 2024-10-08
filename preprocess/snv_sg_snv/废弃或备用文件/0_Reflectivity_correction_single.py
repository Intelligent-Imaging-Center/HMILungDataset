import cv2
import numpy as np
from tqdm import tqdm
import os


parent_folder = r'G:\HMI\lin1-10\lin3'
# 定义子文件夹名称
sub_folder_name1 = '202403-RF2\\'
sub_folder_name2 = 'white\\'

no_light_background_path = 'G:\\Dark1\\dark1.tiff'

for x in range(1, 21):
    # 构建文件名
    file_name = f'lin3-{x}\\'
    # 构建单波段图像输入路径
    input_path = os.path.join(parent_folder, file_name)
    # 构建白板图像输入路径
    whiteboard_input_path = os.path.join(parent_folder, sub_folder_name2)
    # 构建反射率校正后文件输出路径
    output_path = os.path.join(input_path, sub_folder_name1)

    # 循环处理每张图像
    for i in tqdm(range(420, 751, 5)):
        # 构造文件名
        data_path = input_path + f'{i}nm.tiff'
        whiteboard_path = whiteboard_input_path + f'w{i}nm.tiff'
        output_path1 = output_path + f'{i}nm_RC.tiff'

        # 读入图像数据
        data_image = cv2.imread(data_path, cv2.IMREAD_GRAYSCALE)
        whiteboard_image = cv2.imread(whiteboard_path, cv2.IMREAD_GRAYSCALE)
        no_light_background_image = cv2.imread(no_light_background_path, cv2.IMREAD_GRAYSCALE)

        wd = whiteboard_image - no_light_background_image
        print(wd.max(), wd.min())

        # 对数据进行相应处理

        reflectance = (data_image - no_light_background_image) / (wd + 1e-3)
        bigPos = reflectance >= 2
        reflectance[bigPos] = 1.99999
        # reflectance = (reflectance-reflectance.min())/(reflectance.max()-reflectance.min())
        print(reflectance.max(), reflectance.min())
        # 保存反射率校正后的图像
        cv2.imwrite(output_path1, ((reflectance/2)*255).astype(np.uint8))


