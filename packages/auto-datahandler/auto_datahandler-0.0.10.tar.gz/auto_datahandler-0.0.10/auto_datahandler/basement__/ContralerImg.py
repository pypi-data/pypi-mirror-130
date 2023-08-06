import os, hashlib

import cv2
import numpy as np

'''
    针对图片的基础操作
'''
class Contraler_Img:
    @staticmethod
    def get_imgHeight(img_path):
        """获取图片的高度"""
        img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), -1)
        h = img.shape[0]
        return h

    @staticmethod
    def cutting_single_img(img_path, cutBottomHeight):
        """裁切单张图片 并且覆盖原图片"""
        img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), -1)
        if (img is not None):
            h = img.shape[0]
            w = img.shape[1]
            cutHeight = h - cutBottomHeight
            cutWidth = w
            print('img_shape: ', img.shape, 'cutWidth:cutHeight ', cutWidth, ":", cutHeight)
            cropped = img[0:cutHeight, 0:cutWidth]  # 裁剪坐标为[y0:y1, x0:x1]
            try:
                # cv2.imwrite(imgSrc, cropped) #这种方式保存命名中文会乱码
                cv2.imencode('.jpg', cropped)[1].tofile(img_path)
            except:
                print("图片裁切失败： ", img_path)

    @staticmethod
    def cutting_imgs_dir(dirpath, cutBottomHeight=55):
        '''
            以指定裁切高度裁切指定目录下的所有图片
        :param dirpath 待处理的目录  路径结尾需要\\结尾
        :cutBottomHeight 指定裁切高度
        '''
        imgName_list = os.listdir(dirpath)
        for imgName in imgName_list:
            imgpath = dirpath + imgName
            Contraler_Img.cutting_single_img(img_path=imgpath, cutBottomHeight=cutBottomHeight)

    @staticmethod
    def change_imgMD5(imgSrc):
        """修改单张图片的md5"""
        with open(imgSrc, 'rb') as f:
            md5 = hashlib.md5(f.read()).hexdigest()
        file = open(imgSrc, 'rb').read()
        with open(imgSrc, 'wb') as new_file:
            new_file.write(file + bytes('\0', encoding='utf-8'))  # here we are adding a null to change the file content
            newMD5 = hashlib.md5(open(imgSrc, 'rb').read()).hexdigest()
        print("修改MD5的文件：", imgSrc,"\n旧MD5: ", md5, " \t 新MD5： ",newMD5)

    @classmethod
    def change_imgMD5_dir(cls, dirPath):
        """批量修改目录下图片的MD5"""
        imgNameList = os.listdir(dirPath)
        for imgName in imgNameList:
            imgSrc = dirPath + '\\' + imgName
            cls.changeMD5(imgSrc)



