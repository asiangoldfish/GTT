import argparse
from src import Application
from sys import argv

VERSION = '1.0'

parser = argparse.ArgumentParser(
    description='The GitLab time tracker analytics tool')

# Command
parser.add_argument(
    "--format",
    help="Choose output format: table, json"
)
parser.add_argument('--time-deviation', action='store_true', help='Show time deviation for a user')

# Options
parser.add_argument('--version', action='store_true',
                    help='print the current version')
parser.add_argument('--debug', action='store_true', help='enable debug mode')
parser.add_argument('--sync', action='store_true', help='synchronise with remote')
parser.add_argument('--user')

args = parser.parse_args()

# Show help page. At least one argument must be present
if len(argv) == 1:
    parser.print_help()
    exit(0)

if args.version:
    print(f"GTT version {VERSION}")
    exit(0)

app = Application()
app.debug = args.debug

if not app.init():
    exit(1)

if args.sync and app.sync():
    print("Successfully synchronised with remote")

if args.format:
    app.show(args.format)
elif args.time_deviation:
    app.show_time_estimate_deviation(args.user)