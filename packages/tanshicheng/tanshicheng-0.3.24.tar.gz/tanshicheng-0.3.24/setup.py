# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

LONGDOC = """
作者:
    tanshicheng
包括:
    用于读取参数文件
    文件、xml、正则的一般处理/读写
    时间/过程处理
日志:
    2018年09月11日: 增加过程时间输出(ProgressAndTime)
    2018年09月13日: 增加pickle读写(FileProcess)等
    2018年09月14日: 增加简化的时间输出(ProgressAndTime.ProgressOut2)等
    2018-11-17：仿照 tqdm 增加 ProgressOut3，可以在循环中控制头部输出
"""

setup(
    name='tanshicheng',
    version='0.3.24',
    description="tanshicheng's tools",
    long_description=LONGDOC,
    author='tanshicheng',
    license='GPLv3',
    url='https://github.com/aitsc',
    keywords='tools',
    packages=find_packages(),

    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'matplotlib>=3.1.3,<=3.2.3',
        'numpy>=1.18.1',
        'scipy>=1.4.1',
        'requests>=2.22.0',
        'tinydb>=4.4.0',
        'Flask>=1.1.1',
        'pymongo>=3.11',
        'tsc-auto>=0.7.2',
    ],
    python_requires='>=3.6',
)
