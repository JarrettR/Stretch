import io, os
from bs4 import BeautifulSoup
import json
import re
import math
import cmath

from parser_base import ParserBase
from sexpressions_parser import parse_sexpression
from sexpressions_writer import SexpressionWriter

from svgpath import parse_path

pxToMM = 3.779528

class PcbWrite(object):
    def __init__(self):
        self.filename_in = "example/out.svg"
        self.filename_out = "example/out.kicad_pcb"
        self.filename_json = "example/out.json"

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

    def Svg_To_List(self, base):
        content = base.svg.kicad.contents[0][1:-3]
        content = '[' + content + ' ]'
        # self.Save(content)
        meta = json.loads(content)
        # meta.insert(0, 'kicad_pcb')
        if meta[0] != 'kicad_pcb':
            meta.insert(0, 'kicad_pcb')

        lst = meta

        layers, modules, segments, gr_lines, gr_arcs, vias = self.Parse_Layers_Segments(base)
        # print(layers_segments)

        lst.append(layers[::-1])
        lst = lst + vias
        lst = lst + modules
        lst = lst + segments
        lst = lst + gr_lines
        lst = lst + gr_arcs

        return lst

    def Parse_Layers_Segments(self, base):
        #This gets reversed later
        layers = []
        modules = []
        segments = []
        gr_lines = []
        gr_arcs = []


        for tag in base.svg.find_all('g'):
            if tag['id'] == 'layervia':
                vias = self.Parse_Vias(tag)

            elif tag['id'].startswith('module'):
                module = self.Parse_Module(tag)
                modules.append(module)

            elif tag['id'].startswith('layer'):
                #This gets reversed later
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
                    segment, gr_line, gr_arc = self.Parse_Segment(path)
                    segments = segments + segment
                    gr_lines = gr_lines + gr_line
                    gr_arcs = gr_arcs + gr_arc


        layers.append('layers')
        return layers, modules, segments, gr_lines, gr_arcs, vias

    def Parse_Module(self, tag):
        # print(tag['id'])
        module = ['module', tag['name'], ['layer', tag['layer']]]
        segments = []
        gr_lines = []
        gr_arcs = []
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
            segment, gr_line, gr_arc = self.Parse_Segment(path)
            segments = segments + segment
            gr_line[0][0] = 'fp_line'
            gr_lines = gr_lines + gr_line
            gr_arcs = gr_arcs + gr_arc

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

        module = module + gr_lines + gr_arcs
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

        if tag.has_attr('layer'):
            name = ['layer', tag['layer']]
        elif tag.parent.has_attr('inkscape:label'):
            #XML metadata trashed, try to recover from parent tag
            name = ['layer', tag.parent['inkscape:label']]
        else:
            assert False, "Path not in layer"

        paths = parse_path(tag['d'])

        segments = []
        gr_lines = []
        gr_arcs = []

        for path in paths:
            segment = []
            start = ['start', str(path.start.real / pxToMM), str(path.start.imag / pxToMM)]
            end = ['end', str(path.end.real / pxToMM), str(path.end.imag / pxToMM)]

            segment = [ start, end, width, name]

            if tag.has_attr('net'):
                segment.append(['net', tag['net']])
            if tag.has_attr('tstamp'):
                segment.append(['tstamp', tag['tstamp']])

            if tag.has_attr('type') == False or tag['type'] == 'gr_line':
                segment = ['gr_line'] + segment
                gr_lines.append(segment)
            elif tag['type'] == 'segment':
                segment = ['segment'] + segment
                segments.append(segment)
            elif tag['type'] == 'gr_arc':
                gr_arcs.append(self.Parse_Arcs(tag, segment))
            else:
                print(tag)
                assert False,"Gr_line / segments: Nobody knows!"

        return segments, gr_lines, gr_arcs

    def Parse_Arcs(self, tag, segments):
        # 0 gr_arc
        # 1
        #   0 start
        #   1 66.66
        #   2 99.99
        # 2
        #   0 end
        #   1 66.66
        #   2 99.99
        # 3
        #   0 angle
        #   1 -90
        # 4
        #   0 layer
        #   1 Edge.Cuts
        # 5
        #   0 width
        #   1 0.05
        # 6
        #   0 tstamp
        #   1 5E451B20

        path = parse_path(tag['d'])
        # print(tag)
        # print(tag['d'])
        # print(path)
        radius = path[0].radius.real / pxToMM
        # angle = '90'
        sweep = path[0].sweep
        large_arc = path[0].large_arc
        # print(segments)


        if bool(large_arc) == True:
            print("Handle~!")

        #KiCad 'start' is actually centre, 'end' is actually svg start
        #SVG end is actual end, we need to calculate centre instead
        # print('path', path[0].start, path[0].end)

        end = [str(path[0].start.real / pxToMM), str(path[0].start.imag / pxToMM)]
        end_complex = (path[0].start.real / pxToMM) + 1j * (path[0].start.imag / pxToMM)
        start_complex = (path[0].end.real / pxToMM) + 1j * (path[0].end.imag / pxToMM)

        q = math.sqrt((end_complex.real - start_complex.real)**2 + (end_complex.real - start_complex.real)**2)

        x3 = (start_complex.real + end_complex.real) / 2
        y3 = (start_complex.imag + end_complex.imag) / 2


        if bool(large_arc) == True:
            #hackhack / fix / whatever:
            #figure out why this is larger than radius sometimes
            print("hackhack: generating janky arc")
            print(radius , q)
            q = q / 2


        if bool(sweep) == False:
            # angle = -angle
            angle = 1
            x = x3 + math.sqrt(radius**2 - (q / 2) ** 2) * (start_complex.imag - end_complex.imag) / q
            y = y3 - math.sqrt(radius**2 - (q / 2) ** 2) * (start_complex.real - end_complex.real) / q
        else:
            # angle = '90'
            angle = -1
            x = x3 - math.sqrt(radius**2 - (q / 2) ** 2) * (start_complex.imag - end_complex.imag) / q
            y = y3 + math.sqrt(radius**2 - (q / 2) ** 2) * (start_complex.real - end_complex.real) / q
   
        start_list = ['start', str(x), str(y)]
        end_list = ['end', end[0], end[1]]

        start_angle = self.Get_Angle([x,y], [path[0].start.real / pxToMM, path[0].start.imag / pxToMM])
        end_angle = self.Get_Angle([x,y], [path[0].end.real / pxToMM, path[0].end.imag / pxToMM])

        angle = angle * (end_angle - start_angle)
        if bool(sweep) == True:
            angle = 360 - angle
        angle = "{:.6f}".format(round(angle, 6))
        
        segments[0] = start_list
        segments[1] = end_list
        segments.insert(2, ([ 'angle', angle]))
        segments.insert(0, 'gr_arc')
        return segments


    def Get_Angle(self, centre, point):
        vec1 = centre[0] + 1j * centre[1]
        vec2 = point[0] + 1j * point[1]
        vec3 = vec2 - vec1
        return math.degrees(cmath.phase(vec3))

    def Parse_Vias(self, tag):
        # (via (at 205.486 133.731) (size 0.6) (drill 0.3) (layers F.Cu B.Cu) (net 0) (tstamp 5EA04144) (status 30))
        vias = []
        for via_in in tag.find_all('g'):
            if not via_in.has_attr('type'):
                continue
            if not via_in['type'] == "via":
                continue
            x = via_in['x']
            y = via_in['y']
            at = ['at', str(float(x) / pxToMM), str(float(y) / pxToMM)]

            via = [ 'via', at, ['size', via_in['size']], ['drill', via_in['drill']]]

            layers = via_in['layers'].split(',')
            layers = ['layers'] + layers

            via.append(layers)

            via.append(['net', via_in['net']])

            if via_in.has_attr('tstamp'):
                via.append(['tstamp', via_in['tstamp']])
            if via_in.has_attr('status'):
                via.append(['status', via_in['status']])

            vias.append(via)
        return vias


    def Run_Standalone(self):
        svg = self.Load()
        lst = self.Svg_To_List(svg)
        a = SexpressionWriter()
        
        sexpression = a.List_To_Sexpression(lst)
        a.Save(sexpression)
        # self.Save(sexpression)

    def Run_Plugin(self, pcb_filename, svg_filename):
        
        infile = os.path.dirname(pcb_filename) + '/' + svg_filename

        svg = self.Load(infile)
        lst = self.Svg_To_List(svg)
        a = SexpressionWriter()
        
        sexpression = a.List_To_Sexpression(lst)
        a.Save(sexpression, pcb_filename)
        # self.Save(sexpression)
        

if __name__ == '__main__':
    e = PcbWrite()
    e.Run_Standalone()