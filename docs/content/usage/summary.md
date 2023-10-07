# Elasticsearch Kibana CLI

## Summary Usage
```shell
Usage: eskbcli summary [OPTIONS] FILENAME

  Summary report for search result datafile; use "-" to pipe stdin.

Options:
  -t, --top INTEGER  Depth of the top-count summary to produce.  [default: 3]
  -o, --out TEXT     Filename to write output.  [default: stdout]
  --help             Show this message and exit.
```

### Read file
Create a summary report to `stdout` on a previous `search` search output-datafile at 
`/tmp/outputfile.json`
```shell
eskbcli summary /tmp/outputfile.json
```

### Pipe input
Create a summary report to `stdout` on a search output-datafile `/tmp/outputfile.json` 
piped in via `stdin` using the `cat` command.
```shell
cat /tmp/outputfile.json | eskbcli summary - 
```

### Extended summary report depth
Create a summary report to `stdout` showing the `--top` 12x results on a previous 
search output-datafile `/tmp/outputfile.json`
```shell
eskbcli summary -t 12 /tmp/outputfile.json
```
