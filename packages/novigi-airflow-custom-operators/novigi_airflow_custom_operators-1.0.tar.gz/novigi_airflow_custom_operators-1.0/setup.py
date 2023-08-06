

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='novigi_airflow_custom_operators',
    version="1.0",
    description='Novigi Custom Airflow Operators',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT', 
    packages=find_packages(exclude=['tests']),
    install_requires=['requests','jsonpath_ng','pandas'],
    setup_requires=['setuptools', 'wheel'],
    author='Novigi',
    author_email='prasadi.jayakodi@novigi.com.au',
)
