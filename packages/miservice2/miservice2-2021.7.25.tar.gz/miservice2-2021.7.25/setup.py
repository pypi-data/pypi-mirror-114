#!/usr/bin/env python3

import os
import sys

if len(sys.argv) == 1:
    os.system('%s sdist' % sys.argv[0])
    os.system('twine upload dist/*')
    os.system('rm -rf dist *.egg-info')
    exit(0)


import time
from pathlib import Path
from setuptools import setup

setup(
    name='miservice2',
    description='XiaoMi Cloud Service',
    version=time.strftime("%Y.%m.%d"),
    license='MIT',
    author='Yonsm',
    author_email='Yonsm@qq.com',
    url='https://github.com/Yonsm/MiService',
    long_description=Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    packages=['miservice2'],
    scripts=['micli.py'],
    python_requires='>=3.7',
    install_requires=['aiohttp'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
