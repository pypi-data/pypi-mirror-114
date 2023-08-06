# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="power-digit-addition",
    version="0.1.0",
    description="Addition of digit of power(base_number, exponent_number)",
    long_description="""
    A library is intended to perform the following activities on input received from a user specifically a base numebr & exponent number : 
    1. calculate the result for base & exponent number, 
    2. perform the addition of all digits of a result generated in step 1
    Note : addition of digits will be performed recursively until program reaches to single digit result.
    """,
    long_description_content_type="text/markdown",
    url="https://power-digit-addition.readthedocs.io/",
    author="Govardhan Veer, Vijay Shinde",
    author_email="vijayshinde993@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["power_digit_addition"],
    include_package_data=True
)