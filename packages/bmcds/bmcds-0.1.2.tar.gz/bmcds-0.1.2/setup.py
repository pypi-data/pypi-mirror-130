#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'pmdarima']

test_requirements = [ ]

setup(
    author="Ben McCarty",
    author_email='bmccarty505@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Collection of personal functions for data science",
    entry_points={
        'console_scripts': [
            'bmcds=bmcds.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='bmcds',
    name='bmcds',
    packages=find_packages(include=['bmcds', 'bmcds.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/BenJMcCarty/bmcds',
    version='0.1.2',
    zip_safe=False,
)
