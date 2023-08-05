#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages

import weather_in

from os import path
this_directory = path.abspath(path.dirname(__file__)) 
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='weather_in',
    version=weather_in.__version__,
    packages=find_packages(where='weather_in'),
    python_requires='>=3.0',
    author='Travis Pawlikowski',
    author_email='tnp123@protonmail.com',
    description='OpenWeather CLI script',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url = 'https://github.com/fleetyeets/weather.in',
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/fleetyeets/weather.in/issues',
        'Source': 'https://github.com/fleetyeets/weather.in',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent'
    ],
    scripts = ['weather_in/weather_in.py']
)