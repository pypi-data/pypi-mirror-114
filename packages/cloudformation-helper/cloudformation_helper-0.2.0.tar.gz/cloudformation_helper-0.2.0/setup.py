#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'boto3>=1.17', 'PyYAML>=5.4.1' ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Jean-Sebastien Gelinas",
    author_email='calestar@gmail.com',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Small python tool to make it easier to use cloudformation.",
    entry_points={
        'console_scripts': [
            'cfhelper=cloudformation_helper.cli:cfhelper',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='cloudformation_helper',
    name='cloudformation_helper',
    packages=find_packages(include=['cloudformation_helper', 'cloudformation_helper.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/calestar/cloudformation_helper',
    version='0.2.0',
    zip_safe=False,
)
