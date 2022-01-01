import os
from datetime import datetime

import pcbnew

class Stretch(pcbnew.ActionPlugin, object):

    def __init__(self, tool):
        self.tool = tool
        super(Stretch, self).__init__()

    def defaults(self):
        if self.tool == "to_svg":
            self.name = "Stretch-To-SVG"
            self.category = "A KiCad plugin"
            self.description = "A plugin to add beauty"
            self.show_toolbar_button = True # Optional, defaults to False
            self.icon_file_name = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'icons', 'to_svg.png') # Optional
        elif self.tool == "to_pcb":
            self.name = "Stretch-To-PCB"
            self.category = "A KiCad plugin"
            self.description = "A plugin to add beauty"
            self.show_toolbar_button = True # Optional, defaults to False
            self.icon_file_name = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'icons', 'to_pcb.png') # Optional

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
            from .svg_writer import SvgWrite
            a = SvgWrite()
            a.Run_Plugin(pcb_filename, self.svg_file_name)
        elif self.tool == "to_pcb":
            from .pcb_writer import PcbWrite
            a = PcbWrite()
            a.Run_Plugin(pcb_filename, self.svg_file_name)
            pcbnew.Refresh()
   



