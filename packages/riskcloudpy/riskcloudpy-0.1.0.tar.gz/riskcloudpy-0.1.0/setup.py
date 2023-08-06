from setuptools import find_packages, setup

from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='riskcloudpy',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(include=['riskcloudpy']),
    version='0.1.0',
    description='A Python SDK for the Risk Cloud',
    author='LogicGate',
    license='MIT',
    install_requires=["requests"],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
