    def Parse_Polys(self, tag):
        # 0 gr_poly
        # 1
        #   0 pts
        #   1
        #     0 xy
        #     1 147.6375
        #     2 120.9675
        #   2
        #     0 xy
        #     1 147.6375
        #     2 120.9675
        #   3
        #     ...
        # 2
        #   0 layer
        #   1 B.Cu
        # 3
        #   0 width
        #   1 0.1

        data = [tag['type']]
        style = tag['style']

        styletag = style[style.find('stroke-width:') + 13:]
        width = styletag[0:styletag.find('mm')]

        if tag.has_attr('layer'):
            layer = ['layer', tag['layer']]
        elif tag.parent.has_attr('inkscape:label'):
            #XML metadata trashed, try to recover from parent tag
            layer = ['layer', tag.parent['inkscape:label']]
        else:
            assert False, "Poly not in layer"
            
            
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

        data.append(pts)
        data.append(layer)
        data.append(['width', width])
        
                
        return data


    def Convert_Gr_Poly_To_SVG(self, input, id):
        # 0 gr_poly
        # 1
        #   0 pts
        #   1
        #     0 xy
        #     1 147.6375
        #     2 120.9675
        #   2
        #     0 xy
        #     1 147.6375
        #     2 120.9675
        #   3
        #     ...
        # 2
        #   0 layer
        #   1 B.Cu
        # 3
        #   0 width
        #   1 0.1
        
        xy_text = ''
        additional = ''
        hide = ''

        for item in input:
                
            if item[0] == 'layer':
                layer = item[1]
                
            elif item[0] == 'width':
                width = item[1]
                
            elif item[0] == 'pts':
                for xy in item:
                    if xy[0] == 'xy':
                        xy_text += ' ' + str(float(xy[1]) * pxToMM)
                        xy_text += ',' + str(float(xy[2]) * pxToMM)
                        
        if layer in self.hiddenLayers:
            hide = ';display:none'
            
        parameters = '<path style="stroke-linecap:round;stroke-linejoin:miter;stroke-opacity:1'
        parameters += ';fill:#' + self.Assign_Layer_Colour(layer)
        parameters += ';stroke:#' + self.Assign_Layer_Colour(layer)
        parameters += ';stroke-width:' + width + 'mm'
        parameters += hide
        parameters += '" '
        parameters += 'd="M ' + xy_text + ' Z" '
        parameters += 'id="path' + str(id) + '" '
        parameters += 'layer="' + layer + '" '
        parameters += 'type="gr_poly" />'
        
        # print(parameters)
        return parameters
        
