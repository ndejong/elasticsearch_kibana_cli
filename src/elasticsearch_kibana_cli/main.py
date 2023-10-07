import json
import os
import sys

from . import constants
from .exceptions import ElasticsearchKibanaCLIException
from .lib.config import ElasticsearchKibanaCLIConfig
from .lib.connection import ElasticsearchKibanaCLIConnection
from .lib.logger import Logger
from .lib.search import ElasticsearchKibanaCLISearch
from .lib.summary import ElasticsearchKibanaCLISummary

logger = Logger(name=constants.TITLE).logging


class ElasticsearchKibanaInterface:
    config = None
    config_filename = None
    search = None
    connection = None

    def __init__(self, config_filename=None):
        logger.info("{} v{}".format(constants.CLI_NAME, constants.VERSION))
        self.config_filename = config_filename

    def list_searches(self):
        if self.config is None:
            self.config = self.read_config(self.config_filename)
        data = []
        if "search_definitions" not in self.config:
            raise ElasticsearchKibanaCLIException('Configuration does not provide a "search_definitions" section.')
        else:
            for definition_key in self.config["search_definitions"].keys():
                data.append(definition_key)
            return data

    def show_search(self, name):
        if self.config is None:
            self.config = self.read_config(self.config_filename)

        if name is None:
            names = self.list_searches()
            if len(names) < 1:
                raise ElasticsearchKibanaCLIException('No named "search_definitions" found in configuration file.')
            elif len(names) > 1:
                raise ElasticsearchKibanaCLIException(
                    'Search name not provided and more than one "search_definitions" '
                    "name exists in the configuration file.  Unable to determine "
                    "which search name to use."
                )
            name = names[0]
            logger.debug('Found a single "search_definitions" name in configuration file: {}'.format(name))

        if name not in self.list_searches():
            raise ElasticsearchKibanaCLIException(
                'Configuration does not provide "search_definitions" section with ' 'name "{}"'.format(name)
            )
        return self.config["search_definitions"][name]

    def perform_search(self, name=None, split_count=None, ping_connection=True):
        if self.config is None:
            self.config = self.read_config(self.config_filename)

        search_config = self.show_search(name)

        if split_count is not None:
            search_config["splits"] = int(split_count)
        if "splits" not in search_config.keys():
            search_config["splits"] = constants.SEARCH_SPLIT_COUNT_DEFAULT

        self.kibana_connect(ping_connection=ping_connection)
        return self.search.msearch(**search_config)

    def generate_summary(self, filename=None, data=None, top_count=3):
        if filename:
            filename = os.path.expanduser(filename)

            if filename == "-":
                logger.debug("Reading input from stdin")
                rawdata = sys.stdin.read()
            elif os.path.isfile(filename):
                logger.debug("Reading input from {}".format(filename))
                with open(filename, "r") as f:
                    rawdata = f.read()
            else:
                raise ElasticsearchKibanaCLIException("Unable to locate input file", filename)

            try:
                data = json.loads(rawdata)
            except json.decoder.JSONDecodeError as e:
                raise ElasticsearchKibanaCLIException("JSON data decode error. " + str(e))

        return ElasticsearchKibanaCLISummary().summary(data=data, top_count=top_count)

    def read_config(self, config_filename):
        config = ElasticsearchKibanaCLIConfig(config_filename=config_filename).config
        logger.info("Loaded configuration filename {}".format(config_filename))
        return config

    def kibana_connect(self, ping_connection=True, kbn_version=None):
        base_uri = "http://127.0.0.1:9200"
        if "base_uri" in self.config.keys():
            base_uri = self.config["base_uri"]

        proxy_config = None
        if "internal_proxy" in self.config.keys():
            proxy_config = self.config["internal_proxy"]
            logger.debug("Using internal_proxy to connect {}".format(base_uri))
        else:
            logger.debug("Using direct connection {}".format(base_uri))

        self.connection = ElasticsearchKibanaCLIConnection(proxy_config=proxy_config)
        self.connection.attach(base_uri=base_uri, kbn_version=kbn_version)
        logger.debug("Connection definition setup {}".format(self.connection.client_connect_address))

        if ping_connection is True:
            if self.connection.ping():
                logger.info("Ping okay {}".format(self.connection.client_connect_address))
            else:
                raise ElasticsearchKibanaCLIException(
                    "Unable to ping Kibana endpoint", format(self.connection.client_connect_address)
                )
        else:
            logger.debug("Skipping ping endpoint check via {}".format(self.connection.client_connect_address))

        self.search = ElasticsearchKibanaCLISearch(connection=self.connection)
