"""facemosaic可以对图片中的人脸添加马赛克

函数：
1.add_mosaic（
    必要参数:img 可选参数:frame pixel_width conf_threshold cuda
    img -> 通过cv2中imread函数返回的值*flags使用默认参数*
    frame -> 目前支持的参数有 'CAFFE' 
    pixel_width -> 参数要求为 整型 参数。该参数可修改一个马赛克像素的尺寸大小(单位为 像素 )
    conf_threshold -> 要求参数为不大于1不小于0的浮点数。该参数可规定识别的人脸形态阈值(建议不小于0.6)

    返回
    会返回修改后的图像，使用cv2的imwrite函数即可保存图像）

要求：
使用本模块需要以下模块/包
opencv-python

暂不支持cuda
"""

from .facemosaic import *

__title__ = 'facemosaic'
__version__ = '1.0.0'
__author__ = '刘子豪'