
from elasticsearch_kibana_cli import __title__ as NAME
from elasticsearch_kibana_cli import __version__ as VERSION
from elasticsearch_kibana_cli import __cli_name__ as CLI_NAME
from elasticsearch_kibana_cli import __search_split_count_default__ as SEARCH_SPLIT_COUNT_DEFAULT

from elasticsearch_kibana_cli.utils.logger import Logger
from elasticsearch_kibana_cli.utils.config import ElasticsearchKibanaCLIConfig
from elasticsearch_kibana_cli.utils.connection import ElasticsearchKibanaCLIConnection
from elasticsearch_kibana_cli.utils.search import ElasticsearchKibanaCLISearch
from elasticsearch_kibana_cli.exceptions.ElasticsearchKibanaCLIException import ElasticsearchKibanaCLIException


logger = Logger(name=NAME).logging


class ElasticsearchKibanaInterface:

    config = None
    search = None
    connection = None

    def __init__(self, config_filename):
        logger.info('{} v{}'.format(CLI_NAME, VERSION))

        self.config = ElasticsearchKibanaCLIConfig(config_filename=config_filename).config
        logger.info('Loaded configuration filename {}'.format(config_filename))

    def list_searches(self):
        data = []
        if 'search_definitions' not in self.config:
            raise ElasticsearchKibanaCLIException('Configuration does not provide a "search_definitions" section.')
        else:
            for definition_key in self.config['search_definitions'].keys():
                data.append(definition_key)
            return data

    def show_search(self, name):
        if name not in self.list_searches():
            raise ElasticsearchKibanaCLIException('Configuration does not provide "search_definitions" '
                                                  'section with name "{}"'.format(name))
        else:
            return self.config['search_definitions'][name]

    def perform_search(self, name, split_count=None, ping_connection=True):

        search_config = self.show_search(name)

        if split_count is not None:
            search_config['splits'] = int(split_count)
        if 'splits' not in search_config.keys():
            search_config['splits'] = SEARCH_SPLIT_COUNT_DEFAULT

        self.kibana_connect(ping_connection=ping_connection)
        return self.search.msearch(**search_config)

    def kibana_connect(self, ping_connection=True, kbn_version=None):

        base_uri = 'http://127.0.0.1:9200'
        if 'base_uri' in self.config.keys():
            base_uri = self.config['base_uri']

        proxy_config = None
        if 'internal_proxy' in self.config.keys():
            proxy_config = self.config['internal_proxy']
            logger.debug('Using internal_proxy to connect {}'.format(base_uri))
        else:
            logger.debug('Using direct connection {}'.format(base_uri))

        self.connection = ElasticsearchKibanaCLIConnection(proxy_config=proxy_config)
        self.connection.attach(base_uri=base_uri, kbn_version=kbn_version)
        logger.debug('Connection definition setup {}'.format(self.connection.client_connect_address))

        if ping_connection is True:
            if self.connection.ping():
                logger.info('Ping okay {}'.format(self.connection.client_connect_address))
            else:
                raise ElasticsearchKibanaCLIException('Unable to ping Kibana endpoint', format(self.connection.client_connect_address))
        else:
            logger.debug('Skipping ping endpoint check via {}'.format(self.connection.client_connect_address))

        self.search = ElasticsearchKibanaCLISearch(connection=self.connection)
