from setuptools import find_packages
from setuptools import setup

setup(
    name='appleproj_interfaces',
    version='0.0.0',
    packages=find_packages(
        include=('appleproj_interfaces', 'appleproj_interfaces.*')),
)
