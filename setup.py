# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup

version = '0.1.0'
description = 'Bird Feeder provides input data for the Birds.'
long_description = (
    open('README.rst').read() + '\n' +
    open('AUTHORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

requires = [
    'pysolr',
    'nose',
    ]

classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        ]

setup(name='birdfeeder',
      version=version,
      description=description,
      long_description=long_description,
      classifiers=classifiers,
      keywords='thredds solr python netcdf birdhouse anaconda',
      author='Birdhouse Developers',
      url='https://github.com/bird-house/bird-feeder',
      license = "Apache License v2.0",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      install_requires=requires,
      entry_points = {
          'console_scripts': [
              'birdfeeder=birdfeeder:main',
              ]}     
      ,
      )
