"""
RPC Server
"""

import threading
from jsonrpctcp import server
import config

class CommandServer(server.Server):
    def __init__(self, host, port, cntrl):
        server.Server.__init__(self, (host, port))
        self.control = cntrl

        # add each remote procedure handler
        self.add_handler(self.command_handler, 'command')
        self.add_handler(self.turn_on_handler, 'turn_on')
        self.add_handler(self.turn_off_handler, 'turn_off')

    def command_handler(self, command):
        try:
            # retrieve action
            action = config.ACTIONS[command]
            # build function name
            function = 'do_' + action

            # execute function
            # 'getattr(object, function)' returns a function which is called
            f = getattr(self.control, function)
            return f()
        except KeyError as ke:  # command not present
            raise Exception('Command %s not implemented' % str(command))
        except Exception as e:  # generic error
            print e.message
            raise Exception('Error doing %s' % str(command))

    def turn_on_handler(self):
        try:
            f = getattr(self.control, 'turn_on')
            f()
        except Exception as e:  # generic error
            raise Exception('Error doing turn_on')

    def turn_off_handler(self):
        try:
            f = getattr(self.control, 'turn_off')
            f()
        except Exception as e:  # generic error
            raise Exception('Error doing turn_on')

if __name__ == '__main__':
    import time
    import sys
    import control

    c = control.Control()
    svr = CommandServer(config.RPC_HOST, config.RPC_PORT, c)

    server_thread = threading.Thread(target=svr.serve)
    server_thread.daemon = True
    server_thread.start()

    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print 'Finished.'
        sys.exit()