import io, os
from bs4 import BeautifulSoup
import json
import re
import math
import cmath

#Running KiCad Linux vs. standalone requires different imports
try:
    from .parser_base import ParserBase
    from .sexpressions_parser import parse_sexpression
    from .sexpressions_writer import SexpressionWriter
    from .svgpath import parse_path
except:
    from parser_base import ParserBase
    from sexpressions_parser import parse_sexpression
    from sexpressions_writer import SexpressionWriter
    from svgpath import parse_path

pxToMM = 3.779528

class PcbWrite(object):
    def __init__(self):
        currentdir = os.path.dirname(os.path.realpath(__file__))
        self.filename_in = os.path.join(currentdir, 'example', 'out.svg')
        self.filename_out = os.path.join(currentdir, 'example', 'out.kicad_pcb')
        self.filename_json = os.path.join(currentdir, 'example', 'out.json')

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
        content = base.svg.kicad.contents[0][0:-1]
        content = '[' + content + ' ]'
        # self.Save(content)
        meta = json.loads(content)
        # meta.insert(0, 'kicad_pcb')
        if meta[0] != 'kicad_pcb':
            meta.insert(0, 'kicad_pcb')

        lst = meta

        layers, chunk = self.Parse_Layers_Segments(base)
        # print(layers_segments)

        lst.append(layers[::-1])
        lst = lst + chunk

        return lst

    def Parse_Layers_Segments(self, base):
        #This gets reversed after it returns
        layers = []
        modules = []
        segments = []
        gr_lines = []
        gr_arcs = []
        gr_curves = []
        gr_polys = []
        gr_text = []
        zones = []

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
                    if path.has_attr('type') == True and path['type'] == 'zone':
                        zones.append(self.Parse_Zone(path))
                    elif path.has_attr('type') == True and path['type'] == 'gr_poly':
                        gr_polys.append(self.Parse_Polys(path))
                    else:
                        segment, gr_line, gr_arc, gr_curve = self.Parse_Segment(path)
                        segments += segment
                        gr_lines += gr_line
                        gr_arcs += gr_arc
                        gr_curves += gr_curve
                        
                for text in tag.find_all('text'):
                    gr_text.append(self.Parse_Text(text))


        layers.append('layers')
        chunk = modules + segments + gr_polys + gr_lines + gr_arcs + gr_curves + gr_text + vias + zones
        return layers, chunk



    def Get_Angle(self, centre, point):
        vec1 = centre[0] + 1j * centre[1]
        vec2 = point[0] + 1j * point[1]
        vec3 = vec2 - vec1
        return math.degrees(cmath.phase(vec3))

 
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
        lst = self.Svg_To_List(svg)
        a = SexpressionWriter()
        
        sexpression = a.List_To_Sexpression(lst)
        a.Save(sexpression)
        # self.Save(sexpression)

    def Run_Plugin(self, pcb_filename, svg_filename):
        
        infile = os.path.join(os.path.dirname(pcb_filename),svg_filename)

        svg = self.Load(infile)
        lst = self.Svg_To_List(svg)
        a = SexpressionWriter()
        
        sexpression = a.List_To_Sexpression(lst)
        a.Save(sexpression, pcb_filename)
        # self.Save(sexpression)
        

if __name__ == '__main__':
    e = PcbWrite()
    e.Run_Standalone()