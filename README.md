# Elasticsearch Kibana CLI

[![PyPi](https://img.shields.io/pypi/v/elasticsearch-kibana-cli.svg)](https://pypi.org/project/elasticsearch-kibana-cli/)
[![Build Status](https://api.travis-ci.org/ndejong/elasticsearch_kibana_cli.svg?branch=master)](https://api.travis-ci.org/ndejong/elasticsearch_kibana_cli)

The Elasticsearch Kibana CLI provides a configurable shell interface to
query the Elasticsearch backend via the Kibana frontend which is useful in
situations where the Elasticsearch backend is not otherwise accessible.
Configuration options are available that permit HTTP request header overrides
that hence enable access to Kibana in more complex situations that may require
additional authentication such as when Kibana is behind an OAuth reverse
proxy.

## Project
* [github.com/ndejong/elasticsearch_kibana_cli](https://github.com/ndejong/elasticsearch_kibana_cli)

## Install
#### via PyPi
```bash
pip3 install elasticsearch-kibana-cli
```

#### via Source
```bash
git clone https://github.com/ndejong/elasticsearch_kibana_cli
cd elasticsearch_kibana_cli
python3 -m venv venv
./venv/bin/activate
pip3 install -r requirements.txt
```

## Configuration
The provided `eskbcli-sample.yml` demonstrates the configuration options available to create 
search_definitions.  Under the hood, query strings are generated using the `Q` function from the
standard [elasticsearch-dsl](https://elasticsearch-dsl.readthedocs.io/en/latest/) Python library from 
Elastic.  The `search` configuration parameter is loaded into the `Q` function wrapped within a `bool` 
and honours the `must`, `must_not`, `should`, `should_not` and `filter` attributes.

By example therefore, where a Python elasticsearch-dsl expression is written as such
```python
s.query = Q('bool', must=[Q('match', title='python'), Q('match', body='best')])
```

then the YML configuration equivalent is therefore
```yaml
  search:
    must:
      match:
        - title: "python"
        - body: "best"
```  

This enables the user to define most forms of Elastic Search query in an Elastic standard way.

## Environment Variables

#### Standard Environment Variables
The following environment variables are available

* `ELASTICSEARCHKIBANACLI_CONFIG_FILENAME` alternative method to set or override the configuration 
   file to be loaded.  Has same effect as setting the `-c` argument.

* `ELASTICSEARCHKIBANACLI_LOGLEVEL` adjust the level of logging output to stderr.  Valid settings are
  `CRITICAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG`


#### Configuration Import Environment Variables
Loading environment variables into the configuration is possible using the env name with an 
`env:` prefix, for example
```yaml
    header_overrides:
      cookie: env:GCP_IAP_COOKIE
``` 
In this case the HTTP header override configuration value gets loaded from the `GCP_IAP_COOKIE` env value.


## Usage
```
usage: eskbcli [-s <search>] [-o <filename>] [-sc <split-count>]
               [-hc <hit-count>] [-np] [-D] [-k <kbn_version>] [-c <filename>]
               [-d]

Elasticsearch Kibana CLI v0.1.0

optional arguments:
  -s <search>        The search_definition name from configuration to use and
                     execute (hint: use -D to list).
  -o <filename>      Filename to write output to, by default output it written
                     to stdout.
  -sc <split-count>  Number of splits to break the search into, overrides the
                     config value if set (default:1).
  -hc <hit-count>    Search hit count limit, overrides the config value if set
                     min=1, max=10000 (default:10000).
  -np, --noping      Do not ping the Kibana endpoint before using this
                     connection (default: False).
  -D, --defn         List the configured search_definitions sections in the
                     config and immediately exit.
  -k <kbn_version>   Kibana version override, useful in some debugging
                     situations.
  -c <filename>      Override the configuration file to read, else search for
                     eskbcli.yml in common paths.
  -d, --debug        Debug level logging output (default: False).

The Elasticsearch Kibana CLI provides a configurable shell interface to
query the Elasticsearch backend via the Kibana frontend which is useful in
situations where the Elasticsearch backend is not otherwise accessible.
Configuration options are available that permit HTTP request header overrides
that hence enable access to Kibana in more complex situations that may require
additional authentication such as when Kibana is behind an OAuth reverse
proxy.
```

## Example

```bash
$ eskbcli -d -sc 10 -s example01 -o /tmp/example01.json
20190922Z024453 - INFO - elasticsearch_kibana_cli
20190922Z024453 - INFO - version 0.1.0
20190922Z024453 - INFO - Loaded configuration filename /etc/eskbcli/eskbcli.yml
20190922Z024453 - DEBUG - Using internal_proxy to connect https://kibana.internal
20190922Z024454 - DEBUG - kbn_metadata read from cache file /tmp/elasticsearch_kibana_cli-connection-6140f131-metadata.cache
20190922Z024454 - DEBUG - Connection definition setup http://127.0.0.1:59200
20190922Z024500 - INFO - Ping okay http://127.0.0.1:59200
20190922Z024501 - INFO - Search split into 10 requests based on "range" keyword
20190922Z024502 - INFO - 2905 available-hits; 2905 returned-hits; 290 average-hits-per-split; 10 msearch-splits
```

****

## Authors
[Nicholas de Jong](https://nicholasdejong.com)

## License
BSD-2-Clause - see LICENSE file for full details.
