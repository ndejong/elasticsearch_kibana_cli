
import json
import time
import maya
import copy
import requests
import dpath.util
from collections import OrderedDict
from elasticsearch_dsl import Q, A

from elasticsearch_kibana_cli import __title__ as NAME
from elasticsearch_kibana_cli import __version__ as VERSION
from elasticsearch_kibana_cli import __search_split_bucket_limit__ as SEARCH_SPLIT_BUCKET_LIMIT


from elasticsearch_kibana_cli.exceptions.ElasticsearchKibanaCLIException import ElasticsearchKibanaCLIException
from elasticsearch_kibana_cli.utils.logger import Logger


logger = Logger(name=NAME).logging


class ElasticsearchKibanaCLISearch:

    connection = None
    user_agent = '{}/{}'.format(NAME, VERSION)

    def __init__(self, connection):
        self.connection = connection

    def msearch(self, index, search, size=SEARCH_SPLIT_BUCKET_LIMIT, source=None, splits=1, range_keyword='range'):

        url = '{}/elasticsearch/_msearch'.format(self.connection.client_connect_address)

        payload_data = ''
        for _ in range(0, splits):
            payload_data = '{}{}\n{}\n'.format(
                payload_data,
                self.__payload_header(copy.copy(index)),
                self.__payload_body(
                    query_params=copy.copy(search),
                    size=copy.copy(size),
                    source=copy.copy(source)
                )
            )

        if splits > 1:
            payload_data = self.__payload_range_splitter(payload_data, range_keyword=range_keyword)
            logger.info('Search split into {} requests based on "{}" keyword'.format(str(splits), range_keyword))

        request_headers = {
            'content-type': 'application/x-ndjson',
            'kbn-version': str(self.connection.kbn_version),
            'user-agent': self.user_agent
        }

        r = requests.post(
            url,
            data=payload_data,
            headers=request_headers
        )

        response_data = r.json()
        return_list = []

        hit_total = 0
        for hit_index in range(0, splits):
            value = None
            try:
                value = response_data['responses'][hit_index]['hits']['total']  # responses/0/hits/total
                return_list.extend(response_data['responses'][hit_index]['hits']['hits'])
            except KeyError: pass
            except IndexError: pass
            if value is not None and value > SEARCH_SPLIT_BUCKET_LIMIT:
                logger.warning('Search split {} has {} hit-results which exceeds the {} limit, '
                               'results truncated!'.format(hit_index, value, SEARCH_SPLIT_BUCKET_LIMIT))
            hit_total = hit_total + value

        hit_count = len(return_list)
        logger.info('{} available-hits; {} returned-hits; {} average-hits-per-split; {} msearch-splits'.
                    format(hit_total, hit_count, int(hit_total/splits), splits))

        if self.connection.internal_proxy:
            time.sleep(0.1)  # allows internal_proxy threads to close-out

        return return_list

    def __payload_header(self, index):
        return json.dumps({
            'index': index,
            'ignore_unavailable': True,
            'preference': int(round(time.time() * 1000))
        })

    def __payload_body(self, query_params, size=SEARCH_SPLIT_BUCKET_LIMIT, source=None):

        if size > SEARCH_SPLIT_BUCKET_LIMIT or size < 1:
            raise ElasticsearchKibanaCLIException('Payload size is out-of-bounds in __parse_query_param()', size)

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
            'size': size,
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
                    raise ElasticsearchKibanaCLIException('Unsupported type in __parse_query_param()', param_query_item)
        return query

    def __parse_query_timestamp(self, element):
        if type(element) in [int, str, bool] or element is None:
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
            raise ElasticsearchKibanaCLIException('Unsupported type in __parse_query_timestamp()', element)

    def __payload_range_splitter(self, ndjson_payload, range_keyword='range'):

        return_payloads = OrderedDict()
        for index, json_payload in enumerate(ndjson_payload.split('\n')):
            if len(json_payload) > 0:
                return_payloads[index] = json.loads(json_payload)

        payload_ranges = OrderedDict()
        for payload_k, payload_v in return_payloads.items():
            for payload_tupple in dpath.util.search(payload_v, '**/{}'.format(range_keyword), yielded=True):
                payload_ranges[payload_k] = payload_tupple

        # check the range paths are the same
        payload_range_path = None
        payload_range_path_key = None
        for payload_range_k, payload_range_value in payload_ranges.items():
            if payload_range_path is None:
                payload_range_path, payload_range_path_value = payload_range_value
                payload_range_path_key = next(iter(payload_range_path_value.keys()))
            else:
                payload_range_path_next, payload_range_path_next_value = payload_range_value
                payload_range_path_next_key = next(iter(payload_range_path_next_value.keys()))
                if payload_range_path_next != payload_range_path:
                    raise ElasticsearchKibanaCLIException('Ranges with different paths in __payload_range_splitter()')
                if payload_range_path_next_key != payload_range_path_key:
                    raise ElasticsearchKibanaCLIException('Ranges with different internal keys in __payload_range_splitter()')

        # determine the min max values within the discovered range definitions
        min = max = None
        limit_keys = []
        for range_key in payload_ranges.keys():
            range_values = dpath.util.get(
                return_payloads,
                '{}/{}/{}'.format(range_key, payload_range_path, payload_range_path_key)
            )
            for range_value_key, range_value_value in range_values.items():
                if range_value_key.lower() in ['gt','gte','lt','lte']:
                    if min is None:
                        min = range_value_value
                    elif range_value_value < min:
                        min = range_value_value
                    if max is None:
                        max = range_value_value
                    elif range_value_value > max:
                        max = range_value_value
                    if range_value_key not in limit_keys:
                        limit_keys.append(range_value_key)

        def split_min_max_delta(min_max_delta, num_of_parts):
            part_duration = int(min_max_delta / num_of_parts)
            parts = []
            marker = 0
            for _ in range(num_of_parts):
                part = [marker, marker + part_duration]
                marker += part_duration
                parts.append(part)
            parts[len(parts)-1][1] = min_max_delta  # rewrite final value so it correctly lines up
            return parts

        splits = split_min_max_delta(int(max-min), len(payload_ranges.keys()))

        splits_index = 0
        for range_key in payload_ranges.keys():
            for limit_key in limit_keys:

                if splits_index == 0 and 'gt' in limit_key.lower():
                    dpath.util.set(
                        return_payloads,
                        '{}/{}/{}/{}'.format(range_key, payload_range_path, payload_range_path_key, limit_key),
                        (min + splits[splits_index][0])
                    )

                elif 'gt' in limit_key.lower():
                    dpath.util.delete(
                        return_payloads,
                        '{}/{}/{}/{}'.format(range_key, payload_range_path, payload_range_path_key, limit_key)
                    )
                    dpath.util.new(
                        return_payloads,
                        '{}/{}/{}/gte'.format(range_key, payload_range_path, payload_range_path_key),
                        (min + splits[splits_index][0])
                    )

                elif splits_index == len(splits)-1 and 'lt' in limit_key.lower():
                    dpath.util.set(
                        return_payloads,
                        '{}/{}/{}/{}'.format(range_key, payload_range_path, payload_range_path_key, limit_key),
                        (min + splits[splits_index][1])
                    )

                elif 'lt' in limit_key.lower():
                    dpath.util.delete(
                        return_payloads,
                        '{}/{}/{}/{}'.format(range_key, payload_range_path, payload_range_path_key, limit_key)
                    )
                    dpath.util.new(
                        return_payloads,
                        '{}/{}/{}/lt'.format(range_key, payload_range_path, payload_range_path_key),
                        (min + splits[splits_index][1])
                    )

                else:
                    raise ElasticsearchKibanaCLIException('Unsupported limit key in __payload_range_splitter()', limit_key)

            splits_index += 1

        # re-cast back into ndjson_payload format
        ndjson_return_payload = ''
        for return_payloads_k, return_payloads_v in return_payloads.items():
            ndjson_return_payload = '{}{}\n'.format(ndjson_return_payload, json.dumps(return_payloads_v))

        # logger.debug(ndjson_return_payload)
        return ndjson_return_payload
