from signal import SIGINT, signal

from ..cli import click_cli
from ..constants import CLI_NAME as CLI_NAME, VERSION as VERSION
from ..exceptions import ElasticsearchKibanaCLIException


def sigint_handler(signal_received, frame):
    print("SIGINT received, exiting.")
    exit(1)


def eskbcli():
    signal(SIGINT, sigint_handler)

    try:
        click_cli.eskbcli_interface()
    except ElasticsearchKibanaCLIException as e:
        print("")
        print("{} v{}".format(CLI_NAME, VERSION))
        print("ERROR: ", end="")
        for err in iter(e.args):
            print(err)
        print("")
        exit(9)
