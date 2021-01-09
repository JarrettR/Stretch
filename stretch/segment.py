#https://github.com/KiCad/kicad-source-mirror/blob/93466fa1653191104c5e13231dfdc1640b272777/pcbnew/plugins/kicad/pcb_parser.cpp#L4204

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

class Segment(object):

    def __init__(self):
        self.start = []
        self.end = []
        self.width = 0
        self.layer = ''
        self.net = 0
        self.tstamp = ''
        self.status = 0
        self.locked = False
    
    def From_SVG(self, tag):

        style = tag['style']

        width = style[style.find('stroke-width:') + 13:]
        self.width = width[0:width.find('mm')]

        if tag.has_attr('layer'):
            self.layer = tag['layer']
        elif tag.parent.has_attr('inkscape:label'):
            #XML metadata trashed, try to recover from parent tag
            self.layer = tag.parent['inkscape:label']
        else:
            assert False, "Path not in layer"

        paths = parse_path(tag['d'])

        segments = []

        for path in paths:
            segment = []
            start = ['start', str(path.start.real / pxToMM), str(path.start.imag / pxToMM)]
            end = ['end', str(path.end.real / pxToMM), str(path.end.imag / pxToMM)]

            segment = [ start, end, width, self.layer]

            if tag.has_attr('net'):
                segment.append(['net', tag['net']])
                
            if tag.has_attr('status'):
                segment.append(['status', tag['status']])
                
            if tag.has_attr('tstamp'):
                segment.append(['tstamp', tag['tstamp']])

            segment = ['segment'] + segment
            segments.append(segment)
            

        #return segments, gr_lines, gr_arcs, gr_curves
    
    def To_PCB(self):
        width = ['width', self.width]

        segments = []
        for path in paths:
            segment = []
            start = ['start', str(self.start[0]), str(self.start[1])]
            end = ['end', str(self.end[0]), str(self.end[1])]

            segment = [ start, end, width, self.layer]

            if self.net != 0:
                segment.append(['net', self.net])
                
            if self.status != 0:
                segment.append(['status', self.status])
                
            if self.tstamp != '':
                segment.append(['tstamp', self.tstamp])

            segment = ['segment'] + segment
            segments.append(segment)
            
        return segments

    def From_PCB(self, pcblist):
        if pcblist[0] != 'segment':
            assert False,"Segment: Not a segment"
            return None
            
        for item in pcblist:

            if item[0] != 'start':
                self.start = [input[1], input[2]]
                
            if item[0] != 'end':
                self.end = [input[1], input[2]]
                
            if item[0] != 'width':
                self.width = input[1]
                
            if item[0] != 'layer':
                self.layer = input[1]
                
            if item[0] != 'net':
                self.net = input[1]
                
            if item[0] != 'tstamp':
                self.tstamp = input[1]
                
            if item[0] != 'status':
                self.status = input[1]
        
        
    def To_SVG(self):
        tstamp = ''
        status = ''

        if self.tstamp != '':
            tstamp = 'tstamp="' + self.tstamp + '" '
        if self.status != '':
            status = 'status="' + self.status + '" '

        parameters = '<path style="fill:none;stroke-linecap:round;stroke-linejoin:miter;stroke-opacity:1'
        parameters += ';stroke:#' + self.Assign_Layer_Colour(self.layer)
        parameters += ';stroke-width:' + self.width + 'mm'
        parameters += '" '
        parameters += 'd="M ' + str(float(self.start[0]) * pxToMM) + ',' + str(float(self.start[1]) * pxToMM) + ' ' + str(float(self.end[0]) * pxToMM) + ',' + str(float(self.end[1]) * pxToMM) + '" '
        # parameters += 'id="path' + str(id) + '" '
        parameters += 'layer="' + self.layer + '" '
        parameters += 'type="segment" '
        parameters += 'net="' + self.net + '" '
        parameters += tstamp
        parameters += status
        parameters += '/>'

        # print(parameters)
        return parameters