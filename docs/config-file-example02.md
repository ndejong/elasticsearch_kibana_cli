# Elasticsearch Kibana CLI

## Config File Example 02
The example below shows an Elasticsearch Kibana CLI (`eskbcli`) configuration for a search definition with the
name `example02-match-operators` in the following way -
* Direct queries to Kibana at `https://kibana.internal`
* Name the search definition `eexample02-match-operators` 
* Perform a search against indexes with names that match `logstash-api-*`
* Split the search up into 20x smaller searches (based on the `range` provided); this is done to manage Kibana result-count limits which are often set to 10k results.
* Return all fields because the `source` definition is not set.
* Search results `must` be within the supplied timestamps (with timezones)
* Search results `must` match the `hostname: "api.*"` and `path: "\\/v1\\/user\\/auth"` qualifiers; notice the requirement for the double-backslash 
* Search results `must_not` match the `geoip.country_name: "Australia"` qualifier.

```yaml
elasticsearch_kibana_cli:

  base_uri: https://kibana.internal

  search_definitions:

    example02-match-operators:

      index: logstash-api-*
      splits: 20

      search:
        must:
          range:
            @timestamp:
              'lte': '2021-04-01 04:17:15.126 AEST'
              'gte': '2021-04-01 01:22:00.555 AEST'
          match:
            - hostname: "api.*"
            - path: "\\/v1\\/user\\/auth"
        must_not:
          match:
            - geoip.country_name: "Australia"
```

Download example02 [here](https://github.com/ndejong/elasticsearch_kibana_cli/raw/master/config-examples/example02.yml)
