"""The base command."""

import os.path
from sked.common import YamlParser
import sys


class BaseCommand(object):
    """A base command."""

    def __init__(self, options, *args, **kwargs):
        DEFAULT_FILE = 'sked.yml'
        self.options = options
        self.args = args
        self.kwargs = kwargs
        filename = DEFAULT_FILE

        if options['-c'] != None:
            filename = str(options['-c'])
        if os.path.exists(filename) != True:
            print('config file:' + filename + ' Doesn\'t exists')
            sys.exit()
        self.config_parser = YamlParser(filename)

    def run(self):
        raise NotImplementedError('You must implement the run() method!')
