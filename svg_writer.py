import io, os
from bs4 import BeautifulSoup
import json
import math
import cmath

#Running KiCad Linux vs. standalone requires different imports
try:
    from .stretch import Board
    from .parser_base import ParserBase
    from .sexpressions_parser import parse_sexpression
    from .sexpressions_writer import SexpressionWriter
except:
    from stretch import Board
    from parser_base import ParserBase
    from sexpressions_parser import parse_sexpression
    from sexpressions_writer import SexpressionWriter


class SvgWrite(object):
    def __init__(self):
        print(os.path.dirname(os.path.realpath(__file__)) )
        currentdir = os.path.dirname(os.path.realpath(__file__))
        self.filename_in = os.path.join(currentdir, 'tests', 'complex.kicad_pcb')
        # self.filename_in = os.path.join(currentdir, 'tests', 'simple.kicad_pcb')
        self.filename_json = os.path.join(currentdir, 'tests', 'out.json')
        self.filename_svg = os.path.join(currentdir, 'tests', 'out.svg')
        self.filename_base = os.path.join(currentdir, 'tests', 'base.svg')
        
        self.hiddenLayers = []


    def Load(self, filename = None):
        if filename is None:
            filename = self.filename_in

        with io.open(filename, 'r', encoding='utf-8') as f:
            sexpression = parse_sexpression(f.read())
        return sexpression

    def Convert(self, obj, save = False):
        js = json.dumps(obj)
        if save:
            with open(self.filename_json, 'wb') as f:
                f.write(js)
        return js

    def Save(self, svg, filename = None):
        if filename is None:
            filename = self.filename_svg

        with open(filename, 'wb') as f:
            f.write(svg)

    def Print_Headings(self, dic):
        for item in dic:
            if type(item) is str:
                print(item)
            else:
                print(item[0])

    def Run_Standalone(self):
        dic = self.Load()
        
        #Save JSON file, for development
        #self.Convert(dic, True)

        with open(self.filename_base, "r") as f:
            contents = f.read()
            base = BeautifulSoup(contents, 'html.parser')
        

        board = Board()
        board.From_PCB(dic)
        
        svg = board.To_SVG()

        self.Save(svg)

   
    def Run_Plugin(self, filename, outfilename):
        dic = self.Load(filename)
        
        with open(self.filename_base, "r") as f:
    
            contents = f.read()
            base = BeautifulSoup(contents, 'html.parser')
        
        outfile = os.path.join(os.path.dirname(filename), outfilename)

        svg = self.Handle_Headings(dic, base)

        self.Save(svg, outfile)



if __name__ == '__main__':
    e = SvgWrite()
    e.Run_Standalone()