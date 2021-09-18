
import sys
import json

from elasticsearch_kibana_cli import __title__ as NAME
from elasticsearch_kibana_cli.utils.logger import Logger
from elasticsearch_kibana_cli.exceptions.ElasticsearchKibanaCLIException import ElasticsearchKibanaCLIException


logger = Logger(NAME).logging


def output_handler(data, filename=None, compact=False, replacements=None):

    if compact:
        output = json.dumps(data, indent=None, separators=(',', ':'))
    else:
        output = json.dumps(data, indent='  ', separators=(', ', ': '))

    if replacements:
        output = replacements_handler(output, replacements)

    if filename is None or filename.upper() == 'STDOUT':
        print(output)
    elif filename.upper() == 'STDERR':
        print(output, file=sys.stderr)
    else:
        logger.info('Saving output to filename {}'.format(filename))
        with open(filename, 'w') as f:
            f.write(output)


def replacements_handler(s, replacements):
    if type(replacements) is not list:
        raise ElasticsearchKibanaCLIException('replacements is not list type')
    for replacement in replacements:
        if type(replacement) is not tuple:
            raise ElasticsearchKibanaCLIException('replacement is not tuple type')
        s = s.replace(replacement[0], replacement[1])
    return s

