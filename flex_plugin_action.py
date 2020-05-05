import pcbnew
import os

from svg_writer import SvgWrite 
# from .svg_writer import SvgWrite 

class FlexPluginAction(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Flex"
        self.category = "A KiCad plugin"
        self.description = "A plugin to add beauty"
        self.show_toolbar_button = True # Optional, defaults to False
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'icon.png') # Optional
        self.output_file_name = 'out.svg'

    def Run(self):
        b = pcbnew.GetBoard()
        filename = b.GetFileName()

        a = SvgWrite()
        a.Run_Plugin(filename, self.output_file_name)

        
# D:\Programs\KiCad\bin\python.exe .\flex_plugin_action.py
if __name__ == '__main__':
    a = SvgWrite()
    a.Run_Plugin('D:\\Projects\\git\\test\\what.kicad_pcb', 'out.svg')