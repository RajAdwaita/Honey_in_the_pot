"""NanoPot.

Simple TCP honeypot logger

Usage:
    nanopot <config_filepath>

Options:
    <config_filepath>     Path to config options .ini file
    -h --help             Show this screen.
"""

# the above doc is the one that will be run directly

import configparser
from os import system
import logging
from nanopot import HoneyPot # from the nanopot package that we have we import the HoneyPot class that is we import it from the __init__.py file
import sys


def print_usage():
    print("Usage:")
    print("     python -m nanopot /etc/nanopot.ini")


# Check arguments

if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help']:
    print(__doc__)
    sys.exit(1)


# Load config_file

# from a python ini file we are loading the ports and the log_file_path
config_filepath = sys.argv[1]
config = configparser.ConfigParser()
config.read(config_filepath)

#using these we are running the .ini files and is the .ini files are empty then we log the default values

ports = config.get('default', 'ports', raw=True, fallback="8080,8888,9999")
host = config.get('default', 'host', raw=True, fallback="0.0.0.0")
log_filepath = config.get('default', 'logfile', raw=True,
                          fallback="/var/log/nanopot.log")
print("TEST")



# Double check ports provided
ports_list = []

try:
    ports_list = ports.split(',') # here we replace the string of ports with the actual list
except Exception as e:
    print('[-] Error parsing ports: %s.\nExiting.', ports) # if it doesn't work we throw an error

    sys.exit(1)

# Launch honeypot
honeypot = HoneyPot(host, ports_list, log_filepath) # the HoneyPot class is in the __init__ file and it defines the class when we initialize the thing
honeypot.run()
