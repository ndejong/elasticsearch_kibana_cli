import os

import yaml

from .. import constants
from ..exceptions import ElasticsearchKibanaCLIException
from ..lib.logger import Logger

logger = Logger(name=constants.TITLE).logging


class ElasticsearchKibanaCLIConfig:
    config = None
    config_root = constants.TITLE
    config_filename = None

    def __init__(self, config_filename=None):
        self.config_filename = os.path.expanduser(config_filename)
        logger.debug("loading config_filename: {}".format(self.config_filename))

        if self.config_filename is None or not os.path.isfile(self.config_filename):
            raise ElasticsearchKibanaCLIException("Unable to locate config_filename", self.config_filename)

        self.config = self.__load_config(self.config_filename)

    def __load_config(self, config_filename):
        loaded_config = {}

        with open(config_filename, "r") as f:
            try:
                loaded_config = yaml.safe_load(f.read().replace("@timestamp", "___timestamp"))
            except yaml.YAMLError as e:
                raise ElasticsearchKibanaCLIException(e)

        loaded_config = self.__replace_env_values(loaded_config)

        if type(loaded_config) is not dict:
            raise ElasticsearchKibanaCLIException("Configuration loaded is incorrect data type", self.config_root)

        if type(loaded_config) is not dict or self.config_root not in loaded_config.keys():
            raise ElasticsearchKibanaCLIException("Unable to locate config root", self.config_root)

        return loaded_config[self.config_root]

    def __replace_env_values(self, value):
        if value is None:
            return value
        elif type(value) in (int, bool):
            return value
        elif type(value) is str:
            if value.lower()[0:4] == "env:":
                env_name = value.replace("env:", "")
                logger.debug("Config element set via env value {}".format(env_name))
                env_val = os.getenv(env_name, None)
                if env_val is None or len(env_val) < 1:
                    raise ElasticsearchKibanaCLIException("Config requested env value not set", env_name)
                return env_val
            return value
        elif type(value) is list:
            r = []
            for item in value:
                r.append(self.__replace_env_values(item))
            return r
        elif type(value) is dict:
            r = {}
            for item_k, item_v in value.items():
                r[item_k] = self.__replace_env_values(item_v)
            return r
        else:
            raise ElasticsearchKibanaCLIException("Unsupported type in replace_env_values()", value)
