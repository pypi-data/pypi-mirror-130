VERSION = (0, 7, 8)
__release__ = ''.join(['-.'[type(x) == int]+str(x) for x in VERSION])[1:]
__version__ = '.'.join((str(VERSION[0]), str(VERSION[1])))
