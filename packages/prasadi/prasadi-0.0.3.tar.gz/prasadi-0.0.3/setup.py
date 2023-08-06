"""Setup.py for the Astronomer sample Airflow provider package. Built from datadog provider package for now."""

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

"""Perform the package airflow-provider-sample setup."""
setup(
    name='prasadi',
    version="0.0.3",
    description='A sample provider package built by Astronomer.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        "apache_airflow_provider": [
            "provider_info=prasadi.__init__:get_provider_info"
        ]
    },
    license='Apache License 2.0',
    packages=['prasadi', 'prasadi.hooks',
              'prasadi.sensors', 'prasadi.operators'],
    #install_requires=['apache-airflow>=2.0'],
    setup_requires=['setuptools', 'wheel'],
    author='prasadi',
    author_email='prasadi.jayakodi@novigi.com.au',
    url='http://astronomer.io/',
    python_requires='>=2.7',
)
