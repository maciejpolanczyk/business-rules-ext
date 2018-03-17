#! /usr/bin/env python

import setuptools

from business_rules import __version__ as version

setuptools.setup(
    name='business-rules-ext',
    version=version,
    description='Python DSL for setting up business intelligence rules that can be configured without code',
    author='Maciej Polanczyk',
    author_email='maciej.polanczyk@gmail.com',
    url='https://github.com/maciejpolanczyk/django-business-rules-ext/',
    packages=['business_rules'],
    license='BSD License',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
