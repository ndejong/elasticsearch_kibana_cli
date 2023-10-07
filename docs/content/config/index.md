# Elasticsearch Kibana CLI

## Config Files
Elasticsearch Kibana CLI (`eskbcli`) configuration files are YAML format files that define; the Kibana 
endpoint address; an optional internal proxy allowing http-header overrides; and the search definitions
to use at the Kibana frontend.

NB: all Elasticsearch Kibana CLI configurations *MUST* have an `elasticsearch_kibana_cli:` top-level root.

Three options exist for setting the configuration file; in order of precedence -

 1. Setting the `--config` command line argument at runtime.
 2. Setting the `ESKBCLI_CONFIG_FILENAME` shell environment variable.
 3. Saving the configuration in the user-path `~/.eskbcli`

## Examples
 * [Example01](example01)
 * [Example02](example02)
