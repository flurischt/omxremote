#!/usr/bin/env python

from setuptools import setup

setup(name='omxremote',
      version='0.1',
      description='remote control for a raspberry pi movie player',
      author='Flurin Rindisbacher',
      author_email='info@flurischt.ch',
      url='http://github.com/flurischt/omxremote',
      license='BSD',
      packages=['omxremote'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['Flask>=0.10.1'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Topic :: Multimedia :: Video'
      ],
      )
