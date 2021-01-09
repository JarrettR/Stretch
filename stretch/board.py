from .segment import Segment

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

class Board(object):

    def __init__(self):
        self.general = ''
        self.paper = ''
        self.title_block = ''
        self.layers = ''
        self.setup = ''
        self.property = ''
        self.net = ''
        self.net_class = ''
        self.gr_arc = ''
        self.gr_curve = ''
        self.gr_line = ''
        self.gr_poly = ''
        self.gr_circle = ''
        self.gr_rect = ''
        self.gr_text = ''
        self.gr_dimension = ''
        self.module = ''
        self.footprint = ''
        self.segment = ''
        self.arc = ''
        self.group = ''
        self.via = ''
        self.zone = ''
        self.target = ''
        
        
    def From_PCB(self, pcb):
        # svg = ''
        dic = []
        segments = []

        i = 0
        for item in pcb:
            if type(item) is str:
                print(item)
            else:
            
                if item[0] == 'layers':
                    print(item[0])
                    
                elif item[0] == 'module':
                    print(item[0])

                elif item[0] == 'segment':
                    print(item[0])
                    # tag = BeautifulSoup(self.Convert_Segment_To_SVG(item, i), 'html.parser')
                    # layer = tag.path['layer']
                    # base.svg.find('g', {'inkscape:label': layer}, recursive=False).append(tag)

                elif item[0] == 'gr_line':
                    print(item[0])
                    # tag = BeautifulSoup(self.Convert_Gr_Line_To_SVG(item, i), 'html.parser')
                    # layer = tag.path['layer']
                    # base.svg.find('g', {'inkscape:label': layer}, recursive=False).append(tag)
                    
                elif item[0] == 'gr_poly':
                    print(item[0])
                    # tag = BeautifulSoup(self.Convert_Gr_Poly_To_SVG(item, i), 'html.parser')
                    # layer = tag.path['layer']
                    # base.svg.find('g', {'inkscape:label': layer}, recursive=False).append(tag)

                elif item[0] == 'gr_arc':
                    print(item[0])
                    # tag = BeautifulSoup(self.Convert_Gr_Arc_To_SVG(item, i), 'html.parser')
                    # layer = tag.path['layer']
                    # base.svg.find('g', {'inkscape:label': layer}, recursive=False).append(tag)

                elif item[0] == 'gr_curve':
                    print(item[0])
                    # tag = BeautifulSoup(self.Convert_Gr_Curve_To_SVG(item, i), 'html.parser')
                    # layer = tag.path['layer']
                    # base.svg.find('g', {'inkscape:label': layer}, recursive=False).append(tag)

                elif item[0] == 'gr_text':
                    print(item[0])
                    # tag = BeautifulSoup(self.Convert_Gr_Text_To_SVG(item, i), 'html.parser')
                    # layer = tag.find('text')['layer']
                    # base.svg.find('g', {'inkscape:label': layer}, recursive=False).append(tag)

                elif item[0] == 'zone':
                    print(item[0])
                    # tag = BeautifulSoup(self.Convert_Zone_To_SVG(item, i), 'html.parser')
                    # layer = tag.path['layer']
                    # if layer:
                        # base.svg.find('g', {'inkscape:label': layer}, recursive=False).append(tag)

                elif item[0] == 'via':
                    print(item[0])
                    # tag = BeautifulSoup(self.Convert_Via_To_SVG(item, i), 'html.parser')
                    # base.svg.find('g', {'inkscape:label': 'Vias'}, recursive=False).append(tag)
                    
                else:
                    print(item[0])
                    # svg = self.Convert_Metadata_To_SVG(item)
                    # base.svg.kicad.append(BeautifulSoup(svg, 'html.parser'))
                    
                    
    def To_SVG(self, items, base):
        # svg = ''
        dic = []
        segments = []
        #if items[0] != 'kicad_pcb':
        #    assert False,"kicad_pcb: Not a kicad_pcb"

        base.svg.append(BeautifulSoup('<kicad />', 'html.parser'))

        i = 0
        for item in items:
            if type(item) is str:
                print(item)
            else:
                if item[0] == 'layers':
                    layers = self.Convert_Layers_To_SVG(item)
                   
                    for layer in layers:
                        tag = BeautifulSoup(layer, 'html.parser')
                        base.svg.append(tag)
            i = i + 1
                             
        for item in items:
            if type(item) is str:
                print(item)
            else:
                if item[0] == 'module':
                    base.svg.append(self.Convert_Module_To_SVG(item, i))
            i = i + 1
            
        base.svg.append(BeautifulSoup('<g inkscape:label="Vias" inkscape:groupmode="layer" id="layervia" user="True" />', 'html.parser'))


        for item in items:
            if type(item) is str:
                print(item)
            else:
                # print(item[0])
                if item[0] == 'segment':
                    tag = BeautifulSoup(self.Convert_Segment_To_SVG(item, i), 'html.parser')
                    layer = tag.path['layer']
                    base.svg.find('g', {'inkscape:label': layer}, recursive=False).append(tag)

                elif item[0] == 'gr_line':
                    tag = BeautifulSoup(self.Convert_Gr_Line_To_SVG(item, i), 'html.parser')
                    layer = tag.path['layer']
                    base.svg.find('g', {'inkscape:label': layer}, recursive=False).append(tag)
                    
                elif item[0] == 'gr_poly':
                    tag = BeautifulSoup(self.Convert_Gr_Poly_To_SVG(item, i), 'html.parser')
                    layer = tag.path['layer']
                    base.svg.find('g', {'inkscape:label': layer}, recursive=False).append(tag)

                elif item[0] == 'gr_arc':
                    tag = BeautifulSoup(self.Convert_Gr_Arc_To_SVG(item, i), 'html.parser')
                    layer = tag.path['layer']
                    base.svg.find('g', {'inkscape:label': layer}, recursive=False).append(tag)

                elif item[0] == 'gr_curve':
                    tag = BeautifulSoup(self.Convert_Gr_Curve_To_SVG(item, i), 'html.parser')
                    layer = tag.path['layer']
                    base.svg.find('g', {'inkscape:label': layer}, recursive=False).append(tag)

                elif item[0] == 'gr_text':
                    tag = BeautifulSoup(self.Convert_Gr_Text_To_SVG(item, i), 'html.parser')
                    layer = tag.find('text')['layer']
                    base.svg.find('g', {'inkscape:label': layer}, recursive=False).append(tag)

                elif item[0] == 'zone':
                    tag = BeautifulSoup(self.Convert_Zone_To_SVG(item, i), 'html.parser')
                    layer = tag.path['layer']
                    if layer:
                        base.svg.find('g', {'inkscape:label': layer}, recursive=False).append(tag)

                elif item[0] == 'via':
                    tag = BeautifulSoup(self.Convert_Via_To_SVG(item, i), 'html.parser')
                    base.svg.find('g', {'inkscape:label': 'Vias'}, recursive=False).append(tag)
                    
                elif item[0] != 'layers' and item[0] != 'module':
                    # Already handled above
                    svg = self.Convert_Metadata_To_SVG(item)
                    base.svg.kicad.append(BeautifulSoup(svg, 'html.parser'))
                    
            i = i + 1
        dic.append({'segment': segments})

        if debug == True:
            svg = base.prettify("utf-8")
        else:
            svg = base.encode()
        
        return svg