
import os
import click

from elasticsearch_kibana_cli import __title__ as NAME
from elasticsearch_kibana_cli import __version__ as VERSION
from elasticsearch_kibana_cli import __env_config_filename__ as ENV_CONFIG_FILENAME
from elasticsearch_kibana_cli import __search_split_count_default__ as SEARCH_SPLIT_COUNT_DEFAULT
from elasticsearch_kibana_cli import __summary_top_count_default__ as SUMMARY_TOP_COUNT_DEFAULT

from elasticsearch_kibana_cli.utils.logger import Logger
from elasticsearch_kibana_cli.utils.output import output_handler
from elasticsearch_kibana_cli.ElasticsearchKibanaInterface import ElasticsearchKibanaInterface


config_file_default = '~/.eskbcli'
elasticsearch_kibana_interface = None


@click.group()
@click.option('-c', '--config', help='Config file location; overrides {} environment var and the default {} value.'
              .format(ENV_CONFIG_FILENAME, config_file_default))
@click.option('-v', '--verbose', is_flag=True, help='Verbose logging messages (debug level).')
@click.option('-q', '--quiet', is_flag=True, help='Quiet mode, takes priority over --verbose')
@click.version_option(VERSION)
def eskbcli_interface(config, verbose, quiet):
    """
    ElasticSearch Kibana CLI (`eskbcli`) provides a shell interface to query
    an ElasticSearch backend via the Kibana frontend which is useful in
    situations where the ElasticSearch backend is not otherwise accessible.

    ElasticSearch Kibana CLI makes it possible to copy-paste query expressions
    directly from the Kibana user-interface and then easily access very large
    sets of result data.  This makes the `eskbcli` useful in SecOps situations
    where the ability to rapidly move from a Kibana query to raw data is
    valued.

    Configuration options are available to adjust http-headers so-as-to enable
    access to Kibana in situations that require complex user-authentication
    such as when Kibana exists behind an OAuth reverse proxy or other session-
    based authentication arrangement.

    Documentation available https://elasticsearch-kibana-cli.readthedocs.io
    """

    if quiet:
        Logger(name=NAME).setup(level='CRITICAL')
    elif verbose:
        Logger(name=NAME).setup(level='DEBUG')
    else:
        Logger(name=NAME).setup(level='INFO')

    if config is not None:
        config_filename = config
    else:
        if os.getenv(ENV_CONFIG_FILENAME):
            config_filename = os.getenv(ENV_CONFIG_FILENAME)
        else:
            config_filename = config_file_default

    global elasticsearch_kibana_interface
    elasticsearch_kibana_interface = ElasticsearchKibanaInterface(config_filename=config_filename)


@eskbcli_interface.command('search')
@click.option('-o', '--out',
              help='Filename to write output.',
              required=False, default='stdout', show_default=True)
@click.option('-S', '--summary',
              help='Generate summary report and output to stderr with the default summary-top count.',
              is_flag=True, required=False, default=False, show_default=True)
@click.option('-ST', '--summary-top',
              help='Depth of the top-count summary to produce.  [default: {}]'.format(SUMMARY_TOP_COUNT_DEFAULT),
              required=False, type=int, default=None, show_default=False)
@click.option('-s', '--splits',
              help='Number of splits to break search into.  [default: {}]'.format(SEARCH_SPLIT_COUNT_DEFAULT),
              required=False, type=int, default=None, show_default=False)  # NB: manually express default value
@click.option('-np', '--no-ping',
              help='Do not ping the Kibana endpoint before using the connection.',
              is_flag=True, required=False, default=False, show_default=True)
@click.argument('search_name', required=False)
def perform_search(**kwargs):
    """
    Execute the named search configuration.
    """
    data = elasticsearch_kibana_interface.perform_search(
        name=kwargs['search_name'],
        split_count=kwargs['splits'],
        ping_connection=False if kwargs['no_ping'] is True else True
    )

    output_handler(
        data=data,
        filename=kwargs['out'],
        compact=False if kwargs['out'] == 'stdout' else True
    )

    if ('summary' in kwargs.keys() and kwargs['summary'] is True) or \
            ('summary_top' in kwargs.keys() and kwargs['summary_top'] is not None):
        output_handler(
            data=elasticsearch_kibana_interface.generate_summary(data=data, top_count=kwargs['summary_top']),
            filename='stderr',
            compact=False
        )


@eskbcli_interface.command('summary')
@click.option('-t', '--top',
              help='Depth of the top-count summary to produce.',
              required=False, default=SUMMARY_TOP_COUNT_DEFAULT, show_default=True)
@click.option('-o', '--out',
              help='Filename to write output.',
              required=False, default='stdout', show_default=True)
@click.argument('filename', required=True)
def generate_summary(**kwargs):
    """
    Summary report for search result datafile; use "-" to pipe stdin.
    """
    output_handler(
        data=elasticsearch_kibana_interface.generate_summary(
            filename=kwargs['filename'],
            top_count=kwargs['top'],
        ),
        filename=kwargs['out'],
        compact=False if kwargs['out'] == 'stdout' else True
    )


@eskbcli_interface.command('show')
@click.option('-o', '--out',
              help='Filename to write output.',
              required=False, default='stdout', show_default=True)
@click.argument('search_name', required=False)
def show_search(**kwargs):
    """
    Show the named eskbcli search configuration.
    """
    output_handler(
        data=elasticsearch_kibana_interface.show_search(name=kwargs['search_name']),
        filename=kwargs['out'],
        compact=False if kwargs['out'] == 'stdout' else True,
        replacements=[('___timestamp', '@timestamp')]
    )


@eskbcli_interface.command('list')
@click.option('-o', '--out',
              help='Filename to write output.',
              required=False, default='stdout', show_default=True)
def list_searches(**kwargs):
    """
    List the available eskbcli search names.
    """
    output_handler(
        data=elasticsearch_kibana_interface.list_searches(),
        filename=kwargs['out'],
        compact=False if kwargs['out'] == 'stdout' else True,
    )
