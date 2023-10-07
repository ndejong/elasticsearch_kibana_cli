import os
import tempfile

from elasticsearch_kibana_cli import constants
from elasticsearch_kibana_cli.main import ElasticsearchKibanaInterface


def test_version_exist():
    assert constants.VERSION is not None


def test_title_exist():
    assert constants.TITLE is not None


def test_list_searches():
    config_filename = __faux_config_file()
    ls = ElasticsearchKibanaInterface(config_filename=config_filename).list_searches()
    os.unlink(config_filename)
    assert "test01" in ls


def test_show_search():
    config_filename = __faux_config_file()
    ss = ElasticsearchKibanaInterface(config_filename=config_filename).show_search(name="test01")

    os.unlink(config_filename)
    assert "splits" in ss.keys()
    assert ss["splits"] == 5


def __faux_config_file(filename=None):
    if filename is None:
        filename = tempfile.mktemp()

    faux_config = """
elasticsearch_kibana_cli:
  base_uri: http://127.0.0.1
  search_definitions:
    test01:
      index: test
      size: 10
      splits: 5
      source:
      search:
    """

    with open(filename, "w") as f:
        f.write(faux_config)
    return filename
