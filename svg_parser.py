import io
from bs4 import BeautifulSoup
import json
import re

from parser_base import ParserBase
from sexpressions_parser import parse_sexpression
from sexpressions_writer import SexpressionWriter


class SvgParser(object):
    def __init__(self):
        self.filename_in = "example/out.svg"
        self.filename_out = "example/out.kicad_pcb"
        self.filename_json = "example/out.json"

    def Load(self):
        with open(self.filename_in, "r") as f:
    
            contents = f.read()
            svg = BeautifulSoup(contents, 'html.parser')
            return svg

    def Save(self, lst):
        with open(self.filename_json, 'w') as f:
            f.write(lst)

    def Svg_To_List(self, base):
        # content = base.svg.kicad.contents[0][:-3]
        content = base.svg.kicad.contents[0][1:-3]
        content = '[' + content + ' ]'
        self.Save(content)
        js = json.loads(content)
        # print(js)
        js.insert(0, 'kicad_pcb')

        return js

    def Run(self):
        svg = self.Load()
        lst = self.Svg_To_List(svg)
        a = SexpressionWriter()
        
        sexpression = a.List_To_Sexpression(lst)
        a.Save(sexpression)
        # self.Save(sexpression)
        

if __name__ == '__main__':
    e = SvgParser()
    e.Run()