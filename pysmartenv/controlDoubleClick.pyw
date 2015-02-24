"""
Main class
"""

import os
import threading
import time
import Queue
import panel
import config
import commandserver
import GUI
import arduino


class Control(object):
    def __init__(self, panelFile=None):
        # instantiate serial
        self.arduino = None
        try:
            self.arduino = arduino.Arduino()
        except Exception as e:
            print e.message

        if panelFile is None:
            # read from serial the panel id?
            pass
        else:
            self.panelFile = panelFile

        # build panel
        self.panels = dict()
        self.panels[1] = panel.Panel(self.panelFile, panelId=1)  # the key is = to panelId
        self.currentPanelId = 1

        # here the messages from Control will arrive
        # onOffQueue will contain string messages with 'on' and 'off'
        # panelQueue will contain panel that will be drawn
        # optionQueue will contain option that was selected
        self.onOffQueue = Queue.Queue()
        self.panelQueue = Queue.Queue()
        queues = (self.onOffQueue, self.panelQueue)

        # create GUI
        self.synchGUI = threading.Event()
        self.gui = GUI.GUI(queues, self.synchGUI)

        self.state = 'off'

    def _operate_device(self, pnl, option, operation):
        """
        :param
        pnl: The panel in which the option is
        option: The option representing the device
        operation: A string expressing the type of operation.
        In JSON file is attribute "deviceOperation"
        """
        # check type of operation
        if operation == 'switch' or (
                        operation == 'device_on' and not option.isOn) or (
                        operation == 'device_off' and option.isOn):
            # first, serial communication with arduino
            if self.arduino is not None:
                self.arduino.write(option.message)
            # update the panel
            pnl.switch()
            self.panelQueue.put_nowait(pnl)
            # the GUI main loop will update the window automatically
        elif operation == 'device_modify':
            # first, serial communication with arduino
            if self.arduino is not None:
                self.arduino.write(option.message)

            # update the panel, show ON icon only for 1 second
            pnl.switch()
            self.panelQueue.put_nowait(pnl)
            time.sleep(1)  # wait a moment with the icon highlighted
            pnl.switch()
            self.panelQueue.put_nowait(pnl)
            # the GUI main loop will update the window automatically

    def start(self):
        # start rpc
        server = commandserver.CommandServer(config.RPC_HOST, config.RPC_PORT, self)
        server_thread = threading.Thread(target=server.serve)
        server_thread.daemon = True
        server_thread.start()

        self.state = 'on'
        # create gui and enter in its main loop
        p = self.panels[self.currentPanelId]
        self.panelQueue.put(p)
        self.synchGUI.set()
        self.gui.mainloop()

    def turn_on(self):
        if self.state == 'off':
            self.onOffQueue.put_nowait('on')
            self.state = 'on'
            self.synchGUI.clear()
            time.sleep(2)  # wait a moment for the user to rest
            self.synchGUI.set()

    def do_ok(self):
        if self.state != 'off':
            option = self.panels[self.currentPanelId].currentOption

            if hasattr(option, 'turnOff'):
                self.onOffQueue.put_nowait('off')
                self.state = 'off'
                return 'OFF'

            if hasattr(option, 'deviceOperation') and not hasattr(option, 'objectId'):
                # operate a device and wait
                self._operate_device(self.panels[self.currentPanelId], option, option.deviceOperation)

            if hasattr(option, 'deviceOperation') and hasattr(option, 'objectId'):
                # the operation is about a device in another panel
                # the search in not efficient, but the number of panels and options is small
                for p in self.panels.values():  # loop through panels
                    for o in p.options:  # loop through option
                        # is there an option with same id in the panel?
                        if o.id == option.objectId:
                            # so, the deviceOperation is about a device in the other panel
                            self._operate_device(p, o, option.deviceOperation)

            if hasattr(option, 'panelId'):
                # create the new panel
                newPanelId = option.panelId

                if newPanelId in self.panels.keys():
                    p = self.panels[newPanelId]
                else:
                    p = panel.Panel(self.panelFile, newPanelId)
                    self.panels[newPanelId] = p
                self.currentPanelId = newPanelId
                self.panelQueue.put_nowait(p)
                # the GUI main loop will update the window automatically

            # wait a moment for the user to rest
            self.synchGUI.clear()
            time.sleep(2)  # wait
            self.synchGUI.set()

    def do_next(self):
        p = self.panels[self.currentPanelId]
        p.next_option()
        self.panelQueue.put_nowait(p)
        # wait a moment for the user to rest
        self.synchGUI.clear()
        time.sleep(2)
        self.synchGUI.set()

    def do_previous(self):
        p = self.panels[self.currentPanelId]
        p.prev_option()
        self.panelQueue.put_nowait(p)
        # wait a moment for the user to rest
        self.synchGUI.clear()
        time.sleep(2)
        self.synchGUI.set()


if __name__ == '__main__':
    PANEL_FILE = os.path.join(config.RESOURCES_PATH, 'sala.panel')
    cntrl = Control(PANEL_FILE)

    cntrl.start()

