# Elasticsearch Kibana CLI

## Search Usage
```shell
Usage: eskbcli search [OPTIONS] [SEARCH_NAME]

  Execute the named search configuration.

Options:
  -o, --out TEXT              Filename to write output.  [default: stdout]
  -S, --summary               Generate summary report and output to stderr
                              with the default summary-top count.  
                              [default: False]
  -ST, --summary-top INTEGER  Depth of the top-count summary to produce.
                              [default: 3]
  -s, --splits INTEGER        Number of splits to break search into.
                              [default: 10]
  -np, --no-ping              Do not ping the Kibana endpoint before using the
                              connection.  [default: False]
  --help                      Show this message and exit.
```

### Example #1 - default
Search using the `example01-query-string` definition in the default `~/.eskbcli` 
configuration file
```shell
eskbcli search example01-query-string
```

### Example #2 - config file with named search definition
Use the `--config` file located at `~/project/eskbcli-foobar.yml` and search 
using the `example01-query-string` definition
```shell
eskbcli -c ~/project/eskbcli-foobar.yml search example01-query-string
```

### Example #3 - config file with single search definition
Use the `--config` file located at `~/project/eskbcli-foobar.yml` and search 
using the single search definition within that configuration.  NB This only works when 
there is a single search definition within the configuration file.
```shell
eskbcli -c ~/project/eskbcli-foobar.yml search
```

### Example #4 - output filename
Search using the `example01-query-string` definition in the default `~/.eskbcli` 
configuration file and `--out` to filename `/tmp/outputfile.json`
```shell
eskbcli search example01-query-string -o /tmp/outputfile.json
```

### Example #5 - summary report (default depth)
Search using the `example01-query-string` definition in the default `~/.eskbcli` 
configuration file and write to STDERR the `--summary` report.
```shell
eskbcli search example01-query-string -S
```

### Example #6 - summary report with report depth 10
Search using the `example01-query-string` definition in the default `~/.eskbcli` 
configuration file and write to STDERR the `--summary-top` report.
```shell
eskbcli search example01-query-string -ST 10
```

### Example #7 - verbose logging
Provide `--verbose` logging messages when searching the `example01-query-string` 
definition in the default `~/.eskbcli` configuration file
```shell
eskbcli -v search example01-query-string
```
