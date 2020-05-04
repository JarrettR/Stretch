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
        content = base.svg.kicad.contents[0][1:-3]
        content = '[' + content + ' ]'
        self.Save(content)
        meta = json.loads(content)
        meta.insert(0, 'kicad_pcb')

        lst = meta

        layers, modules, segments, gr_lines, vias = self.Parse_Layers_Segments(base)
        # print(layers_segments)

        lst.append(layers)
        lst = lst + vias
        lst = lst + modules
        lst = lst + segments
        lst = lst + gr_lines

        return lst

    def Parse_Layers_Segments(self, base):
        layers = ['layers']
        modules = []
        segments = []
        gr_lines = []


        for tag in base.svg.find_all('g'):
            if tag['id'] == 'layervia':
                vias = self.Parse_Vias(tag)

            elif tag['id'].startswith('module'):
                module = self.Parse_Module(tag)
                modules.append(module)

            elif tag['id'].startswith('layer'):
                layer = [ tag['number'] ]
                layer.append(tag['inkscape:label'])

                if tag.has_attr('user'):
                    layer.append('user')
                if tag.has_attr('signal'):
                    layer.append('signal')
                if tag.has_attr('power'):
                    layer.append('power')
                if tag.has_attr('hide'):
                    layer.append('hide')

                layers.append(layer)

                for path in tag.find_all('path'):
                    segment, gr_line = self.Parse_Segment(path)
                    segments = segments + segment
                    gr_lines = gr_lines + gr_line


        # layers.append(vias)
        # layers.append(segments)
        return layers, modules, segments, gr_lines, vias

    def Parse_Module(self, tag):
        # print(tag['id'])
        module = ['module', tag['name'], ['layer', tag['layer']]]
        segments = []
        gr_lines = []
        pads = []
        transform = tag['transform']
        
        translate = transform[transform.find('translate(') + 10:]
        translate = translate[0:translate.find(')')]
        x = translate[0:translate.find(',')]
        y = translate[len(x) + 1:]
        x = float(x) / pxToMM
        y = float(y) / pxToMM

        rotate = 0
        if 'rotate(' in transform:
            rotate = transform[transform.find('rotate(') + 7:]
            rotate = float(rotate[0:-1]) * -1

        at = ['at', str(x), str(y), str(rotate)]
        module.append(at)

        for path in tag.find_all('path'):
            segment, gr_line = self.Parse_Segment(path)
            segments = segments + segment
            gr_line[0][0] = 'fp_line'
            gr_lines = gr_lines + gr_line

        for rect in tag.find_all('rect'):
            pad = self.Parse_Pad(rect, 'rect')
            if pad != None:
                pads.append(pad)
        for circle in tag.find_all('circle'):
            pad = self.Parse_Pad(circle, 'circle')
            if pad != None:
                pads.append(pad)

        if len(segments) > 0:
            module.append(segments)
        if len(pads) > 0:
            module = module + pads

        module = module + gr_lines
        return module


    def Parse_Pad(self, tag, padtype):
        # print(tag['id'])

        if tag.has_attr('first') == False:
            return None

        pin = tag['pin']
        process = tag['process']

        if padtype == 'rect':

            width = float(tag['width']) / pxToMM
            height = float(tag['height']) / pxToMM
            x = str((float(tag['x']) / pxToMM) + (width / 2))
            y = str((float(tag['y']) / pxToMM) + (height / 2))
            width = str(width)
            height = str(height)

            size = ['size', width, height]

        elif padtype == 'circle':
            r = str((float(tag['r']) * 2) / pxToMM)
            size = ['size', r, r]
            x = str(float(tag['cx']) / pxToMM)
            y = str(float(tag['cy']) / pxToMM)


        at = ['at', x, y]
        if tag.has_attr('rotate'):
            at.append(tag['rotate'])

        layers = ['layers'] + tag['layers'].split(',')
        pad = ['pad', pin, process, padtype, at, size, layers]

        if tag.has_attr('roundrect_rratio'):
            pad.append(['roundrect_rratio',tag['roundrect_rratio']])
            pad[3] = 'roundrect'

        if tag.has_attr('net'):
            pad.append(['net',tag['net'],tag['netname']])


        return pad

    def Parse_Segment(self, tag):
        # print(tag['id'])

        style = tag['style']

        width = style[style.find('stroke-width:') + 13:]
        width = ['width', width[0:width.find('mm')]]

        name = ['layer', tag['layer']]

        paths = parse_path(tag['d'], None)

        segments = []
        gr_lines = []

        for path in paths:
            segment = []
            start = ['start', str(path.start.real / pxToMM), str(path.start.imag / pxToMM)]
            end = ['end', str(path.end.real / pxToMM), str(path.end.imag / pxToMM)]

            segment = [ start, end, width, name]

            if tag.has_attr('net'):
                segment.append(['net', tag['net']])
            if tag.has_attr('tstamp'):
                segment.append(['tstamp', tag['tstamp']])

            if tag['type'] == 'gr_line':
                segment = ['gr_line'] + segment
                gr_lines.append(segment)
            elif tag['type'] == 'segment':
                segment = ['segment'] + segment
                segments.append(segment)
            else:
                assert False,"Gr_line / segments: Nobody knows!"

        return segments, gr_lines

    def Parse_Vias(self, tag):
        # (via (at 205.486 133.731) (size 0.6) (drill 0.3) (layers F.Cu B.Cu) (net 0) (tstamp 5EA04144) (status 30))
        vias = []
        for circle in tag.find_all('circle'):
            x = circle['cx']
            y = circle['cy']
            at = ['at', str(float(x) / pxToMM), str(float(y) / pxToMM)]

            via = [ 'via', at, ['size', circle['size']], ['drill', circle['drill']]]

            layers = circle['layers'].split(',')
            layers = ['layers'] + layers

            via.append(layers)

            via.append(['net', circle['net']])

            if circle.has_attr('tstamp'):
                via.append(['tstamp', circle['tstamp']])
            if circle.has_attr('status'):
                via.append(['status', circle['status']])

            vias.append(via)
        return vias


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