
import os
import json
import time

from . import ElasticsearchKibanaCLIException

from . import NAME
from . import ElasticsearchKibanaCLILogger
from . import ElasticsearchKibanaCLIConfig
from . import ElasticsearchKibanaCLIConnection
from . import ElasticsearchKibanaCLISearch


class ElasticsearchKibanaCLI:

    search = None
    connection = None

    def __init__(self, ping_connection=True, kbn_version=None, debug=False):

        if debug:
            loglevel_env_override = '{}_LOGLEVEL'.format(NAME.replace('_', '').replace(' ', '').upper())
            os.environ[loglevel_env_override] = 'debug'

        global logger
        logger = ElasticsearchKibanaCLILogger().logger
        logger.info(NAME)

        global config, config_filename
        try:
            es_config = ElasticsearchKibanaCLIConfig()
        except ElasticsearchKibanaCLIException as e:
            logger.fatal(str(e).replace('\n', ' '))
            exit(1)

        config = es_config.config
        config_filename = es_config.config_filename
        logger.info('Using config filename {}'.format(config_filename))

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

    def msearch(self, search_definition, size=None):

        if 'search_definitions' not in config or search_definition not in config['search_definitions']:
            logger.error('Unable to locate "{}" in config under "search_definitions"'.format(search_definition))
            return

        kwargs = config['search_definitions'][search_definition]

        if size is not None:
            kwargs['size'] = size

        try:
            data = self.search.msearch(**kwargs)
        except ElasticsearchKibanaCLIException as e:
            logger.fatal(str(e).replace('\n', ' '))
            exit(1)

        print(json.dumps(data, indent='  '))
        time.sleep(0.1)  # allows internal_proxy threads to come back
        return

    def search_definitions(self):
        definition_keys = []
        if 'search_definitions' in config:
            for definition_key in config['search_definitions'].keys():
                definition_keys.append(definition_key)
        print(json.dumps(definition_keys, indent='  '))
        return
