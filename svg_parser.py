import io
from bs4 import BeautifulSoup
import json
import re

from parser_base import ParserBase
from sexpressions_parser import parse_sexpression
from sexpressions_writer import SexpressionWriter

from svgpath import parse_path

pxToMM = 3.779528

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
        meta = json.loads(content)
        # print(js)
        meta.insert(0, 'kicad_pcb')

        lst = meta


        layers, segments = self.Parse_Layers_Segments(base)
        # print(layers_segments)

        lst.append(layers)
        lst = lst + segments

        return lst

    def Parse_Layers_Segments(self, base):
        layers = ['layers']
        segments = []


        for tag in base.svg.find_all('g'):
            if tag['id'] == 'layervia':
                vias = self.Parse_Vias(tag)

            elif tag['id'].startswith('module'):
                print(tag['id'])

            elif tag['id'].startswith('layer'):
                print(tag['id'])
                layer = [ tag['number'] ]
                layer.append(tag['inkscape:label'])

                if tag.has_attr('user'):
                    layer.append('user')
                if tag.has_attr('hide'):
                    layer.append('hide')
                if tag.has_attr('signal'):
                    layer.append('signal')

                layers.append(layer)

                for path in tag.find_all('path'):
                    segments = segments + self.Parse_Segment(path)


        # layers.append(vias)
        # layers.append(segments)
        return layers, segments

    def Parse_Segment(self, tag):
        print(tag['id'])

        style = tag['style']

        width = style[style.find('stroke-width:') + 13:]
        width = ['width', width[0:width.find('mm')]]

        name = ['layer', tag['layer']]

        paths = parse_path(tag['d'], None)

        segments = []

        for path in paths:
            segment = []
            start = ['start', str(path.start.real / pxToMM), str(path.start.imag / pxToMM)]
            end = ['end', str(path.end.real / pxToMM), str(path.end.imag / pxToMM)]

            segment = [ 'segment', start, end, width, name]

            if 'net' in tag:
                segment.append(['net', tag['net']])
            if 'tstamp' in tag:
                segment.append(['tstamp', tag['tstamp']])

            segments.append(segment)

        return segments

    def Parse_Vias(self, tag):
        # for tag in base.svg.find_all('g'):
        print(tag['id'])


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