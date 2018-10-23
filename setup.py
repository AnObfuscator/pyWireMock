#!/usr/bin/env python
import setuptools

with open('README.md', 'rb') as r_file:
    LDINFO = r_file.read()

required = [
    "requests"
]

setuptools.setup(
    name="pywiremock",
    version="2.11.0-4",
    author="AnObfuscator",
    author_email="anobfuscator@gmail.com",
    description="An implementation of the WireMock REST API in Python.",
    long_description=LDINFO,
    packages=setuptools.find_packages(),
    url="https://github.com/AnObfuscator/pyWireMock",
    install_requires=required,
    classifiers=[
        'Intended Audience :: Information Technology',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules']
)