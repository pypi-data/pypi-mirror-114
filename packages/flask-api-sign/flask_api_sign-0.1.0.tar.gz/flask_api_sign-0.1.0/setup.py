#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Flask Api Sign Verification
-------------

Flask extension of Api Sign Verification.
"""
from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'Flask>=1.0',
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='flask_api_sign',
    version='0.1.0',
    description="Flask extension of Api sign Verification",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    author="juforg",
    author_email='juforg@gmail.com',
    url='https://github.com/juforg/flask-api-sign',
    packages=[
        'flask_api_sign',
    ],
    # package_dir={'flask_api_sign':
    #              'flask_api_sign'},
    entry_points={
        'console_scripts': [
            'flask_api_sign=flask_api_sign.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords=['flask', 'api', 'sign', 'auth', 'verification', 'flask_api_sign'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Natural Language :: Chinese (Simplified)',
        'Environment :: Plugins',
        'Framework :: Flask',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS"
    ],
    test_suite='tests',
    tests_require=test_requirements
)
