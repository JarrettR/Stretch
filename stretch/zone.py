
from .colour import Colour
from .metadata import Metadata


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
        self.layers = ''
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

        xy_text = ''
        additional = ''

        for item in input:
                
            if item[0] == 'layer':
                self.layer = item[1]
                
            elif item[0] == 'hatch':
                self.hatch = item[1:]
                
            elif item[0] == 'polygon':
                for xy in item:
                    if item[0] == 'pts':
                        for xy in item:
                            self.polygon.append([xy[0], xy[1]])
                        
            else:
                self.metadata.append(item)       


    def To_SVG(self):

        xy_text = ''
        additional = ''

        for xy in self.polygon:
            xy_text += ' ' + str(float(xy[0]) * pxToMM)
            xy_text += ',' + str(float(xy[1]) * pxToMM)
                        
        
        additional += Metadata().Convert_Metadata_To_SVG(self.metadata)
            
        parameters = '<path style="fill:none;stroke-linecap:round;stroke-linejoin:miter;stroke-opacity:1'
        parameters += ';stroke:#' + Colour.Assign(self.layer)
        parameters += ';stroke-width:1mm'
        parameters += '" '
        parameters += 'd="M ' + xy_text + ' Z" '
        parameters += 'layer="' + self.layer + '" '
        parameters += 'type="zone">'
        parameters += additional
        parameters += '</path>'

        # print(parameters)
        return parameters

   
        
    def Parse_Zone(self, tag):
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

        style = tag['style']

        width = style[style.find('stroke-width:') + 13:]
        hatch = ['hatch', 'edge', width[0:width.find('mm')]]

        if tag.has_attr('layer'):
            layer = ['layer', tag['layer']]
        elif tag.parent.has_attr('inkscape:label'):
            #XML metadata trashed, try to recover from parent tag
            layer = ['layer', tag.parent['inkscape:label']]
        else:
            assert False, "Zone not in layer"
            
            
        path = parse_path(tag['d'])
        # print(tag)
        # print(tag['d'])
        # print(path)
        
        pts = ['pts']
        for point in path:
            xy = ['xy']
            xy.append(str(point.start.real / pxToMM))
            xy.append(str(point.start.imag / pxToMM))
            pts.append(xy)

        polygon = ['polygon', pts]
        
        content = tag.contents[0][0:-1]
        content = '[' + content + ' ]'
        # self.Save(content)
        data = json.loads(content)
        
        data.insert(3, layer)
        data.insert(5, hatch)
        data.insert(9, polygon)
                
        return data
