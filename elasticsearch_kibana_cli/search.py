
import json
import time
import maya
import requests
from elasticsearch_dsl import Q, A

from . import NAME
from . import VERSION
from . import ElasticsearchKibanaCLIException
from . import ElasticsearchKibanaCLILogger


class ElasticsearchKibanaCLISearch:

    connection = None
    user_agent = '{}/{}'.format(NAME, VERSION)

    def __init__(self, connection):

        global logger
        logger = ElasticsearchKibanaCLILogger().logger

        self.connection = connection

    def msearch(self, index, search, source=None):

        url = '{}/elasticsearch/_msearch'.format(self.connection.client_connect_address)

        payload_header = self.__payload_header(index)
        payload_body = self.__payload_body(search, source)

        request_headers = {
            'content-type': 'application/x-ndjson',
            'kbn-version': str(self.connection.kbn_version),
            'user-agent': self.user_agent
        }

        r = requests.post(
            url,
            data='{}\n{}\n'.format(payload_header, payload_body),
            headers=request_headers
        )
        return r.json()

    def __payload_header(self, index):
        return json.dumps({
            'index': index,
            'ignore_unavailable': True,
            'preference': int(round(time.time() * 1000))
        })

    def __payload_body(self, query_params, source=None):

        for param_name in ['must', 'must_not', 'should', 'should_not', 'filter']:
            if param_name in query_params:
                query_params[param_name] = self.__parse_query_param(query_params[param_name])
            else:
                query_params[param_name] = []

        query = Q(
            'bool',
            must=query_params['must'],
            must_not=query_params['must_not'],
            should=query_params['should'],
            should_not=query_params['should_not'],
            minimum_should_match=query_params['minimum_should_match'] if 'minimum_should_match' in query_params else (1 if len(query_params['should']) > 0 else None),
            filter=query_params['filter']
        )

        payload_values = {
            'source': json.dumps(source) if source is not None else '[ ]',
            'size': int(query_params['size']) if 'size' in query_params else 50,
            'aggs': '{ }',
            'timeout': '"' + (str(query_params['timeout']) if 'timeout' in query_params else '30s') + '"',
            'query': json.dumps(query.to_dict())
        }

        payload_json = """
            {
              "version": true,
              "sort": [ ],
              "stored_fields": [ ],
              "script_fields": { },
              "docvalue_fields": [ ],
              "highlight": { },
              
              "_source": __SOURCE__,
              "size": __SIZE__,
              "aggs": __AGGS__,
              "timeout": __TIMEOUT__,
              "query": __QUERY__
            }
        """

        for payload_k, payload_v in payload_values.items():
            replace_token = '__{}__'.format(payload_k.upper())
            payload_json = payload_json.replace(replace_token, str(payload_v))

        return json.dumps(json.loads(payload_json))

    def __parse_query_param(self, query_param):
        query = []
        for param_query_type, param_queries in query_param.items():
            for param_query_item in param_queries:
                if param_query_item == '__timestamp':
                    timestamp = self.__parse_query_timestamp(param_queries[param_query_item])
                    query.append(Q(param_query_type, **{'@timestamp': timestamp}))
                elif type(param_query_item) is dict:
                    for param_query_item_k, param_query_item_v in param_query_item.items():
                        query.append(Q(param_query_type, **{param_query_item_k:param_query_item_v}))
                else:
                    raise ElasticsearchKibanaCLIException('Unsupported type', param_query_item)
        return query

    def __parse_query_timestamp(self, element):
        if type(element) in [int, str, bool]:
            return element
        elif type(element) is list:
            r = []
            for item in element:
                r.append(self.__parse_query_timestamp(item))
            return r
        elif type(element) is dict:
            r = {}
            for key, value in element.items():
                if key in ['gt', 'gte', 'lt', 'lte', 'eq']:
                    r[key] = int(maya.when(value).datetime().timestamp() * 1000)
                else:
                    r[key] = self.__parse_query_timestamp(value)
            r['format'] = 'epoch_millis'
            return r
        else:
            raise ElasticsearchKibanaCLIException('Unsupported type', element)
