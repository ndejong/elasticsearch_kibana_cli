# Elasticsearch Kibana CLI

## Show Usage
```shell
Usage: eskbcli show [OPTIONS] SEARCH_NAME

  Show the named eskbcli search configuration.

Options:
  -o, --out TEXT  Filename to write output.  [default: stdout]
  --help          Show this message and exit.
```

### Example #1 - default
Show search configuration for the `example01-query-string` definition in the 
default `~/.eskbcli` configuration file
```shell
eskbcli show example01-query-string
```

### Example #2 - config file with named search definition
Read the `--config` file located at `~/project/eskbcli-foobar.yml` and show
the search definition for `example01-query-string`
```shell
eskbcli -c ~/project/eskbcli-foobar.yml show example01-query-string
```

### Example #3 - config file with single search definition
Read the `--config` file located at `~/project/eskbcli-foobar.yml` and show
the only search definition within the configuration.
```shell
eskbcli -c ~/project/eskbcli-foobar.yml show
```
