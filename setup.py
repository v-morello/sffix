import os
import setuptools
from setuptools import setup

def parse_version():
    thisdir = os.path.dirname(__file__)
    version_file = os.path.join(thisdir, 'sffix', '_version.py')
    with open(version_file, 'r') as fobj:
        text = fobj.read()
    items = {}
    exec(text, None, items)
    return items['__version__']

version = parse_version()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='sffix',
    url='https://github.com/v-morello/sffix',
    author='Vincent Morello',
    author_email='vmorello@gmail.com',
    description='Modify multi-chunk PSRFITS headers so that dspsr considers them time-contiguous',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=version,
    packages=setuptools.find_packages(),
    install_requires=['astropy'],
    license='MIT License',
)