import pcbnew
import os

class FlexPluginAction(pcbnew.ActionPlugin)
    def defaults(self):
        self.name = "Flex"
        self.category = "A KiCad plugin"
        self.description "A plugin to add beauty"
        self.show_toolbar_button = True # Optional, defaults to False
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'icon.png') # Optional

    def Run(self):
        # The entry function of the plugin that is executed on user action
        print("Hello World")

        