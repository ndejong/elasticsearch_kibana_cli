
import os
import json
import time

from elasticsearch_kibana_cli.exceptions.ElasticsearchKibanaCLIException import ElasticsearchKibanaCLIException

from elasticsearch_kibana_cli import __title__ as NAME
from elasticsearch_kibana_cli import __version__ as VERSION
from elasticsearch_kibana_cli.utils.logger import ElasticsearchKibanaCLILogger
from elasticsearch_kibana_cli.utils.config import ElasticsearchKibanaCLIConfig
from elasticsearch_kibana_cli.utils.connection import ElasticsearchKibanaCLIConnection
from elasticsearch_kibana_cli.utils.search import ElasticsearchKibanaCLISearch


class ElasticsearchKibanaCLI:

    search = None
    connection = None
    output_filename = None

    def __init__(self, output_filename=None, debug=False):

        if debug:
            loglevel_env_override = '{}_LOGLEVEL'.format(NAME.replace('_', '').replace(' ', '').upper())
            os.environ[loglevel_env_override] = 'debug'

        global logger
        logger = ElasticsearchKibanaCLILogger().logger
        logger.info(NAME)
        logger.info('version {}'.format(VERSION))

        global config, config_filename
        try:
            es_config = ElasticsearchKibanaCLIConfig()
        except ElasticsearchKibanaCLIException as e:
            logger.fatal(str(e).replace('\n', ' '))
            exit(1)

        config = es_config.config
        config_filename = es_config.config_filename
        logger.info('Loaded configuration filename {}'.format(config_filename))

        self.output_filename = output_filename

    def connect_search(self, ping_connection=True, kbn_version=None):

        base_uri = 'http://127.0.0.1:9200'
        if 'base_uri' in config.keys():
            base_uri = config['base_uri']

        proxy_config = None
        if 'internal_proxy' in config.keys():
            proxy_config = config['internal_proxy']
            logger.debug('Using internal_proxy to connect {}'.format(base_uri))
        else:
            logger.debug('Using direct connection {}'.format(base_uri))

        self.connection = ElasticsearchKibanaCLIConnection(proxy_config=proxy_config)
        self.connection.attach(base_uri=base_uri, kbn_version=kbn_version)
        logger.debug('Connection definition setup {}'.format(self.connection.client_connect_address))

        if ping_connection is True:
            ping_status = False
            try:
                ping_status = self.connection.ping()
            except Exception as e:
                logger.fatal(str(e).replace('\n', ' '))
                exit(1)

            if ping_status:
                logger.info('Ping okay {}'.format(self.connection.client_connect_address))
            else:
                logger.fatal('Unable to ping Kibana endpoint via {}'.format(self.connection.client_connect_address))
                exit(1)
        else:
            logger.debug('Skipping ping endpoint check via {}'.format(self.connection.client_connect_address))

        self.search = ElasticsearchKibanaCLISearch(connection=self.connection)

    def msearch(self, search_definition, hit_count=None, split_count=None, ping_connection=True, kbn_version=None):

        self.connect_search(ping_connection=ping_connection, kbn_version=kbn_version)

        if 'search_definitions' not in config or search_definition not in config['search_definitions']:
            logger.error('Unable to locate "{}" in config under "search_definitions"'.format(search_definition))
            return

        kwargs = config['search_definitions'][search_definition]

        if hit_count is not None:
            kwargs['size'] = hit_count

        if split_count is not None:
            kwargs['splits'] = split_count

        try:
            data = self.search.msearch(**kwargs)
        except ElasticsearchKibanaCLIException as e:
            logger.fatal(str(e).replace('\n', ' '))
            exit(1)

        self.__output(data)
        time.sleep(0.1)  # allows internal_proxy threads to close-out
        return

    def search_definitions(self):
        data = []
        if 'search_definitions' in config:
            for definition_key in config['search_definitions'].keys():
                data.append(definition_key)
        self.__output(data)
        return

    def __output(self, data):
        if self.output_filename is None or self.output_filename == '-':
            print(json.dumps(data, indent='  '))
        else:
            with open(self.output_filename, 'w') as f:
                json.dump(data, f, separators=(',', ':'))
        return
