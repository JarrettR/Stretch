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
        gr_curves = []
        gr_polys = []

        for path in paths:
            segment = []
            start = ['start', str(path.start.real / pxToMM), str(path.start.imag / pxToMM)]
            end = ['end', str(path.end.real / pxToMM), str(path.end.imag / pxToMM)]

            segment = [ start, end, width, name]

            if tag.has_attr('net'):
                segment.append(['net', tag['net']])
                
            if tag.has_attr('status'):
                segment.append(['status', tag['status']])
                
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
            elif tag['type'] == 'gr_curve':
                gr_curves.append(self.Parse_Curves(tag, segment))
            else:
                print(tag)
                assert False,"Gr_line / segments: Nobody knows!"
                
            segments.reverse()
            gr_lines.reverse()
            gr_arcs.reverse()
            gr_curves.reverse()

        return segments, gr_lines, gr_arcs, gr_curves

    def Convert_Segment_To_SVG(self, input, id):
        # 0 segment
        # 1
        #   0 start
        #   1 66.66
        #   2 99.99
        # 2
        #   0 end
        #   1 66.66
        #   2 99.99
        # 3
        #   0 width
        #   1 0.25
        # 4
        #   0 layer
        #   1 B.Cu
        # 5
        #   0 net
        #   1 1

        start = []
        end = []

        if input[0] != 'segment':
            assert False,"Segment: Not a segment"
            return None

        if input[1][0] != 'start':
            assert False,"Segment: Start out of order"
            return None

        start.append(input[1][1])
        start.append(input[1][2])

        if input[2][0] != 'end':
            assert False,"Segment: End out of order"
            return None

        end.append(input[2][1])
        end.append(input[2][2])

        if input[3][0] != 'width':
            assert False,"Segment: Width out of order"
            return None

        width = input[3][1]

        if input[4][0] != 'layer':
            assert False,"Segment: Layer out of order"
            return None

        layer = input[4][1]

        if input[5][0] != 'net':
            assert False,"Segment: Net out of order"
            return None

        net = input[5][1]

        tstamp = ''
        status = ''

        if len(input) > 6:
            if input[6][0] == 'tstamp':
                tstamp = 'tstamp="' + input[6][1] + '" '
            if input[6][0] == 'status':
                status = 'status="' + input[6][1] + '" '
        if len(input) > 7:
            if input[7][0] == 'tstamp':
                tstamp = 'tstamp="' + input[7][1] + '" '
            if input[7][0] == 'status':
                status = 'status="' + input[7][1] + '" '

        parameters = '<path style="fill:none;stroke-linecap:round;stroke-linejoin:miter;stroke-opacity:1'
        parameters += ';stroke:#' + self.Assign_Layer_Colour(layer)
        parameters += ';stroke-width:' + width + 'mm'
        parameters += '" '
        parameters += 'd="M ' + str(float(start[0]) * pxToMM) + ',' + str(float(start[1]) * pxToMM) + ' ' + str(float(end[0]) * pxToMM) + ',' + str(float(end[1]) * pxToMM) + '" '
        # parameters += 'd="M ' + start[0] + ',' + start[1] + ' ' + end[0] + ',' + end[1] + '" '
        parameters += 'id="path' + str(id) + '" '
        parameters += 'layer="' + layer + '" '
        parameters += 'type="segment" '
        parameters += 'net="' + net + '" '
        parameters += tstamp
        parameters += status
        parameters += '/>'

        # print(parameters)
        return parameters