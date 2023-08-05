# -*- coding: utf-8 -*-
"""Installer for the mcli package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
])


setup(
    name='m-cli',
    version='1.0.0b7',
    description="Mizuvo CLI",
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "License :: Other/Proprietary License",
    ],
    keywords='CLI',
    author='Mizuvo',
    author_email='info@mizuvo.com',
    url='https://pypi.python.org/pypi/m-cli',
    packages=find_packages(include=['mcli']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'requests',
        'click',
    ],
    extras_require={
        'test': [
        ],
    },
    entry_points={
        'console_scripts': ["mcli=mcli:main"],
    },
)
