import io
from bs4 import BeautifulSoup
import json
import re

from parser_base import ParserBase
from sexpressions_parser import parse_sexpression


class SexpressionWriter(object):
    def __init__(self):
        self.filename_in = "example/out.svg"
        self.filename_out = "example/out.kicad_pcb"
        self.filename_sexpression = "example/complex.kicad_pcb"

    def Load(self):
        with open(self.filename_in, "r") as f:
    
            contents = f.read()
            svg = BeautifulSoup(contents, 'html.parser')
            return svg

    def Load_Sexpression(self):
        with io.open(self.filename_sexpression, 'r', encoding='utf-8') as f:
            sexpression = parse_sexpression(f.read())
        return sexpression



    def List_Escape(self, lst):
        newlist = []
        RE = re.compile('[\\\/\?%\(\)\ ]|^$')

        for value in lst:
            if type(value) is not list:
                # print(value)
                if RE.search(value):
                    value = '"' + value + '"'

            newlist.append(value)

        return newlist


    def List_To_Sexpression(self, lst, first = True):
        line = []

        lst = self.List_Escape(lst)

        for value in lst:
            if type(value) is list:
                line.append('(' + self.List_To_Sexpression(value, False) + ')\n')
            else:
                line.append(value)

        out = ' '.join(line)

        if first:
            out = '(' + out + ')'

        return out

    def Save(self, sexpression, filename = None):
        if filename is None:
            filename = self.filename_out

        with open(filename, 'w') as f:
            f.write(sexpression)

    def Run(self):
        # svg = self.Load()
        lst = self.Load_Sexpression()
        sexpression = self.List_To_Sexpression(lst)
        self.Save(sexpression)
        

if __name__ == '__main__':
    e = SexpressionWriter()
    e.Run()