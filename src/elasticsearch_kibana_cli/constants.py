from . import __version__

TITLE = "elasticsearch_kibana_cli"
AUTHOR = "Nicholas de Jong <contact@nicholasdejong.com>"
VERSION = __version__
LICENSE = "BSD2"
CLI_NAME = "eskbcli"

CONFIG_FILE_DEFAULT = "~/.eskbcli"
CONFIG_FILENAME_ENV = "ESKBCLI_CONFIG_FILENAME"

SEARCH_SPLIT_COUNT_DEFAULT = 10
SEARCH_SPLIT_BUCKET_LIMIT = 10000
SEARCH_TIMEOUT_SECONDS_DEFAULT = 120
SUMMARY_TOP_COUNT_DEFAULT = 3
