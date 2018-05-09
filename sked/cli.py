"""
sked

Usage:
  sked create [-c=<config_file>]
  sked delete [-c=<config_file>]
  sked -h | --help
  sked --version

Options:
  -h --help           Show this screen.
  --version           Show version.
  -c=<config_file>    Config file [default:autoscaling.yml]

Examples:
  sked create -c my_autoscaling.yml
  sked delete -c my_autoscaling.yml

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/niklongstone/sked
"""

from inspect import getmembers, isclass
from docopt import docopt
from . import __version__ as VERSION


def main():
    """Main CLI entrypoint."""
    import sked.commands
    options = docopt(__doc__, version=VERSION)
    for (k, val) in options.items():
        if hasattr(sked.commands, k) and val:
            module = getattr(sked.commands, k)
            sked.commands = getmembers(module, isclass)
            command = [command[1] for command in sked.commands if command[0].lower() == k][0]
            command = command(options)
            command.run()
