
class Zone(object):

    def __init__(self):
        self.tstamp = ''
        
        
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

    def Convert_Zone_To_SVG(self, input, id):
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
        
        xy_text = ''
        additional = ''
        hide = ''

        for item in input:
                
            if item[0] == 'layer':
                layer = item[1]
                if layer in self.hiddenLayers:
                    hide = ';display:none'
                    
            if item[0] == 'layers':
                #todo
                layer = ''
                
            elif item[0] == 'hatch':
                width = item[2]
                
            elif item[0] == 'polygon':
                for xy in item[1]:
                    if xy[0] == 'xy':
                        xy_text += ' ' + str(float(xy[1]) * pxToMM)
                        xy_text += ',' + str(float(xy[2]) * pxToMM)
                        
            else:
                additional += self.Convert_Metadata_To_SVG(item)

            
        parameters = '<path style="fill:none;stroke-linecap:round;stroke-linejoin:miter;stroke-opacity:1'
        parameters += ';stroke:#' + self.Assign_Layer_Colour(layer)
        parameters += ';stroke-width:' + width + 'mm'
        parameters += hide
        parameters += '" '
        parameters += 'd="M ' + xy_text + ' Z" '
        parameters += 'id="path' + str(id) + '" '
        parameters += 'layer="' + layer + '" '
        parameters += 'type="zone">'
        parameters += additional
        parameters += '</path>'

        # print(parameters)
        return parameters

