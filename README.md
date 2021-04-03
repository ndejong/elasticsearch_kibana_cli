# Elasticsearch Kibana CLI (eskbcli)
[![PyPi](https://img.shields.io/pypi/v/elasticsearch-kibana-cli.svg)](https://pypi.python.org/pypi/elasticsearch-kibana-cli/)
[![Python Versions](https://img.shields.io/pypi/pyversions/elasticsearch-kibana-cli.svg)](https://github.com/ndejong/elasticsearch-kibana-cli/)
[![Build Status](https://api.travis-ci.org/ndejong/elasticsearch_kibana_cli.svg?branch=master)](https://travis-ci.org/ndejong/elasticsearch_kibana_cli/)
[![Read the Docs](https://img.shields.io/readthedocs/elasticsearch-kibana-cli)](https://elasticsearch-kibana-cli.readthedocs.io)
![License](https://img.shields.io/github/license/ndejong/elasticsearch_kibana_cli.svg)

ElasticSearch Kibana CLI (`eskbcli`) provides a shell interface to query an ElasticSearch backend via 
the Kibana frontend which is useful in situations where the ElasticSearch backend is not otherwise 
accessible.

ElasticSearch Kibana CLI makes it possible to copy-paste query expressions directly from the Kibana 
user-interface and then easily access very large sets of result data.  This makes the `eskbcli` useful 
in SecOps situations where the ability to rapidly move from a Kibana query to raw data is valued. 

Configuration options are available to adjust http-headers so-as-to enable access to Kibana in 
situations that require complex user-authentication such as when Kibana exists behind an OAuth 
reverse proxy or other session-based authentication arrangement.

Documentation available https://elasticsearch-kibana-cli.readthedocs.io

## Installation
```shell
user@computer:~$ pip3 install elasticsearch-kibana-cli
```

## Sample Configurations
Sample configurations can be found in the [GitHub repo](https://github.com/ndejong/elasticsearch_kibana_cli) 
or at https://elasticsearch-kibana-cli.readthedocs.io

## Project
* Github - [github.com/ndejong/elasticsearch_kibana_cli](https://github.com/ndejong/elasticsearch_kibana_cli)
* PyPI - [pypi.python.org/pypi/elasticsearch-kibana-cli](https://pypi.python.org/pypi/elasticsearch-kibana-cli/)
* TravisCI - [travis-ci.org/github/ndejong/elasticsearch_kibana_cli](https://travis-ci.org/github/ndejong/elasticsearch_kibana_cli)
* ReadTheDocs - [elasticsearch-kibana-cli.readthedocs.io](https://elasticsearch-kibana-cli.readthedocs.io)

---
Copyright &copy; 2020 Nicholas de Jong
