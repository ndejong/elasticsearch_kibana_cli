# Elasticsearch Kibana CLI

## Summary Usage
```shell
Usage: eskbcli summary [OPTIONS] FILENAME

  Summary report for search result datafile; use "-" to pipe stdin.

Options:
  -o, --out TEXT  Filename to write output.  [default: stdout]
  --help          Show this message and exit.
```

### Example #1 - read file
Create a summary report on a previous `search` output file at `/tmp/outputfile.json`
```shell
eskbcli summary /tmp/outputfile.json
```

### Example #2 - pipe input
Create a summary report on a search-datafile `/tmp/outputfile.json` piped in via `cat`.
```shell
cat /tmp/outputfile.json | eskbcli summary - 
```
