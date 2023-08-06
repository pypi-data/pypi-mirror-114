import setuptools
from setuptools import setup

setup(
    name='mca-company-register',
    version='1.6.0',
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