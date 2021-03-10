
import os
import tempfile
from elasticsearch_kibana_cli import ElasticsearchKibanaCLI


def test_version_exist():
    assert ElasticsearchKibanaCLI.VERSION is not None


def test_name_exist():
    assert ElasticsearchKibanaCLI.NAME is not None


def test_search_definitions(capfd):
    config_filename = __faux_config_file()
    os.environ['ELASTICSEARCHKIBANACLI_CONFIG_FILENAME'] = config_filename
    ElasticsearchKibanaCLI.ElasticsearchKibanaCLI(debug=True).search_definitions()
    stdout, stderr = capfd.readouterr()
    os.unlink(config_filename)
    assert 'test01' in stdout
    assert config_filename in stderr


# TODO: add more tests with deeper coverage


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

    with open(filename, 'w') as f:
        f.write(faux_config)
    return filename
