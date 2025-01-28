# Which char does node represent?
# list/dict for pointers to child nodes
# true/false is node stop node (word)?

""" Module for Node class. """

class Node():
    """ Node class. """

    def __init__(self, key=None):
        """ Constructor. """

        self.key = key
        self.children = {}
        self.is_stop = False
        self.freq = None
