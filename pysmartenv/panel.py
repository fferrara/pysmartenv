"""

"""
import json

class ActionOption(object):
    """
    A single action option
    """

    def __init__(self, name, imgFile, actionCode):
        self.name = name
        self.imgFile = imgFile
        self.message = actionCode


class Panel(object):
    """
    A Menu Panel, a container for a set of action options.
    Just one option can be selected at once.

    The object keeps track of the currently selected option and
    the state (on/off) of every option.
    This can be updated using methods: next_option(), switch(), rollback_action()
    """

    def __init__(self, panelFile):
        with open(panelFile) as f:
            panelDict = json.load(f)
            if panelDict['panel'] is None:
                raise AttributeError

        self.id = panelDict['panel']['id'] # id panel
        self.options = [ActionOption(item['name'], item['img'], # list of options
                                     item['message']) for item in panelDict['panel']['items']]
        self.currentOption = self.options[0] # first option selected at beginning

    def next_option(self):
        raise NotImplementedError

    def switch(self):
        raise NotImplementedError

    def rollback_action(self):
        raise NotImplementedError


# Test class example
if __name__ == '__main__':
    jsonFile = '../resources/sala.panel'
    panel = Panel(jsonFile)

    assert (panel.id == 1)
    assert (len(panel.options) == 4)
    print panel.options[0].name