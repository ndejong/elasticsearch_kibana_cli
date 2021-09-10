
import os
import yaml

from elasticsearch_kibana_cli import __title__ as NAME
from elasticsearch_kibana_cli.utils.logger import Logger
from elasticsearch_kibana_cli.exceptions.ElasticsearchKibanaCLIException import ElasticsearchKibanaCLIException


logger = Logger(name=NAME).logging


class ElasticsearchKibanaCLIConfig:

    config = None
    config_root = NAME
    config_filename = None

    def __init__(self, config_filename=None):

        self.config_filename = os.path.expanduser(config_filename)
        logger.debug('loading config_filename: {}'.format(self.config_filename))

        if self.config_filename is None or not os.path.isfile(self.config_filename):
            raise ElasticsearchKibanaCLIException('Unable to locate config_filename', self.config_filename)

        self.config = self.__load_config(self.config_filename)

    def __load_config(self, config_filename):
        loaded_config = {}

        with open(config_filename, 'r') as f:
            try:
                loaded_config = yaml.safe_load(f.read().replace('@timestamp', '___timestamp'))
            except yaml.YAMLError as e:
                raise ElasticsearchKibanaCLIException(e)

        loaded_config = self.__replace_env_values(loaded_config)

        if type(loaded_config) is not dict:
            raise ElasticsearchKibanaCLIException('Configuration loaded is incorrect data type', self.config_root)

        if type(loaded_config) is not dict or self.config_root not in loaded_config.keys():
            raise ElasticsearchKibanaCLIException('Unable to locate config root', self.config_root)

        return loaded_config[self.config_root]

    def __replace_env_values(self, input):
        if input is None:
            return input
        elif type(input) in (int, bool):
            return input
        elif type(input) is str:
            if input.lower()[0:4] == 'env:':
                env_name = input.replace('env:', '')
                logger.debug('Config element set via env value {}'.format(env_name))
                value = os.getenv(env_name, None)
                if value is None or len(value) < 1:
                    raise ElasticsearchKibanaCLIException('Config requested env value not set', env_name)
                return value
            return input
        elif type(input) is list:
            r = []
            for item in input:
                r.append(self.__replace_env_values(item))
            return r
        elif type(input) is dict:
            r = {}
            for item_k, item_v in input.items():
                r[item_k] = self.__replace_env_values(item_v)
            return r
        else:
            raise ElasticsearchKibanaCLIException('Unsupported type in replace_env_values()', input)
