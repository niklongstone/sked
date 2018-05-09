"""ConfigParser."""


class ConfigParser(object):
    """A base class to read a file."""

    def __init__(self, filename):
        self.filename = filename

    def read(self):
        raise NotImplementedError('You must implement the read() method!')
