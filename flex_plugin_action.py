import pcbnew
import os

from svg_writer import SvgWrite 
from pcb_writer import PcbWrite 
# from .svg_writer import SvgWrite 

class FlexPluginAction(pcbnew.ActionPlugin):
    def __init__(self, tool):
        self.tool = tool
        super(FlexPluginAction, self).__init__()

    def defaults(self):
        if self.tool == "to_svg":
            self.name = "Flex-To-SVG"
            self.category = "A KiCad plugin"
            self.description = "A plugin to add beauty"
            self.show_toolbar_button = True # Optional, defaults to False
            self.icon_file_name = os.path.join(os.path.dirname(__file__), 'to_svg.png') # Optional
            self.output_file_name = 'out.svg'
        elif self.tool == "to_pcb":
            self.name = "Flex-To-PCB"
            self.category = "A KiCad plugin"
            self.description = "A plugin to add beauty"
            self.show_toolbar_button = True # Optional, defaults to False
            self.icon_file_name = os.path.join(os.path.dirname(__file__), 'to_pcb.png') # Optional
            self.output_file_name = 'out.svg'

    def Run(self):
        b = pcbnew.GetBoard()
        filename = b.GetFileName()

        if self.tool == "to_svg":
            a = SvgWrite()
            a.Run_Plugin(filename, self.output_file_name)
        elif self.tool == "to_pcb":
            a = PcbWrite()
            a.Run_Plugin(filename, self.output_file_name)

        
# D:\Programs\KiCad\bin\python.exe .\flex_plugin_action.py
if __name__ == '__main__':
    a = PcbWrite()
    a.Run_Plugin('D:\\Projects\\git\\test\\what.kicad_pcb', 'out.svg')