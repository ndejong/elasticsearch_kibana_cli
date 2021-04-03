
from signal import signal, SIGINT

from elasticsearch_kibana_cli import __cli_name__ as CLI_NAME
from elasticsearch_kibana_cli import __version__ as VERSION
from elasticsearch_kibana_cli.cli import click_cli
from elasticsearch_kibana_cli.exceptions.ElasticsearchKibanaCLIException import ElasticsearchKibanaCLIException


def sigint_handler(signal_received, frame):
    print('SIGINT received, exiting.')
    exit(1)


def eskbcli():
    signal(SIGINT, sigint_handler)

    try:
        click_cli.eskbcli_interface()
    except ElasticsearchKibanaCLIException as e:
        print('')
        print('{} v{}'.format(CLI_NAME, VERSION))
        print('ERROR: ', end='')
        for err in iter(e.args):
            print(err)
        print('')
        exit(9)
