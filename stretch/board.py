from bs4 import BeautifulSoup
import json

from .arc import Arc
from .circle import Circle
from .curve import Curve
from .layers import Layers
from .line import Line
from .metadata import Metadata
from .module import Module
from .pad import Pad
from .poly import Poly
from .segment import Segment
from .text import Text
from .via import Via
from .zone import Zone

#https://github.com/KiCad/kicad-source-mirror/blob/93466fa1653191104c5e13231dfdc1640b272777/pcbnew/plugins/kicad/pcb_parser.cpp#L533

# kicad_pcb
# version
# host
# general
# page
# title_block
# layers
# setup
# net
# net_class
# module
# dimension
# gr_line
# gr_arc
# gr_text
# segment
# via
# zone

#Prettifies SVG output, but messes up text field spacing
debug = False

class Board(object):

    def __init__(self):
        self.general = ''
        self.paper = ''
        self.title_block = ''


        self.layers = Layers()
        # self.layers = ''
        self.setup = ''
        self.property = ''
        self.net = ''
        self.net_class = ''
        self.gr_arc = []
        self.gr_curve = []
        self.gr_line = []
        self.gr_poly = []
        self.gr_circle = []
        self.gr_rect = []
        self.gr_text = []
        self.gr_dimension = []
        self.module = []
        self.footprint = []
        self.segment = []
        self.arc = []
        self.group = ''
        self.via = []
        self.zone = []
        self.target = ''
        
        self.metadata = []
        
        
    def From_PCB(self, pcb):
    
        for item in pcb:
            if type(item) is str:
                print(item)
            else:
            
                if item[0] == 'layers':
                    self.layers = Layers()
                    self.layers.From_PCB(item)
                    
                elif item[0] == 'module':
                    module = Module()
                    module.From_PCB(item)
                    self.module.append(module)

                elif item[0] == 'segment':
                    segment = Segment()
                    segment.From_PCB(item)
                    self.segment.append(segment)
                    
                elif item[0] == 'gr_arc':
                    arc = Arc()
                    arc.From_PCB(item)
                    self.gr_arc.append(arc)
                    
                elif item[0] == 'gr_line':
                    line = Line()
                    line.From_PCB(item)
                    self.gr_line.append(line)
                    
                elif item[0] == 'gr_circle':
                    circle = Circle()
                    circle.From_PCB(item)
                    self.gr_circle.append(circle)
                    
                elif item[0] == 'gr_poly':
                    poly = Poly()
                    poly.From_PCB(item)
                    self.gr_poly.append(poly)
                    
                elif item[0] == 'gr_curve':
                    curve = Curve()
                    curve.From_PCB(item)
                    self.gr_curve.append(curve)
                    
                elif item[0] == 'gr_text':
                    print(item[0])
                    # tag = BeautifulSoup(self.Convert_Gr_Text_To_SVG(item, i), 'html.parser')
                    # layer = tag.find('text')['layer']
                    # base.svg.find('g', {'inkscape:label': layer}, recursive=False).append(tag)

                elif item[0] == 'zone':
                    zone = Zone()
                    zone.From_PCB(item)
                    self.zone.append(zone)

                elif item[0] == 'via':
                    via = Via()
                    via.From_PCB(item)
                    self.via.append(via)
                    
                else:
                    self.metadata.append(item)
                   
    def To_PCB(self):

        pcb = self.layers.To_PCB()
        # pcb += self.module.To_PCB() # TODO
        
        for item in self.segment:
            pcb += item.To_PCB()
        
        for item in self.gr_arc:
            pcb += item.To_PCB()
        
        for item in self.gr_line:
            pcb += item.To_PCB()
        
        for item in self.gr_circle:
            pcb += item.To_PCB()
        
        for item in self.gr_poly:
            pcb += item.To_PCB()
        
        for item in self.gr_curve:
            pcb += item.To_PCB()
        
        # for item in self.gr_text:
        #     pcb += item.To_PCB()
        
        for item in self.zone:
            pcb += item.To_PCB()

        for item in self.via:
            pcb += item.To_PCB()

        # for item in self.metadata:
        #     pcb += item.To_PCB()

        # print(pcb)
        return pcb
           
                    
    def To_SVG(self):

        base.svg.append(BeautifulSoup('<kicad />', 'html.parser'))


        layers = self.layers.To_SVG()
       
        for layer in layers:
            tag = BeautifulSoup(layer, 'html.parser')
            base.svg.append(tag)
                             

        base.svg.append(BeautifulSoup('<g inkscape:label="Vias" inkscape:groupmode="layer" id="layervia" user="True" />', 'html.parser'))


        for item in self.segment:
            tag = BeautifulSoup(item.To_SVG(), 'html.parser')
            layer = item.layer
            base.svg.find('g', {'inkscape:label': layer}, recursive=False).append(tag)
            
        for item in self.module:
            tag = item.To_SVG()
            layer = item.layer
            base.svg.find('g', {'inkscape:label': layer}, recursive=False).append(tag)
            
        for item in self.gr_line:
            tag = BeautifulSoup(item.To_SVG(), 'html.parser')
            layer = item.layer
            base.svg.find('g', {'inkscape:label': layer}, recursive=False).append(tag)
            
        for item in self.gr_poly:
            tag = BeautifulSoup(item.To_SVG(), 'html.parser')
            layer = item.layer
            base.svg.find('g', {'inkscape:label': layer}, recursive=False).append(tag)
                        
        for item in self.gr_arc:
            tag = BeautifulSoup(item.To_SVG(), 'html.parser')
            layer = item.layer
            base.svg.find('g', {'inkscape:label': layer}, recursive=False).append(tag)
            
        for item in self.gr_curve:
            tag = BeautifulSoup(item.To_SVG(), 'html.parser')
            layer = item.layer
            base.svg.find('g', {'inkscape:label': layer}, recursive=False).append(tag)
            
        for item in self.gr_circle:
            tag = BeautifulSoup(item.To_SVG(), 'html.parser')
            layer = item.layer
            base.svg.find('g', {'inkscape:label': layer}, recursive=False).append(tag)
            
        for item in self.via:
            tag = BeautifulSoup(item.To_SVG(), 'html.parser')
            base.svg.find('g', {'inkscape:label': 'Vias'}, recursive=False).append(tag)
        
        for item in self.zone:
            tag = BeautifulSoup(item.To_SVG(), 'html.parser')
            layer = item.layer
            if layer:
                base.svg.find('g', {'inkscape:label': layer}, recursive=False).append(tag)
                
        for item in self.metadata:
            tag = BeautifulSoup(Metadata().Convert_Metadata_To_SVG(item), 'html.parser')
            base.svg.kicad.append(tag)
            
        

                # elif item[0] == 'gr_text':
                    # tag = BeautifulSoup(self.Convert_Gr_Text_To_SVG(item, i), 'html.parser')
                    # layer = tag.find('text')['layer']
                    # base.svg.find('g', {'inkscape:label': layer}, recursive=False).append(tag)


        if debug == True:
            svg = base.prettify("utf-8")
        else:
            svg = base.encode()
        
        return svg
        
        
    def From_SVG(self, svg):
        self.layers = Layers()
        self.layers.From_SVG(svg)
        
    def From_SVG_old(self, svg):
        content = svg.svg.kicad.contents[0][0:-1]
        content = '[' + content + ' ]'
        # self.Save(content)
        meta = json.loads(content)
        # meta.insert(0, 'kicad_pcb')
        if meta[0] != 'kicad_pcb':
            meta.insert(0, 'kicad_pcb')

        lst = meta

        layers, chunk = self.Parse_Layers_Segments(svg)
        # print(layers_segments)

        lst.append(layers[::-1])
        lst = lst + chunk

        return lst
                  
    def Parse_Layers_Segments(self, svg):
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

        for tag in svg.svg.find_all('g'):
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
        
base = BeautifulSoup('''
    <?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->

<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   width="210mm"
   height="297mm"
   viewBox="0 0 210 297"
   version="1.1"
   id="svg8290"
   inkscape:version="0.92.4 (5da689c313, 2019-01-14)"
   sodipodi:docname="base.svg">
  <defs
     id="defs8284" />
  <sodipodi:namedview
     id="base"
     pagecolor="#000000"
     bordercolor="#666666"
     borderopacity="1.0"
     inkscape:pageopacity="0.0"
     inkscape:pageshadow="2"
     inkscape:zoom="0.7"
     inkscape:cx="-8.4507329"
     inkscape:cy="782.79942"
     inkscape:document-units="mm"
     inkscape:current-layer="svg8290"
     showgrid="false"
     inkscape:window-width="1920"
     inkscape:window-height="1137"
     inkscape:window-x="-8"
     inkscape:window-y="32"
     inkscape:window-maximized="1" />
  <metadata
     id="metadata1">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title />
      </cc:Work>
    </rdf:RDF>
  </metadata>
</svg>
''', 'html.parser')