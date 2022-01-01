# https://github.com/KiCad/kicad-source-mirror/blob/93466fa1653191104c5e13231dfdc1640b272777/pcbnew/plugins/kicad/pcb_parser.cpp#L4386

from .colour import Colour
from .metadata import Metadata
from .svgpath import parse_path


# 0 zone
# 1
#   0 net
#   1 16
# 2
#   0 net_name
#   1 GND
# 3
#   0 layer
#   1 B.Cu
# 4
#   0 tstamp
#   1 5EACCA92
# 5
#   0 hatch
#   1 edge
#   2 0.508
# 6
#   0 connect_pads
#   1
#     0 clearance
#     1 0.1524
# 7
#   0 min_thickness
#   1 0.1524
# 8
#   0 fill
#   1 yes
#   2
#     0 arc_segments
#     1 32
#   3
#     0 thermal_gap
#     1 0.1524
#   4
#     0 thermal_bridge_width
#     1 0.1525
# 9
#   0 polygon
#   1
#     0 pts
#     1
#       0 xy
#       1 147.6375
#       2 120.9675
#     2
#       0 xy
#       1 147.6375
#       2 120.9675
#     3
#       ...
# 10
#   0 filled_polygon
#   1
#     0 pts
#     1
#       0 xy
#       1 147.6375
#       2 120.9675
#     2
#       0 xy
#       1 147.6375
#       2 120.9675
#     3
#       ...

