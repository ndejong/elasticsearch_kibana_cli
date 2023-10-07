# Elasticsearch Kibana CLI (eskbcli)
[![PyPi](https://img.shields.io/pypi/v/elasticsearch-kibana-cli.svg)](https://pypi.python.org/pypi/elasticsearch-kibana-cli/)
[![Python Versions](https://img.shields.io/pypi/pyversions/elasticsearch-kibana-cli.svg)](https://github.com/ndejong/elasticsearch_kibana_cli/)
[![Read the Docs](https://img.shields.io/readthedocs/elasticsearch-kibana-cli)](https://elasticsearch-kibana-cli.readthedocs.io)
![License](https://img.shields.io/github/license/ndejong/elasticsearch_kibana_cli.svg)

!!! danger
    ElasticSearch Kibana CLI relies on the availability of a
    `/elasticsearch/_msearch` API endpoint exposed through Kibana.
    Recent versions (v8.??) of Kibana appear to have removed this API 
    endpoint rendering this utility no longer functional.
    C'est la vie, `eskbcli` has served well but no longer.

ElasticSearch Kibana CLI (`eskbcli`) provides a shell interface to query
an ElasticSearch backend via the Kibana frontend which is useful in
situations where the ElasticSearch backend is not otherwise accessible.

ElasticSearch Kibana CLI makes it possible to copy-paste query expressions
directly from the Kibana user-interface and then easily access very large
sets of result data.  This makes the `eskbcli` useful in SecOps situations
where the ability to rapidly move from a Kibana query to raw data is
valued.

Configuration options are available to adjust http-headers so-as-to enable
access to Kibana in situations that require complex user-authentication
such as when Kibana exists behind an OAuth reverse proxy or other session-
based authentication arrangement.

## Install / Upgrade
```shell
user@computer:~$ pip install [--upgrade] elasticsearch-kibana-cli
```


## Documentation
Documentation is available at [elasticsearch-kibana-cli.readthedocs.io](https://elasticsearch-kibana-cli.readthedocs.io)

### Usage
* [Search](https://elasticsearch-kibana-cli.readthedocs.io/en/latest/usage/search) - Execute the named search configuration.
* [Summary](https://elasticsearch-kibana-cli.readthedocs.io/en/latest/usage/summary) - Summary report for search result datafile; use "-" to pipe stdin.
* [Show](https://elasticsearch-kibana-cli.readthedocs.io/en/latest/usage/show) - Show the named eskbcli search configuration.
* [List](https://elasticsearch-kibana-cli.readthedocs.io/en/latest/usage/list) - List the available eskbcli search names.

### Config Files
Refer to the worked example [config files](https://elasticsearch-kibana-cli.readthedocs.io/en/latest/config/) 
with descriptions and details.

## Project
* Github - [github.com/ndejong/elasticsearch_kibana_cli](https://github.com/ndejong/elasticsearch_kibana_cli)
* PyPI - [pypi.python.org/pypi/elasticsearch-kibana-cli](https://pypi.python.org/pypi/elasticsearch-kibana-cli/)
* ReadTheDocs - [elasticsearch-kibana-cli.readthedocs.io](https://elasticsearch-kibana-cli.readthedocs.io)

---
Copyright &copy; 2021-2023 [Nicholas de Jong](https://wwww.nicholasdejong.com)
