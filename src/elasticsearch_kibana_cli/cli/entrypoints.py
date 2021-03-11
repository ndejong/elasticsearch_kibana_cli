
import os
import argparse
from signal import signal, SIGINT

from elasticsearch_kibana_cli import __title__ as NAME
from elasticsearch_kibana_cli import __version__ as VERSION
from elasticsearch_kibana_cli.exceptions.ElasticsearchKibanaCLIException import ElasticsearchKibanaCLIException


def sigint_handler(signal_received, frame):
    print('SIGINT received, exiting.')
    exit(0)


def eskbcli():
    signal(SIGINT, sigint_handler)
    from elasticsearch_kibana_cli.ElasticsearchKibanaCLI import ElasticsearchKibanaCLI

    parser = argparse.ArgumentParser(
        description='{} v{}'.format(NAME, VERSION),
        add_help=False,
        epilog="""
            The Elasticsearch Kibana CLI provides a configurable shell interface to query the Elasticsearch backend 
            via the Kibana frontend which is useful in situations where the Elasticsearch backend is not otherwise 
            accessible. Configuration options are available that permit HTTP request header overrides that hence enable 
            access to Kibana in more complex situations that may require additional authentication such as when Kibana 
            exists behind an OAuth reverse proxy or other zero-trust-network environment.
        """,
    )

    # Note to self: consider click-cli arrangement for release args
    #
    #   eskbcli -v -c <config_file> list
    #   eskbcli -v -c <config_file> search <search_name>
    #   eskbcli -v -c <config_file> -o <output_file> search <search_name>
    #
    #   eskbcli -v -c <config_file> search -sc <split_count> <search_name>
    #   eskbcli -v -c <config_file> search -np <search_name>
    #   eskbcli -v -c <config_file> search -k <kibana_version> <search_name>

    parser.add_argument('-s', type=str, metavar='<search>', default=None,
                        help='The search_definition name from configuration to use and execute (hint: use -D to list).')

    parser.add_argument('-o', type=str, metavar='<filename>', default=None,
                        help='Filename to write output to, by default output it written to stdout.')

    parser.add_argument('-sc', type=int, metavar='<split-count>', default=None,
                        help='Number of splits to break the search into, overrides the config value if set (default:1).')

    parser.add_argument('-hc', type=int, metavar='<hit-count>', default=None,
                        help='Search hit count limit, overrides the config value if set min=1, max=10000 (default:10000).')

    parser.add_argument('-np', '--noping', action='store_true', default=False,
                        help='Do not ping the Kibana endpoint before using this connection (default: False).')

    parser.add_argument('-D', '--defn', action='store_true', default=False,
                        help='List the configured search_definitions sections in the config and immediately exit.')

    parser.add_argument('-k', type=str, metavar='<kbn_version>', default=None,
                        help='Kibana version override, useful in some debugging situations.')

    parser.add_argument('-c', type=str, metavar='<filename>', default=None,
                        help='Override the configuration file to read, else search for eskbcli.yml in common paths.')

    parser.add_argument('-d', '--debug', action='store_true', default=False,
                        help='Debug level logging output (default: False).')

    args = parser.parse_args()
    if args.s is None and args.defn is False:
        parser.print_help()
        exit(1)

    if args.c is not None:
        config_filename_env_override = '{}_CONFIG_FILENAME'.format(
            NAME.replace('_', '').replace(' ', '').upper()
        )
        os.environ[config_filename_env_override] = args.c

    try:
        if args.defn is True:
            ElasticsearchKibanaCLI(output_filename=args.o, debug=args.debug).search_definitions()
        else:
            try:
                ElasticsearchKibanaCLI(output_filename=args.o, debug=args.debug).msearch(
                    search_definition=args.s,
                    hit_count=args.hc,
                    split_count=args.sc,
                    ping_connection=True if args.noping is False else False,
                    kbn_version=args.k,
                )
            except KeyboardInterrupt:
                pass

    except ElasticsearchKibanaCLIException as e:
        print('')
        print('{} v{}'.format(NAME, VERSION))
        print('ERROR: ', end='')
        for err in iter(e.args):
            print(err)
        print('')
        exit(1)
