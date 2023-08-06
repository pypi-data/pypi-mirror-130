import os, shutil

"""
    文件及目录处理相关的基类和方法
"""
# 目录处理类
class Contraler_Dir:
    # 获取当前根目录路径
    @staticmethod
    def getCurOriPath():
        return os.path.abspath(os.path.dirname(__file__))

    # 判断目录是否存在，不存在则创建
    @staticmethod
    def checkACreateDir(dirPath):
        exist = os.path.exists(dirPath)
        if (not exist):
            os.makedirs(dirPath)
        else:
            pass
        pass

    # 清空指定目录下所有文件
    @staticmethod
    def clearDirFiles(dirPath):
        lis = os.listdir(dirPath)
        for i in lis:
            os.remove(dirPath + i)

    @staticmethod
    def copyFile(src, dst):
        '''
            复制文件
        '''
        shutil.copyfile(src, dst)

    @staticmethod
    def renameFile(imgSrc, imgDst):
        """图片重命名"""
        os.rename(imgSrc, imgDst)
