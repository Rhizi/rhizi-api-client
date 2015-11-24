#!/usr/bin/env python
from setuptools import setup,find_packages

"""Setup script for Rhizi API Client."""

version = "0.0.1" # [major].[minor].[release]

# parse README
with open('README.md') as readme_file:
    long_description = readme_file.read()

# parse requirements
with open('requirements.txt') as f:
    required = f.read().splitlines()

# run setup
setup(
    name='Rhizi API Client',
    version=version,
    description='Rhizi - collaborative network mapping.',
    long_description =long_description,
    author='',
    author_email='clement@rhizi.com',
    url = "http://rhizi.org",
    download_url='https://github.com/rhizi/rhizi-client',
    keywords = ["network", "edition", "visualization", "rhizi"],
    packages = find_packages(exclude=['res', 'scripts', 'tests*']),
    install_requires=required,
    entry_points = {
                'console_scripts': [ 'rhizi-client=bin.import_to_rhizi:main' ]
                },
    license='BSD',
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
    ]
)
