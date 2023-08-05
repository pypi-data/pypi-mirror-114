#!/usr/bin/env python
#
# Copyright (C) 2014-2020  UAVCAN Development Team  <uavcan.org>
#
# This software is distributed under the terms of the MIT License.
#
# Author: Ben Dyer <ben_dyer@mac.com>
#         Pavel Kirienko <pavel.kirienko@zubax.com>
#

import os
import sys
from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

args = dict(
    name='uavcan',
    version='1.0.0.dev35',
    description='OBSOLETE, use pyuavcan_v0 instead',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=[],
    author='Pavel Kirienko, Ben Dyer',
    author_email='maintainers@uavcan.org',
    url='http://uavcan.org',
    license='MIT',
    keywords=''
)

if sys.version_info[0] < 3:
    args['install_requires'] = ['monotonic']

setup(**args)
