
import sys
import json


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
        with open(filename, 'w') as f:
            f.write(output)
