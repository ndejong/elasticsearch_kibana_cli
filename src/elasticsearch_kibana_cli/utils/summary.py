
from collections.abc import MutableMapping

from elasticsearch_kibana_cli import __title__ as NAME
from elasticsearch_kibana_cli.utils.logger import Logger
from elasticsearch_kibana_cli import __summary_top_count_default__ as SUMMARY_TOP_COUNT_DEFAULT


logger = Logger(name=NAME).logging


class ElasticsearchKibanaCLISummary:

    def __init__(self):
        pass

    def summary(self, data, data_key='_source', top_count=None):

        if top_count is None:
            top_count = SUMMARY_TOP_COUNT_DEFAULT

        summary_data = {}

        for record in data:
            if type(record) is dict and data_key in record.keys():
                flat_record = self.flatten_dict(record['_source'])
                for record_key, record_value in flat_record.items():
                    if record_key not in summary_data.keys():
                        summary_data[record_key] = {}
                    if record_value not in summary_data[record_key].keys():
                        summary_data[record_key][record_value] = 1
                    else:
                        summary_data[record_key][record_value] += 1

        summary_report = {}
        for summary_data_key, summary_data_value in summary_data.items():
            top_sorted = {}
            top_sorted_index = 0
            for top_sorted_item in sorted(summary_data_value.items(), key=lambda kv: kv[1], reverse=True):
                if top_sorted_index < top_count:
                    top_sorted[top_sorted_item[0]] = top_sorted_item[1]
                    top_sorted_index += 1
                elif '_other_' in top_sorted.keys():
                    top_sorted['_other_'] = top_sorted['_other_'] + top_sorted_item[1]
                else:
                    top_sorted['_other_'] = top_sorted_item[1]
            summary_report[summary_data_key] = top_sorted
        return summary_report

    def flatten_dict(self, d: MutableMapping, parent_key: str = '', sep: str = '.'):
        return dict(self._flatten_dict_gen(d, parent_key, sep))

    def _flatten_dict_gen(self, d, parent_key, sep):
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, MutableMapping):
                yield from self.flatten_dict(v, new_key, sep=sep).items()
            else:
                yield new_key, v
