from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

"""Perform the package Novigi_Operators setup."""
setup(
    name='test_lasa',
    version="1.1",
    description='Novigi Custom Airflow Operators',
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        "apache_airflow_provider": [
            "provider_info = novigi_operators.__init__:get_provider_info"
        ]
    },
    license='Apache License 2.0',
    packages= ['test_lasa'] , 
    install_requires=[
                      'requests',
                      'jsonpath_ng',
                      'pandas'
                      ],
    author='Novigi',
    author_email='prasadi19943@gmail.com',
    url='https://Prasadi1994@bitbucket.org/novigi/novigi_operators.git',
    python_requires='>=3.0',
)