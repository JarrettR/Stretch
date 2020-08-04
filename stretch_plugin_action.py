import pcbnew
import os

from .svg_writer import SvgWrite 
from .pcb_writer import PcbWrite 

class StretchPluginAction(pcbnew.ActionPlugin):
    def __init__(self, tool):
        self.tool = tool
        super(StretchPluginAction, self).__init__()

    def defaults(self):
        if self.tool == "to_svg":
            self.name = "Stretch-To-SVG"
            self.category = "A KiCad plugin"
            self.description = "A plugin to add beauty"
            self.show_toolbar_button = True # Optional, defaults to False
            self.icon_file_name = os.path.join(os.path.dirname(__file__), 'to_svg.png') # Optional
        elif self.tool == "to_pcb":
            self.name = "Stretch-To-PCB"
            self.category = "A KiCad plugin"
            self.description = "A plugin to add beauty"
            self.show_toolbar_button = True # Optional, defaults to False
            self.icon_file_name = os.path.join(os.path.dirname(__file__), 'to_pcb.png') # Optional

        self.svg_file_name = 'out.svg'

    def Run(self):
        b = pcbnew.GetBoard()
        pcb_filename = b.GetFileName()
        
        #If BS4 not installed:
        try:
            import bs4
        except ImportError:
            pcbnew._pcbnew.ProcessExecute('pip install bs4')
        #todo: test!

        if self.tool == "to_svg":
            a = SvgWrite()
            a.Run_Plugin(pcb_filename, self.svg_file_name)
        elif self.tool == "to_pcb":
            a = PcbWrite()
            a.Run_Plugin(pcb_filename, self.svg_file_name)
            pcbnew.Refresh()

        
# D:\Programs\KiCad\bin\python.exe .\stretch_plugin_action.py
if __name__ == '__main__':
    a = PcbWrite()
    a.Run_Plugin('D:\\Projects\\git\\test\\what.kicad_pcb', 'out.svg')