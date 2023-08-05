import os
from setuptools import setup



def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="lowdash",
    version="1.0.0",
    author="Abh80",
    description="A python implementation of lodash in javascript",
    license="MIT",
    url="https://github.com/abh80/lowdash",
    keywords="lodash python lowdash",
    long_description=read('README.md'),
)
