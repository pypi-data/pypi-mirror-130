from setuptools import setup, find_packages
import os
thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_requires = [] # Here we'll get: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()
setup(
    name='cenzopapa-sdk',
    version='1.0.0',
    author='Adrian \'Qwizi\' Ciołek',
    author_email='ciolek.adrian@protonmail.com',
    url='https://github.com/Qwizi/cenzopapa-sdk',
    packages=find_packages(include=['cenzopapa', 'cenzopapa.*']),
    install_requires=install_requires

)