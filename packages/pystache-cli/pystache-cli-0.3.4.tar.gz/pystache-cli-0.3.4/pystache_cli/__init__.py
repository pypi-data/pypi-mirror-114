"""
Extended command line client for pystache
"""
__version__ = "0.3.4"
__author__ = "Christian Winger"
__email__ = "c@wingechr.de"
__url__ = "https://github.com/wingechr/pystache-cli"

try:
    from .pystache_cli import render
except ModuleNotFoundError: # during setup
    pass
