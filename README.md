# Elasticsearch Kibana CLI

The Elasticsearch Kibana CLI provides a configurable programatic interface to
query the Elasticsearch backend via the Kibana frontend which is useful in
situations where the Elasticsearch backend is not otherwise accessible.
Configuration options are available that permit HTTP request header overrides
that hence enable access to Kibana in situations that require additional
authentication such as when Kibana is behind an OAuth reverse proxy.

### Github
* [github.com/ndejong/elasticsearch_kibana_cli](https://github.com/ndejong/elasticsearch_kibana_cli)

### Prerequisites

### Environment Variables

### Outputs

### Example: 

### Example: 

### Example: 

### Usage
```
usage: eskbcli [-c <filename>] [-s <search>] [-h <hits>] [-p]
               [-k <kbn_version>] [-D] [-d]

Elasticsearch Kibana CLI

optional arguments:
  -c <filename>     Configuration file to use, use this if the eskbcli.yml is
                    not be automatically located.
  -s <search>       The search_definition name from configuration to use and
                    execute
  -h <hits>         Search hit count limit, overrides the config value if set
                    min=1, max=10000 (default:10000)
  -p                Ping the Kibana endpoint before using this connection
                    (default: False)
  -k <kbn_version>  Kibana version override, useful in various debugging
                    situations
  -D                List the configured search_definitions in config and
                    immediately exit
  -d                Debug level logging output (default: False)

The Elasticsearch Kibana CLI provides a configurable programatic interface to
query the Elasticsearch backend via the Kibana frontend which is useful in
situations where the Elasticsearch backend is not otherwise accessible.
Configuration options are available that permit HTTP request header overrides
that hence enable access to Kibana in situations that require additional
authentication such as when Kibana is behind an OAuth reverse proxy.
```

****

## Authors
[Nicholas de Jong](https://nicholasdejong.com)

## License
BSD-2-Clause - see LICENSE file for full details.
