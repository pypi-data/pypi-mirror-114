import moyan
import os
import shutil
import random
import cv2
import numpy as np 
from PIL import Image
import matplotlib.pyplot as plt

img_dir = r"D:\code\PAI\docUnet.pytorch\docUnet.pytorch-master\image_generate_crop"
output_dir = r"C:\Users\Moyan\Desktop\tabel_mask"


img_list = moyan.walkDir2RealPathList(img_dir, filter_postfix=[".png"])
# random.shuffle(img_list)
for idx, path in enumerate(img_list):
    # print(idx, path)
    md5_name = moyan.get_file_md5(path)
    print(idx, md5_name)
    new_path = os.path.join(output_dir, md5_name+".png")
    shutil.copyfile(path, new_path)


# img_dir = r"C:\Users\Moyan\Desktop\img"
# output_dir = r"C:\Users\Moyan\Desktop\img"
# img_list = moyan.walkDir2RealPathList(img_dir, filter_postfix=[".bmp"])
# for idx, path in enumerate(img_list):
#     print(idx, path)
#     im = moyan.cv_read(path, 0)
#     im = cv2.resize(im, (600, 800))
#     new_path = os.path.splitext(path)[0] + ".jpg"
#     cv2.imwrite(new_path, im)

    # exit()

# img_dir = r"D:\Dataset\TableBank_data\Detection_data\cropbox\select_useful2\img"
# out_dir = r"D:\Dataset\TableBank_data\Detection_data\cropbox\select_useful2\padding_img"

# img_list = os.listdir(img_dir)

# def resize_img_keep_ratio(img_name,target_size):
#     img = cv2.imread(img_name)
#     old_size= img.shape[0:2]
#     #ratio = min(float(target_size)/(old_size))
#     ratio = min(float(target_size[i])/(old_size[i]) for i in range(len(old_size)))
#     new_size = tuple([int(i*ratio) for i in old_size])
#     img = cv2.resize(img,(new_size[1], new_size[0]))
#     pad_w = target_size[1] - new_size[1]
#     pad_h = target_size[0] - new_size[0]
#     top,bottom = pad_h//2, pad_h-(pad_h//2)
#     left,right = pad_w//2, pad_w -(pad_w//2)
#     img_new = cv2.copyMakeBorder(img,top,bottom,left,right,cv2.BORDER_CONSTANT,None,(255, 255, 255))
#     return img_new

# def resize_img_keep_ratio2(img_name,target_size):
#     img = cv2.imread(img_name)
#     old_size= img.shape[0:2]
#     #ratio = min(float(target_size)/(old_size))
    
#     ratio = min(float(target_size[i])/(old_size[i]) for i in range(len(old_size)))
#     new_size = tuple([int(i*ratio) for i in old_size])
#     img = cv2.resize(img,(new_size[1], new_size[0]))
#     pad_w = target_size[1] - new_size[1]
#     pad_h = target_size[0] - new_size[0]
#     top,bottom = pad_h//2, pad_h-(pad_h//2)
#     left,right = pad_w//2, pad_w -(pad_w//2)
#     img_new = cv2.copyMakeBorder(img,top,bottom,left,right,cv2.BORDER_CONSTANT,None,(255, 255, 255))
#     return img_new

# for idx, names in enumerate(img_list):
#     print(idx, names)
#     img_path = os.path.join(img_dir, names)
#     out_path = os.path.join(out_dir, names)
#     # im = cv2.imread(img_path, 0)
#     new_im = resize_img_keep_ratio(img_path, (800, 600))
#     cv2.imwrite(out_path, new_im)
#     # exit()



# npy_path = r"D:\code\PAI\docUnet.pytorch\docUnet.pytorch\img\padding_mask_aug\%5BMS-OXCFXICS%5D-080425_33#84_72_527_479_0.jpg.npy"
# label = np.load(npy_path)

# # print(label[:, :, 0]

# for i in range(100): 
#     print("第110行第{}个: ({}, {})".format(i, label[10][i][0], label[10][i][1]))