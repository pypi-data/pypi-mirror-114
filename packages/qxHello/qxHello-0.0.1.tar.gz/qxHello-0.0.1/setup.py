# coding=utf-8
# Copyright 2021 The qx-hello Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Setup script for qx-hello.

This script will install qx-hello as a Python module.

See: https://github.com/qxresearch/qx-hello
"""
import pathlib
import os
from setuptools import find_packages
from setuptools import setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

install_requires = [
    
]

qx_hello_description = ('qxHello: A python package to print your name')

setup(
    name='qxHello',
    version='0.0.1',
    description=qx_hello_description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/qxresearch/qx-hello',
    author='xiowuc2',
    author_email="<rohitmandal814566@gmail.com>",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    keywords='qxresearch, python, pypi, hello-world',
    include_package_data=True,
    packages=find_packages(exclude=['docs']),
    package_data={'testdata': ['testdata/*.gin']},
    install_requires=install_requires,
    project_urls={  # Optional
        'Documentation': 'https://github.com/qxresearch/qx-hello/docs',
        'Bug Reports': 'https://github.com/qxresearch/qx-hello/issues',
        'Source': 'https://github.com/qxresearch/qx-hello',
    },
    license='Apache 2.0',
)

