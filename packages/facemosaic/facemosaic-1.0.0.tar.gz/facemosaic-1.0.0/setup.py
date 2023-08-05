from setuptools import setup, find_packages

setup(
    name='facemosaic',
    version='1.0.0',
    packages=find_packages(),
    description='自动识别图片中人脸并加上马赛克',
    author='刘子豪',
    author_email='2740994541@qq.com',
    install_requires=['opencv-python'],
    python_requires='>=3',
    package_data = {'': ['model/Caffe/deploy.prototxt', 'model/Caffe/res10_300x300_ssd_iter_140000_fp16.caffemodel']},
)