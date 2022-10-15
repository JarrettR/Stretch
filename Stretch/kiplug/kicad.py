import os, shutil
from datetime import datetime

import pcbnew
import sys

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

    def Backup(self, filename):
        # Backups are for when the plugin or the person does an oopsie
        # Running Stretch-from-SVG on a main file will act normally
        # but also create a filename.stretch_bkup.kicad_pcb copy beforehand.
        # Running Stretch-from-SVG on a backup will leave the backup untouched
        # and overwrite the main file with the new SVG->PCB data

        head, tail = os.path.split(filename)
        extension_name = ".kicad_pcb"
        backup_name = ".stretch_bkup"

        base_filename, ext = os.path.splitext(tail)
        if ext == extension_name:
            base_filename, bckup = os.path.splitext(base_filename)
            if bckup == backup_name:
                # this is already a backup, return filename without backup suffix
                return os.path.join(head, base_filename + extension_name)
            else:
                # copy file to backup, then return original filename unchanged
                dst_file = os.path.join(head, base_filename + backup_name + extension_name)

                if os.path.exists(dst_file):
                    os.remove(dst_file)
                shutil.move(filename, dst_file)

                return filename
        else:
            #This is an error condition
            print('Unrecognised extension: ', filename, tail, base_filename, ext)
            return filename

    def Run(self):
        b = pcbnew.GetBoard()
        pcb_filename = b.GetFileName()

        sys.stdout = open(os.path.join(os.path.dirname(pcb_filename), "out.log"), 'w')
        print('Begin Stretch debug')

        # from bs4 import BeautifulSoup
        print('Import BS4')

        if sys.version_info[0] == 3:
            from ..bspy3 import BeautifulSoup
        else:
            from ..bspy2 import BeautifulSoup


        if self.tool == "to_svg":
            from .svg_writer import SvgWrite
            a = SvgWrite()
            a.Run_Plugin(pcb_filename, self.svg_file_name)
        elif self.tool == "to_pcb":
            from .pcb_writer import PcbWrite
            a = PcbWrite()
            pcb_filename = self.Backup(pcb_filename)
            a.Run_Plugin(pcb_filename, self.svg_file_name)
            pcbnew.Refresh()
        sys.stdout.close()
   



