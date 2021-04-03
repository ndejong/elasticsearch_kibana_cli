
import os
import json
import time
import hashlib
import tempfile
import requests
import threading
from bs4 import BeautifulSoup

from elasticsearch_kibana_cli import __title__ as NAME
from elasticsearch_kibana_cli import __cli_name__ as CLI_NAME
from elasticsearch_kibana_cli import __version__ as VERSION
from elasticsearch_kibana_cli.utils.logger import Logger
from elasticsearch_kibana_cli.utils.internal_proxy import ElasticsearchKibanaCLIInternalProxy
from elasticsearch_kibana_cli.exceptions.ElasticsearchKibanaCLIException import ElasticsearchKibanaCLIException


logger = Logger(name=NAME).logging


class ElasticsearchKibanaCLIConnection:

    user_agent = '{}/{}'.format(NAME, VERSION)
    kbn_version = None
    internal_proxy = None
    client_connect_address= None

    def __init__(self, proxy_config=None):
        if proxy_config is not None:
            self.internal_proxy = ElasticsearchKibanaCLIInternalProxy(config=proxy_config)

    def attach(self, base_uri, kbn_version=None):
        if self.internal_proxy:
            thread = threading.Thread(target=self.internal_proxy.start, args=[base_uri])
            thread.daemon = True
            thread.start()
            time.sleep(1)  # wait for internal_proxy thread to start <-- got to be a better way than this?
            self.client_connect_address = self.internal_proxy.client_connect_address
        else:
            self.client_connect_address = base_uri

        if kbn_version:
            self.kbn_version = kbn_version
        else:
            self.kbn_version = self.__kbn_version()

        return self.client_connect_address

    def ping(self, path='/api/spaces/space'):
        url = '{}{}'.format(self.client_connect_address, path)
        headers = {'user-agent': self.user_agent}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return True
        return False

    def __kbn_version(self):
        metadata = self.__kbn_metadata()
        if 'version' not in metadata.keys():
            raise ElasticsearchKibanaCLIException('Unable to locate required version value in metadata')
        return metadata['version']

    def __kbn_metadata(self, use_cache=True):
        if self.client_connect_address is None:
            raise ElasticsearchKibanaCLIException('Attempt to call __kbn_metadata before client_connect_address is set!')

        cache_filename = '{}-metadata.cache'.format(self.__kbn_cache_basename())

        if use_cache and os.path.isfile(cache_filename):
            with open(cache_filename, 'r') as f:
                logger.debug('kbn_metadata read from cache file {}'.format(cache_filename))
                return json.load(f)

        headers = {'user-agent': self.user_agent}
        r = requests.get(self.client_connect_address, headers=headers)

        if r.status_code != 200:
            raise ElasticsearchKibanaCLIException('Unable to obtain data from {}'.format(self.client_connect_address))

        soup = BeautifulSoup(r.content, 'html.parser')
        metadata_find = soup.find('kbn-injected-metadata')
        if not metadata_find:
            raise ElasticsearchKibanaCLIException('Unable to locate kbn-injected-metadata '
                                                  'within {}'.format(self.client_connect_address))

        metadata = json.loads(metadata_find['data'])
        if use_cache:
            with open(cache_filename, 'w') as f:
                logger.debug('kbn_metadata write to cache file {}'.format(cache_filename))
                json.dump(metadata, f)
        return metadata

    def __kbn_cache_basename(self, base_path=None):
        if base_path is None:
            base_path = tempfile.gettempdir()
        if not os.path.exists(base_path):
            raise ElasticsearchKibanaCLIException('Cache base_path does not exist', base_path)

        return os.path.join(
            base_path,
            '{}-{}'.format(
                CLI_NAME,
                hashlib.md5(self.client_connect_address.encode('utf-8')).hexdigest()[0:8]
            )
        )
