import io, os
from bs4 import BeautifulSoup
import json
import re
import math
import cmath

#Running KiCad Linux vs. standalone requires different imports
try:
    # from .stretch import Board
    from .parser_base import ParserBase
    from .sexpressions_parser import parse_sexpression
    from .sexpressions_writer import SexpressionWriter
except:
    # from stretch import Board
    from parser_base import ParserBase
    from sexpressions_parser import parse_sexpression
    from sexpressions_writer import SexpressionWriter

pxToMM = 3.779528

class PcbWrite(object):
    def __init__(self):
        currentdir = os.path.dirname(os.path.realpath(__file__))
        self.filename_in = os.path.join(currentdir, 'tests', 'out.svg')
        self.filename_out = os.path.join(currentdir, 'tests', 'out.kicad_pcb')
        self.filename_json = os.path.join(currentdir, 'tests', 'out.json')

    def Load(self, filename = None):
        if filename is None:
            filename = self.filename_in

        with open(filename, "r") as f:
    
            contents = f.read()
            svg = BeautifulSoup(contents, 'html.parser')
            return svg

    def Save(self, lst, filename = None):
        if filename is None:
            filename = self.filename_json

        with open(filename, 'w') as f:
            f.write(lst)

    def Save_Json(self, obj, save = False):
        currentdir = os.path.dirname(os.path.realpath(__file__))
        self.filename_json = os.path.join(currentdir, 'example', 'out.json')
        js = json.dumps(obj)
        if save:
            with open(self.filename_json, 'wb') as f:
                f.write(js)
        return js


    def Run_Standalone(self):
        svg = self.Load()
        # lst = self.Svg_To_List(svg)

        board = Board()
        board.From_SVG(svg)

        lst = board.To_PCB()
        # print(lst)

        a = SexpressionWriter()
        
        sexpression = a.List_To_Sexpression(lst)
        a.Save(sexpression)
        # self.Save(sexpression)

    def Run_Plugin(self, pcb_filename, svg_filename):
        from .board import Board
        from .board import Board
        
        infile = os.path.join(os.path.dirname(pcb_filename),svg_filename)

        svg = self.Load(infile)

        board = Board()
        board.From_SVG(svg)

        lst = board.To_PCB()

        a = SexpressionWriter()
        
        sexpression = a.List_To_Sexpression(lst)
        a.Save(sexpression, pcb_filename)
        

if __name__ == '__main__':
    e = PcbWrite()
    e.Run_Standalone()