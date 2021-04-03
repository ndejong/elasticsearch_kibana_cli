# This file was auto-generated by Shut. DO NOT EDIT
# For more information about Shut, check out https://pypi.org/project/shut/

from __future__ import print_function
import io
import os
import setuptools
import sys

readme_file = 'README.md'
if os.path.isfile(readme_file):
  with io.open(readme_file, encoding='utf8') as fp:
    long_description = fp.read()
else:
  print("warning: file \"{}\" does not exist.".format(readme_file), file=sys.stderr)
  long_description = None

requirements = [
  'bs4',
  'maya',
  'dpath',
  'Flask',
  'PyYAML',
  'urllib3',
  'chardet',
  'requests',
  'elasticsearch-dsl',
]

setuptools.setup(
  name = 'elasticsearch_kibana_cli',
  version = '0.3.0',
  author = 'Nicholas de Jong',
  author_email = 'contact@nicholasdejong.com',
  description = 'CLI interface to query Elasticsearch backend via the Kibana frontend.',
  long_description = long_description,
  long_description_content_type = 'text/markdown',
  url = 'https://github.com/ndejong/elasticsearch_kibana_cli',
  license = 'BSD2',
  packages = setuptools.find_packages('src', ['test', 'test.*', 'tests', 'tests.*', 'docs', 'docs.*']),
  package_dir = {'': 'src'},
  include_package_data = True,
  install_requires = requirements,
  extras_require = {},
  tests_require = [],
  python_requires = '>=3.5.0,<4.0.0',
  data_files = [],
  entry_points = {
    'console_scripts': [
      'eskbcli = elasticsearch_kibana_cli.cli.entrypoints:eskbcli',
    ]
  },
  cmdclass = {},
  keywords = ['kibana', 'elasticsearch', 'elasticsearch-client'],
  classifiers = ['Intended Audience :: System Administrators', 'Intended Audience :: Information Technology', 'Programming Language :: Python :: 3', 'License :: OSI Approved :: BSD License'],
  zip_safe = True,
)
