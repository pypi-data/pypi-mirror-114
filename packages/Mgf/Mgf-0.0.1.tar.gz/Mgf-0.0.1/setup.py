# -*- coding:utf-8 -*-
try:
    from setuptools import setup, find_packages
except:
    from distutils.core import setup
from codecs import open
from os import path

#版本号
VERSION = '0.0.1'

#发布作者
AUTHOR = "123_python"

#邮箱
AUTHOR_EMAIL = "QQsped2020@Tom.com"

#项目网址
URL = "https://code.xueersi.com/space/47013434"

#项目名称
NAME = "Mgf"

#项目简介
DESCRIPTION = "Heh!"

#LONG_DESCRIPTION为项目详细介绍，这里取README.md作为介绍
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.txt'), encoding='ISO-8859-1') as f:
    LONG_DESCRIPTION = f.read()

#搜索关键词
KEYWORDS = ["Deep Learning", "Machine Learning", "Neural Networks", "Scientific computing", "Differential equations", "PDE solver"]

#发布LICENSE
LICENSE = "MIT"

#包
PACKAGES = ["Mgf"]

#具体的设置
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',

    ],
    #指定控制台命令
    entry_points={
        'console_scripts': [
            'PDESolver = PDESolverByDeepLearning:PDESolver',
        ],
    },
    keywords=KEYWORDS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    packages=PACKAGES,
    include_package_data=True,
    zip_safe=True,
)
