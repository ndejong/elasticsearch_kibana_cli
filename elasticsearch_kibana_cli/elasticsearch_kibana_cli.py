
import os
import json
import time

from . import ElasticsearchKibanaCLIException

from . import ElasticsearchKibanaCLILogger
from . import ElasticsearchKibanaCLIConfig
from . import ElasticsearchKibanaCLIConnection
from . import ElasticsearchKibanaCLISearch


class ElasticsearchKibanaCLI:

    search = None
    connection = None

    def __init__(self, ping_connection=True, kbn_version=None, debug=False):

        if debug:
            os.environ['ELASTICSEARCHKIBANACLI_LOGLEVEL'] = 'debug'

        global logger
        logger = ElasticsearchKibanaCLILogger().logger

        global config, config_filename
        try:
            es_config = ElasticsearchKibanaCLIConfig()
        except ElasticsearchKibanaCLIException as e:
            logger.fatal(str(e).replace('\n', ' '))
            exit()

        config = es_config.config
        config_filename = es_config.config_filename
        logger.debug('Using config filename {}'.format(config_filename))

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
        logger.debug('Connection setup {}'.format(self.connection.client_connect_address))

        if ping_connection is True:
            if not self.connection.ping():
                raise ElasticsearchKibanaCLIException('Unable to ping Kibana endpoint via {}'.
                                                      format(self.connection.client_connect_address))
            else:
                logger.debug('Ping okay {}'.format(self.connection.client_connect_address))

        self.search = ElasticsearchKibanaCLISearch(connection=self.connection)

    def main(self):

        definition_name = 'example01'
        if 'search_definitions' not in config or definition_name not in config['search_definitions']:
            logger.error('Unable to locate config[search_definitions][{}]'.format(definition_name))
            return

        data = self.search.msearch(**config['search_definitions'][definition_name])
        print(json.dumps(data))

        time.sleep(3)
