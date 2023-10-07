# Elasticsearch Kibana CLI

## Usage
* [Search](search) - Execute the named search configuration.
* [Summary](summary) - Summary report for search result datafile; use "-" to pipe stdin.
* [Show](show) - Show the named eskbcli search configuration.
* [List](list) - List the available eskbcli search names.

## Synopsis
```text
Usage: eskbcli [OPTIONS] COMMAND [ARGS]...

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

  Documentation available https://elasticsearch-kibana-cli.readthedocs.io

Options:
  -c, --config TEXT  Config file location; overrides ESKBCLI_CONFIG_FILENAME
                     environment var and the default ~/.eskbcli value.

  -v, --verbose      Verbose logging messages (debug level).
  -q, --quiet        Quiet mode, takes priority over --verbose
  --version          Show the version and exit.
  --help             Show this message and exit.

Commands:
  list     List the available eskbcli search names.
  search   Execute the named search configuration.
  show     Show the named eskbcli search configuration.
  summary  Summary report for search result datafile; use "-" to pipe stdin.
```