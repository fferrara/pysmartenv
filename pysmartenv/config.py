"""
Configuration file.
Includes all the global settings required to use the interface through some control paradigm.
CHECK THIS BEFORE TRY TO RUN THE INTERFACE WITH A NEW CONTROL PARADIGM!
"""

# IMPORTANT
# Mapping from logical values coming from control program into actions.
# The control program needs to agree on this mapping and send respective values through RPC calls.
ACTIONS = {0: 'ok',
           1: 'next',
           2: 'undo'}

# Path where panel descriptor files (living room panel, kitchen panel, etc.) are being stored.
PANEL_PATH = ''

# Number of action options for each panel
OPTIONS_NUM = 4

# Identifier of the port where Arduino will be connected. Under Windows, usually a COM port.
SERIAL_PORT = ''

# RPC server settings. It will open a TCP socket on this host:port combination.
# Check this in case of installing interface and control program on separate computers.
RPC_HOST = 'localhost'
RPC_PORT = 8888



