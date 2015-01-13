"""
Configuration file.
Includes all the global settings required to use the interface through some control paradigm.
CHECK THIS BEFORE TRY TO RUN THE INTERFACE FOR THE FIRST TIME!
"""

# IMPORTANT
# Mapping from logical values coming from control program into actions.
# The control program needs to agree on this mapping and send respective values through RPC calls.
# For each action A below excepting undo, there must be
#    a method in Control class called do_A().
# For example, ok -> control.do_ok()
ACTIONS = {0: 'ok',
           1: 'next',
           2: 'previous'}

# Path where panel descriptor files (living room panel, kitchen panel, etc.) and images are being stored.
RESOURCES_PATH = 'C:/Users/iena/Documents/dev/pysmartenv/resources'

# Maximum number of action options for each panel
OPTIONS_NUM = 6

# Identifier of the port where Arduino will be connected. Under Windows, usually a COM port.
SERIAL_PORT = 'COM3'

# RPC server settings. It will open a TCP socket on this host:port combination.
# Check this in case of installing interface and control program on separate computers.
RPC_HOST = 'localhost'
RPC_PORT = 8888



