# -*- coding:utf-8 -*-
# @Author  : Creat by Han
from distutils.core import setup
from setuptools import find_packages

setup(name='xhproxies',  # 包名
      version='2021.07.29',  # 版本号
      description='',
      long_description='返回代理ip',
      author='Creat by Han',
      author_email='894781617@qq.com',
      url='',
      license='',
      install_requires=[],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.5',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Topic :: Utilities'
      ],
      keywords='',
      packages=find_packages('src'),  # 必填，就是包的代码主目录
      package_dir={'': 'src'},  # 必填
      include_package_data=True,
      )

