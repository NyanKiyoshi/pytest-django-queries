#!/usr/bin/env python

from sys import version_info
from os.path import isfile
from setuptools import setup

REQUIREMENTS = ['pytest>=4.4.0', 'freezegun']
DEV_REQUIREMENTS = []

if version_info < (3, ):
    REQUIREMENTS.append('django<2')
else:
    REQUIREMENTS.append('django')


if isfile('README.md'):
    with open('README.md') as fp:
        long_description = fp.read()
else:
    long_description = ''


setup(
    name='pytest-django-queries',
    author='NyanKiyoshi',
    author_email='hello@vanille.bid',
    url='https://github.com/NyanKiyoshi/pytest-django-queries/',
    description='Generate performance rapports from your django database '
                'performance tests.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.1.0',
    packages=['pytest_django_queries'],
    include_package_data=True,
    entry_points={
        'pytest11': ['django_queries = pytest_django_queries.plugin']},
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Framework :: Django',
        'Framework :: Pytest',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    install_requires=REQUIREMENTS,
    extra_requires={
        "dev": DEV_REQUIREMENTS},
    zip_safe=False)
