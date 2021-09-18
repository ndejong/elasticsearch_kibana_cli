# Elasticsearch Kibana CLI

## Search Usage
```shell
Usage: eskbcli search [OPTIONS] SEARCH_NAME

  Execute the named search configuration.

Options:
  -o, --out TEXT        Filename to write output.  [default: stdout]
  -S, --summary         Generate summary report and output to stderr
                        [default: False]
  -s, --splits INTEGER  Number of splits to break search into.  [default: 10]
  -np, --no-ping        Do not ping the Kibana endpoint before using the
                        connection.  [default: False]
  --help                Show this message and exit.
```

### Example #1 - default
Search using the `example01-query-string` definition in the default `~/.eskbcli` 
configuration file
```shell
eskbcli search example01-query-string
```

### Example #2 - config file
Use the `--config` file located at `~/project/eskbcli-foobar.yml` and search 
using the `example01-query-string` definition
```shell
eskbcli -c ~/project/eskbcli-foobar.yml search example01-query-string
```

### Example #3 - output filename
Search using the `example01-query-string` definition in the default `~/.eskbcli` 
configuration file and `--out` to filename `/tmp/outputfile.json`
```shell
eskbcli search example01-query-string -o /tmp/outputfile.json
```

### Example #4 - summary report
Search using the `example01-query-string` definition in the default `~/.eskbcli` 
configuration file and write to STDERR the `--summary` report.
```shell
eskbcli search example01-query-string -S -o /tmp/outputfile.json
```

### Example #5 - verbose logging
Provide `--verbose` logging messages when searching the `example01-query-string` 
definition in the default `~/.eskbcli` configuration file
```shell
eskbcli -v search example01-query-string
```
