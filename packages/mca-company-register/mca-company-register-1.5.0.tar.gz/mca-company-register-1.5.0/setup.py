import os
import setuptools
from setuptools import setup
from distutils.command.register import register as register_orig
from distutils.command.upload import upload as upload_orig

setup(
    name='mca-company-register',
    version='1.5.0',
    zip_safe=False,
    description='AE ops',
    url='https://github.com/bharath-sadhu/mca-company-registry.git',
    author='bharath sadhu',
    author_email='bharath.sadhu@cloudwick.com',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7'
    ],
    keywords='Company Registry',
    packages=setuptools.find_packages(),
    include_package_data=True,
    setup_requires=['setuptools','pytest-runner'],
    install_requires=[
         'fastapi',
         'pydantic'
    ],
    entry_points={}
)