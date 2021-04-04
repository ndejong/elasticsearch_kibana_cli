
import sys
import json

from elasticsearch_kibana_cli import __title__ as NAME
from elasticsearch_kibana_cli.utils.logger import Logger


logger = Logger(NAME).logging


def output_handler(data, filename=None, compact=False):

    if compact:
        output = json.dumps(data, indent=None, separators=(',', ':'))
    else:
        output = json.dumps(data, indent='  ', separators=(', ', ': '))

    if filename is None or filename.upper() == 'STDOUT':
        print(output)
    elif filename.upper() == 'STDERR':
        print(output, file=sys.stderr)
    else:
        logger.info('Saving output to filename {}'.format(filename))
        with open(filename, 'w') as f:
            f.write(output)
