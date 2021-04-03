
import os
import click

from elasticsearch_kibana_cli import __title__ as NAME
from elasticsearch_kibana_cli import __version__ as VERSION
from elasticsearch_kibana_cli import __env_config_filename__ as ENV_CONFIG_FILENAME
from elasticsearch_kibana_cli import __search_split_count_default__ as SEARCH_SPLIT_COUNT_DEFAULT

from elasticsearch_kibana_cli.utils.logger import Logger
from elasticsearch_kibana_cli.utils.output import output_handler
from elasticsearch_kibana_cli.ElasticsearchKibanaInterface import ElasticsearchKibanaInterface


config_file_default = '~/.eskbcli'
elasticsearch_kibana_interface = None


@click.group()
@click.option('-c', '--config', help='Overrides env {} config file setting and default {} config file setting.'
              .format(ENV_CONFIG_FILENAME, config_file_default))
@click.option('-v', '--verbose', is_flag=True, help='Verbose logging messages (debug level).')
@click.option('-q', '--quiet', is_flag=True, help='Quiet mode, takes priority over --verbose')
@click.version_option(VERSION)
def eskbcli_interface(config, verbose, quiet):
    """
    ElasticSearch Kibana CLI (`eskbcli`) provides a shell interface to query an ElasticSearch backend via
    the Kibana frontend which is useful in situations where the ElasticSearch backend is not otherwise
    accessible.

    ElasticSearch Kibana CLI makes it possible to copy-paste query expressions directly from the Kibana
    user-interface and then easily access very large sets of result data.  This makes the `eskbcli` useful
    in SecOps situations where the ability to rapidly move from a Kibana query to raw data is valued.

    Configuration options are available to adjust http-headers so-as-to enable access to Kibana in
    situations that require complex user-authentication such as when Kibana exists behind an OAuth
    reverse proxy or other session-based authentication arrangement.

    Documentation available https://elasticsearch-kibana-cli.readthedocs.io
    """

    if quiet:
        logger = Logger(name=NAME).setup(level='CRITICAL')
    elif verbose:
        logger = Logger(name=NAME).setup(level='DEBUG')
    else:
        logger = Logger(name=NAME).setup(level='INFO')

    if config is not None:
        config_filename = config
        logger.debug('config_filename taken from cli arg: {}'.format(config_filename))
    else:
        if os.getenv(ENV_CONFIG_FILENAME):
            config_filename = os.getenv(ENV_CONFIG_FILENAME)
            logger.debug('config_filename taken from env value: {}'.format(config_filename))
        else:
            config_filename = config_file_default
            logger.debug('config_filename using default: {}'.format(config_filename))

    global elasticsearch_kibana_interface
    elasticsearch_kibana_interface = ElasticsearchKibanaInterface(config_filename=config_filename)


@eskbcli_interface.command('list')
@click.option('-o', '--out', help='Filename to write data output.', required=False)
def list_searches(**kwargs):
    """
    List the available eskbcli search names.
    """
    output_handler(
        data=elasticsearch_kibana_interface.list_searches(),
        filename=kwargs['out'], compact=False if kwargs['out'] is None else True
    )


@eskbcli_interface.command('show')
@click.option('-o', '--out', help='Filename to write data output.', required=False)
@click.argument('search_name', required=True)
def show_search(**kwargs):
    """
    Show the named eskbcli search configuration.
    """
    output_handler(
        data=elasticsearch_kibana_interface.show_search(name=kwargs['search_name']),
        filename=kwargs['out'], compact=False if kwargs['out'] is None else True
    )


@eskbcli_interface.command('search')
@click.option('-o', '--out', help='Filename to write data output.', required=False)
@click.option('-s', '--splits', help='Number of splits to break the search into (default:{})'
              .format(SEARCH_SPLIT_COUNT_DEFAULT), required=False)
@click.option('-np', '--no-ping', help='Do not ping the Kibana endpoint before using the connection (default: False)',
              is_flag=True, required=False, default=False)
@click.argument('search_name', required=True)
def perform_search(**kwargs):
    """
    Execute the named search configuration.
    """
    output_handler(
        data=elasticsearch_kibana_interface.perform_search(
            name=kwargs['search_name'],
            split_count=kwargs['splits'],
            ping_connection=False if kwargs['no_ping'] is True else True
        ),
        filename=kwargs['out'],
        compact=False if kwargs['out'] is None else True
    )
