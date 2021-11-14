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


# using the logging module to log to a file and to the
# console at the same time (if the user wants to)
import logging
# we are able to replace the print() statement with the logger.info() statement


# from the nanopot package that we have we import the HoneyPot
# class that is we import it from the __init__.py file
from nanopot import HoneyPot
import sys


# Check arguments
# if the user does not provide the correct number of arguments
if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help']:
    print(__doc__)  # prints the docstring provided at the top of the file
    sys.exit(1)  # exit the program


# Load config_file

# from a python ini file we are loading the ports and the log_file_path
config_filepath = sys.argv[1]   # the path to the config file
config = configparser.ConfigParser()  # we are creating a config parser object
config.read(config_filepath)  # we are reading the config file


# using these we are running the .ini files and is the .ini files
# are empty then we log the default values


# we are getting the ports from the config file
# fallback value is basically setting the default value
ports = config.get('default', 'ports', raw=True, fallback="8080,8888,9999")
# we are getting the host from the config file
host = config.get('default', 'host', raw=True, fallback="0.0.0.0")
log_filepath = config.get('default', 'logfile', raw=True,
                          fallback="/var/log/nanopot.log")
# we are getting the log_filepath from the config file
print("TEST")


# Double check ports provided
ports_list = []

try:
    # here we replace the string of ports with the actual list
    ports_list = ports.split(',')
except Exception as e:
    # if it doesn't work we throw an error
    print('[-] Error parsing ports: %s.\nExiting.', ports)

    sys.exit(1)

# Launch honeypot
# the HoneyPot class is in the __init__ file and it defines the class when we initialize the thing
# we are creating a HoneyPot object
honeypot = HoneyPot(host, ports_list, log_filepath)


honeypot.run()  # we are running the HoneyPot class
