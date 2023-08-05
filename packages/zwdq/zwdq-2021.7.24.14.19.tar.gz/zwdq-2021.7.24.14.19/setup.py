# -*- coding: utf-8 -*- 
import json
import sys
import getopt
from setuptools import setup
import time
import datetime
now = datetime.datetime.now()

version = str(now)
version = version.replace("-",".").replace(":",".").replace(" ",".")[0:16]


setup(
    name='zwdq',# 需要打包的名字,即本模块要发布的名字
    version = version ,# 版本
    description='个人接口', # 简要描述
    py_modules=['zwdq'],   # 需要打包的模块
    packages=['zwdq'],
    package_dir={'zwdq': 'src/zwdq'},
    author='zwdq', # 作者名
    author_email='zhuwudaoqin@gmail.com',   # 作者邮件
    requires=['numpy', 'pandas'], # 依赖包,如果没有,可以不要
)
