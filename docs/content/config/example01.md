# Elasticsearch Kibana CLI

## Example 01
The example below shows an Elasticsearch Kibana CLI (`eskbcli`) configuration for a search definition with the
name `example01-query-string` in the following way -

* Direct queries to Kibana at `https://kibana.awesome-company.internal`
* Use an `internal_proxy` arrangement to override the `cookie` http-header with the environment value from `GCP_IAP_COOKIE`
* Name the search definition `example01-query-string`; multiple search definitions with unique names may exist in the same file. 
* Perform a search against indexes with names that match `logstash-rest-*`
* Split the search up into 100x smaller searches (based on the `range` provided); this is done to manage Kibana result-count limits which are often set to 10k results.   
* Return the fields `user_agent`, `remote_ip`, and `http_status` only.
* Search results `must` be within timestamps in the past 30 minutes and match the query string value.

```yaml
elasticsearch_kibana_cli:

  base_uri: https://kibana.awesome-company.internal

  internal_proxy:
    debug: false
    header_overrides:
      cookie: env:GCP_IAP_COOKIE

  search_definitions:

    example01-query-string:

      index: logstash-rest-*
      splits: 100

      source:
        - "user_agent"
        - "remote_ip"
        - "http_status"

      search:
        must:
          range:
            @timestamp:
              'lte': 'now'
              'gte': '-30m'
          query_string:
            - query: "type:auth AND http_status:429 AND user_agent:curl*"
```

Download example01 [here](https://github.com/ndejong/elasticsearch_kibana_cli/raw/master/config-examples/example01.yml)