pxToMM = 96 / 25.4
        
        
class Zone(object):

    def __init__(self):
        self.net = ''
        self.net_name = ''
        self.layer = ''
        self.layers = []
        self.tstamp = ''
        self.hatch = ''
        self.priority = 0
        self.connect_pads = ''
        self.min_thickness = ''
        self.filled_areas_thickness = ''
        self.fill = ''
        self.keepout = ''
        self.polygon = []
        self.filled_polygon = []
        self.filled_segments = []
        self.name = ''
        
        # Most of these don't need to be handled
        self.metadata = []
     
    def From_PCB(self, input):
        # print(input)

        for item in input:
                
            if item[0] == 'net':
                self.net = item[1]

            elif item[0] == 'net_name':
                self.net_name = item[1]

            elif item[0] == 'layer':
                self.layer = item[1]

            elif item[0] == 'layers':
                for layer in item[1]:
                    self.layers.append(layer)
                
            elif item[0] == 'tstamp':
                self.tstamp = item[1]

            elif item[0] == 'hatch':
                self.hatch = item[1:]

            elif item[0] == 'priority':
                self.priority = item[1]

            elif item[0] == 'connect_pads':
                self.connect_pads = item[1]

            elif item[0] == 'min_thickness':
                self.min_thickness = item[1]

            elif item[0] == 'filled_areas_thickness':
                self.filled_areas_thickness = item[1]

            elif item[0] == 'fill':
                self.fill = item[1]

            elif item[0] == 'keepout':
                self.keepout = item[1]

            elif item[0] == 'name':
                self.name = item[1]
                
            elif item[0] == 'polygon':
                for xy in item[1]:
                    if xy[0] == 'xy':
                        self.polygon.append([xy[1], xy[2]])
                
            elif item[0] == 'filled_polygon':
                for xy in item[1]:
                    if xy[0] == 'xy':
                        self.filled_polygon.append([xy[1], xy[2]])
                
            elif item[0] == 'filled_segments':
                for xy in item[1]:
                    if xy[0] == 'xy':
                        self.filled_segments.append([xy[1], xy[2]])
                        


    def To_PCB(self):
        pcb = ['zone']

        if self.net:
            pcb.append(['net', self.net])
        if self.net_name:
            pcb.append(['net_name', self.net_name])
        if self.layer:
            pcb.append(['layer', self.layer])
        if len(self.layers) > 0:
            pcb.append(['layers', self.layers])
        if self.tstamp:
            pcb.append(['tstamp', self.tstamp])
        if self.hatch:
            pcb.append(['hatch'] + self.hatch)
        if self.priority:
            pcb.append(['priority', self.priority])
        if self.connect_pads:
            pcb.append(['connect_pads', self.connect_pads])
        if self.min_thickness:
            pcb.append(['min_thickness', self.min_thickness])
        if self.filled_areas_thickness:
            cb.append(['filled_areas_thickness', self.filled_areas_thickness])
        if self.fill:
            pcb.append(['fill', self.fill])
        if self.keepout:
            pcb.append(['keepout', self.keepout])

        if len(self.polygon) > 0:
            polygon = ['pts']
            for item in self.polygon:
                pt = ['xy'] + item
                polygon.append(pt)
            polygon = ['polygon'] + [polygon]
            pcb.append(polygon)

        if len(self.filled_polygon) > 0:
            filled_polygon = ['filled_polygon']
            for item in self.filled_polygon:
                xy = ['xy'] + item
                filled_polygon += [xy]
            pcb.append(filled_polygon)

        if len(self.filled_segments) > 0:
            filled_segments = ['filled_segments']
            for item in self.filled_segments:
                xy = ['xy'] + item
                filled_segments += [xy]
                pcb.append(filled_segments)

        if self.name:
            pcb.append(['name', self.name])

        return pcb
        
    def To_SVG(self):

        xy_text = ''

        if len(self.polygon) > 0:
            for xy in self.polygon:
                xy_text += ' ' + str(float(xy[0]) * pxToMM)
                xy_text += ',' + str(float(xy[1]) * pxToMM)
        elif len(self.filled_polygon) > 0:
            for xy in self.filled_polygon:
                xy_text += ' ' + str(float(xy[0]) * pxToMM)
                xy_text += ',' + str(float(xy[1]) * pxToMM)
                        
        
        
        net = ''
        if self.net != '':
            net = 'net="' + self.net + '" '
        
        net_name = ''
        if self.net_name != '':
            net_name = 'net_name="' + self.net_name + '" '

        tstamp = ''
        if self.tstamp != '':
            tstamp = 'tstamp="' + self.tstamp + '" '
        
        hatch = ''
        if self.hatch != '':
            hatch = 'hatch="' + self.hatch[0] + '" '
            hatch += 'hatch_distance="' + self.hatch[1] + '" '
            
        priority = ''
        if self.priority != '':
            priority = 'priority="' + str(self.priority) + '" '

        connect_pads = ''
        # if self.connect_pads != '':
        #     connect_pads = 'connect_pads="' + self.connect_pads + '" '
              
        min_thickness = ''      
        if self.min_thickness != '':
            min_thickness = 'min_thickness="' + self.min_thickness + '" '
              
        filled_areas_thickness = ''      
        if self.filled_areas_thickness != '':
            filled_areas_thickness = 'filled_areas_thickness="' + self.filled_areas_thickness + '" '
        
        fill = ''
        if self.fill != '':
            fill = 'fill="' + self.fill + '" '
        
        keepout = ''
        if self.keepout != '':
            keepout = 'keepout="' + self.keepout + '" '
        
        name = ''
        if self.name != '':
            name = 'name="' + self.name + '" '
            
        parameters = '<path style="fill:none;stroke-linecap:round;stroke-linejoin:miter;stroke-opacity:1'
        parameters += ';stroke:#' + Colour.Assign(self.layer)
        parameters += ';stroke-width:1mm'
        parameters += '" '
        parameters += 'd="M ' + xy_text + ' Z" '
        parameters += 'layer="' + self.layer + '" '
        parameters += net
        parameters += net_name
        parameters += tstamp
        parameters += hatch
        parameters += priority
        parameters += connect_pads
        parameters += min_thickness
        parameters += filled_areas_thickness
        parameters += fill
        parameters += keepout
        parameters += name
        parameters += 'type="zone">'
        parameters += '</path>'

        # print(parameters)
        return parameters

   

    def From_SVG(self, tag, path):
        data = [tag['type']]
        style = tag['style']

        styletag = style[style.find('stroke-width:') + 13:]
        width = styletag[0:styletag.find('mm')]

        if tag.has_attr('layer'):
            layer = tag['layer']
        elif tag.parent.has_attr('inkscape:label'):
            #XML metadata trashed, try to recover from parent tag
            layer = tag.parent['inkscape:label']
        else:
            assert False, "Zone not in layer"
            
        path = parse_path(tag['d'])
        
        pts = []
        for point in path:
            xy = []
            xy.append(str(point.start.real / pxToMM))
            xy.append(str(point.start.imag / pxToMM))
            pts.append(xy)

        xy = []
        xy.append(str(path[0].start.real / pxToMM))
        xy.append(str(path[0].start.imag / pxToMM))
        pts.append(xy)


        if tag.has_attr('net'):
            self.net = tag['net']
        if tag.has_attr('net_name'):
            self.net_name = tag['net_name']
        if tag.has_attr('tstamp'):
            self.tstamp = tag['tstamp']
        if tag.has_attr('hatch'):
            self.hatch = [tag['hatch'], tag['hatch_distance']]
        if tag.has_attr('priority'):
            self.priority = tag['priority']
        if tag.has_attr('connect_pads'):
            self.connect_pads = tag['connect_pads']
        if tag.has_attr('min_thickness'):
            self.min_thickness = tag['min_thickness']
        if tag.has_attr('filled_areas_thickness'):
            self.filled_areas_thickness = tag['filled_areas_thickness']
        if tag.has_attr('fill'):
            self.fill = tag['fill']
        if tag.has_attr('keepout'):
            self.keepout = tag['keepout']
        if tag.has_attr('name'):
            self.name = tag['name']

        self.polygon = pts
        self.width = width
        self.layer = layer
