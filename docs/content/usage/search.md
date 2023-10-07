# Elasticsearch Kibana CLI

## Search Usage

```text
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

### Default
Search using the `example01-query-string` definition in the default `~/.eskbcli` 
configuration file
```shell
eskbcli search example01-query-string
```

### Config file with named search definition
Use the `--config` file located at `~/project/eskbcli-foobar.yml` and search 
using the `example01-query-string` definition
```shell
eskbcli -c ~/project/eskbcli-foobar.yml search example01-query-string
```

### Config file with single search definition
Use the `--config` file located at `~/project/eskbcli-foobar.yml` and search 
using the single search definition within that configuration.  NB This only works when 
there is a single search definition within the configuration file.
```shell
eskbcli -c ~/project/eskbcli-foobar.yml search
```

### Output filename
Search using the `example01-query-string` definition in the default `~/.eskbcli` 
configuration file and `--out` to filename `/tmp/outputfile.json`
```shell
eskbcli search example01-query-string -o /tmp/outputfile.json
```

### Summary report (default depth)
Search using the `example01-query-string` definition in the default `~/.eskbcli` 
configuration file and write to STDERR the `--summary` report.
```shell
eskbcli search example01-query-string -S
```

### Summary report with report depth 10
Search using the `example01-query-string` definition in the default `~/.eskbcli` 
configuration file and write to STDERR the `--summary-top` report.
```shell
eskbcli search example01-query-string -ST 10
```

### Verbose logging
Provide `--verbose` logging messages when searching the `example01-query-string` 
definition in the default `~/.eskbcli` configuration file
```shell
eskbcli -v search example01-query-string
```
