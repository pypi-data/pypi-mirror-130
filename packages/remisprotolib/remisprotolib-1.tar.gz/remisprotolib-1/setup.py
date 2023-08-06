from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='remisprotolib',
    version='1',
    packages=find_packages(),
    install_requires=[
        'grpcio==1.37.1',
        'grpcio-tools==1.37.1'
    ],
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
)
