#!/usr/bin/env python
import setuptools

with open('README.md', 'rb') as r_file:
    LDINFO = r_file.read()

required = [
    "psutil",
    "argh",
    "tabulate"
]

dependency_links = [
]

setuptools.setup(
    name="pyWireMock",
    version="0.0.1.dev1",
    author="AnObfuscator",
    author_email="anobfuscator@gmail.com",
    description="An implementation of the WireMock REST API in Python.",
    long_description=LDINFO,
    packages=setuptools.find_packages(),
    url="",
    dependency_links=dependency_links,
    install_requires=required,
    classifiers=[
        'Intended Audience :: Information Technology',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    entry_points={ }
)