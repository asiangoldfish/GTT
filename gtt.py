import argparse
from src import Application
from sys import argv

VERSION = '1.0'

parser = argparse.ArgumentParser(
    description='The GitLab time tracker analytics tool'
)

# Global options
parser.add_argument("--format",
                    choices=["table", "json"],  # restrict formats
                    help="Choose output format: table, json"
                    )
parser.add_argument("--version", action="store_true",
                    help="Print the current version")
parser.add_argument("--debug", action="store_true", help="Enable debug mode")
parser.add_argument("--sync", action="store_true",
                    help="Synchronise with remote")

# Subcommands
subparsers = parser.add_subparsers(dest="command", required=False)

# time-deviation subcommand
time_dev_parser = subparsers.add_parser(
    "time-deviation",
    help="Show time deviations"
)
time_dev_parser.add_argument("--user", help="Specify a GitLab user")
time_dev_parser.add_argument(
    "--sprint",
    required=True,
    help="Sprint name or ID to calculate deviations for",
    default=-1
)

# If no arguments provided, show help
if len(argv) == 1:
    parser.print_help()
    exit(1)

args = parser.parse_args()

# Dispatch commands
app = Application()
app.debug = args.debug

if not app.init():
    exit(1)

if args.command == "time-deviation":
    # Show time deviations
    app.show_time_estimate_deviation(args.user, args.sprint)
else:
    ## Global flags
    if args.format:
        app.show(args.format)

    # Global commands
    if args.version:
        print(f"GTT version {VERSION}")
    elif args.sync:
        app.sync()

