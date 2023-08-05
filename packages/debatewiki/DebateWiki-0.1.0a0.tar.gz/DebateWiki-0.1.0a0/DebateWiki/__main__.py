import argparse
import sys

import DebateWiki
from DebateWiki.cli.start import StartCommand


def _optional_commands(parser):
    """
    Optional cli passed directly to the main parser.
    """
    parser.add_argument(
        "-V", "--version", version=f"{DebateWiki.__version__}", action="version"
    )
    parser.add_argument(
        "-v", "--verbose", help="increase output verbosity", action="store_true"
    )
    return parser


def _main_commands(parser):
    """
    Commands for the cli subparser is defined in
    :mod:`DebateWiki.cli` and called here.
    You can pass any of the arguments except `action` to these cli
    as defined by :func:`argparse.ArgumentParser.add_parser`.
    """
    StartCommand(parser, "start", aliases=["run"], help="start the server")
    return parser


def main(args=None):
    """The main entry point."""
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description="A wiki that only allows valid arguments to make it into its pages."
    )

    parser = _optional_commands(parser)
    parser_commands = parser.add_subparsers(title="Commands", dest="cli")
    parser_commands = _main_commands(parser_commands)

    if isinstance(args, list):
        args = parser.parse_args(args)
    else:
        args = parser.parse_args()

    if args.verbose:

        # This is different from logging output verbosity. Enabling this
        # will print command internals directly to STDOUT regardless of
        # the settings defined in the logging module. Only recommended
        # for use by developers.
        print("Verbose Mode: Enabled")

    try:
        args.action(args)
    except AttributeError:
        pass

    if len(sys.argv[1:]) == 0:
        parser.print_help()
        parser.exit(0)


if __name__ == "__main__":
    main()
