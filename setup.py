#!/usr/bin/env python

from os.path import isfile
from setuptools import setup

REQUIREMENTS = ['pytest', 'django']
TEST_REQUIREMENTS = []


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
    version='0.0.0',
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
    tests_require=TEST_REQUIREMENTS,
    zip_safe=False)
