"""

"""
import json
from collections import deque


class ActionOption(object):
    """
    A single action option
    """

    def __init__(self, properties):
        # create an attribute, with the same name, for each key contained in properties
        self.__dict__ = properties

        # setting the state to false (off) for every option at beginning
        self.isOn = False


class Panel(object):
    """
    A Menu Panel, a container for a set of action options.
    Just one option can be selected at once.

    The object keeps track of the currently selected option and
    the state (on/off) of every option.
    This can be updated using methods: next_option(), switch(), rollback_action()
    """

    def __init__(self, panelFile, panelId, parent=None):
        with open(panelFile) as f:
            try:
                panelDict = json.load(f)
            except Exception as e:
                print 'JSON Error: check the JSON file'
                print e.message
                exit(1)

            if panelDict['panels'] is None:
                raise AttributeError

        self.id = 0
        for p in panelDict['panels']:
            if p['id'] == panelId:  # panel found
                self.id = p['id']  # id panel
                self.options = [ActionOption(item) for item in p['items']] # list of options

                self.currentOption = self.options[0]  # first option selected at beginning
                break

    def next_option(self):
        """
        One step ahead among options
        """
        i = self.options.index(self.currentOption)
        if i == len(self.options) - 1:  # last option
            i = 0
        else:
            i += 1

        self.currentOption = self.options[i]

    def prev_option(self):
        """
        One step behind among options
        """
        i = self.options.index(self.currentOption)
        if i == 0:  # last option
            i = len(self.options) - 1
        else:
            i -= 1

        self.currentOption = self.options[i]

    def switch(self):
        self.currentOption.isOn = not self.currentOption.isOn


# Test class example
if __name__ == '__main__':
    jsonFile = '../resources/sala.panel'
    panel = Panel(jsonFile)

    assert (panel.id == 1)
    assert (len(panel.options) == 4)
    print panel.options[0].name
    print panel.options[0].isOn
    panel.switch()
    print panel.options[0].isOn
    panel.next_option()
    print panel.options[1].isOn
    panel.switch()
    print panel.options[1].isOn
    panel.prev_option()
    print panel.currentOption.name