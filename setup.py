#!/usr/bin/env python3

from setuptools import setup, find_packages
from elasticsearch_kibana_cli import NAME
from elasticsearch_kibana_cli import VERSION

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='elasticsearch-kibana-cli',
    version=VERSION,
    description='CLI interface to query Elasticsearch backend via the Kibana frontend.',

    long_description=long_description,
    long_description_content_type='text/markdown',

    classifiers=[
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
    ],
    keywords='kibana elasticsearch elasticsearch-client',

    author='Nicholas de Jong',
    author_email='contact@nicholasdejong.com',
    url='https://github.com/ndejong/elasticsearch_kibana_cli',
    license='BSD 2-Clause',

    packages=find_packages(),
    scripts=['bin/eskbcli'],

    install_requires=['bs4', 'maya', 'dpath', 'flask', 'pyyaml', 'urllib3', 'chardet', 'requests', 'elasticsearch_dsl'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],

)
