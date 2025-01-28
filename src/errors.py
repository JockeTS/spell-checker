""" Module for custom exceptions. """

class Error(Exception):
    """ User defined class for custom exceptions. """

class SearchMiss(Error):
    """ Raised if search results empty. """
