#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import (
    find_packages,
    setup
)

extras_require = {
    'linter': [
        "flake8==3.7.9",
        "isort>=4.2.15,<4.3.22",
    ],
    'dev': [
        "bumpversion==0.6.0",
        "pytest==5.4.3",
        "twine==3.1.1",
        "mock==4.0.2",
        "when-changed",
        "pytest-cov==2.8.1"
    ]
}

extras_require['dev'] = (
    extras_require['linter'] + extras_require['dev']
)

setup(
    name='awesomesauce',
    version='1.0',
    description='Awesomesauce agent-based Ethereum smart contract testing',
    long_description_markdown_filename='README.md',
    author='SKALE Labs',
    author_email='support@skalelabs.com',
    url='https://github.com/skalenetwork/awesomesauce',
    include_package_data=True,
    install_requires=[
        "skale.py==3.10.dev15",
        "python-dotenv==0.10.3",
        "Click==7.1.2",
        "Mesa>=0.8.4",
        "NetworkX>=2.2",
        "multilevel_mesa",
        "jupyter",
        "matplotlib",
        "transitions"
    ],

    python_requires='>=3.6,<4',
    extras_require=extras_require,

    keywords='skale',
    packages=find_packages(exclude=['tests']),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ]
)
