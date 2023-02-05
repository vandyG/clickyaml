#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'python-dotenv', 'pyyaml']

test_requirements = ['pytest>=3', ]

setup(
    author="Vandit Goel",
    author_email='vandy.goel23@gmail.com',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.7',
    ],
    description="ClickYaml reads a `.yaml` file and creates click Commands out of it.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='clickyaml',
    name='clickyaml',
    packages=find_packages(include=['clickyaml', 'clickyaml.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/vandyG/clickyaml',
    version='1.1.1',
    zip_safe=False,
)
