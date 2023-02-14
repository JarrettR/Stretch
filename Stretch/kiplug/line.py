
from .colour import Colour

# https://github.com/KiCad/kicad-source-mirror/blob/93466fa1653191104c5e13231dfdc1640b272777/pcbnew/plugins/kicad/pcb_parser.cpp#L2209


# 0 gr_line
# 1
#   0 start
#   1 66.66
#   2 99.99
# 2
#   0 end
#   1 66.66
#   2 99.99
# 3
#   0 layer
#   1 Edge.Cuts
# 4
#   0 width
#   1 0.05
# 5
#   0 tstamp
#   1 5E451B20


pxToMM = 96 / 25.4


class Line(object):

    def __init__(self):
        self.start = []
        self.end = []
        self.width = 0
        self.layer = ''
        self.fill = ''
        self.tstamp = ''
        self.status = ''
        
        
    def From_PCB(self, input):


        start = []
        end = []

        for item in input:
            if type(item) == str:
                #if item == 'gr_line' or item == 'fp_line':
                continue

            if item[0] == 'start':
                self.start.append(item[1])
                self.start.append(item[2])

            if item[0] == 'end':
                self.end.append(item[1])
                self.end.append(item[2])

            if item[0] == 'layer':
                self.layer = item[1]

            if item[0] == 'width':
                self.width = item[1]
                
            if item[0] == 'fill':
                self.fill = item[1]

            if item[0] == 'tstamp':
                self.tstamp = item[1]
                
            if item[0] == 'status':
                self.status = item[1]

    def To_PCB(self, fp = False):
        pcb = []
        if fp:
            pcb = ['fp_line']
        else:
            pcb = ['gr_line']

        pcb.append(['start'] + self.start)
        pcb.append(['end'] + self.end)
        pcb.append(['width', self.width])
        pcb.append(['layer', self.layer])
        if self.fill:
            pcb.append(['fill', self.fill])
        if self.tstamp:
            pcb.append(['tstamp', self.tstamp])
        if self.status:
            pcb.append(['status', self.status])
            
        return pcb
        
    def From_SVG(self, tag, path):
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


        self.start = [str(path.start.real / pxToMM), str(path.start.imag / pxToMM)]
        self.end = [str(path.end.real / pxToMM), str(path.end.imag / pxToMM)]

            
        if tag.has_attr('fill') == True:
            self.fill = tag['fill']
            
        if tag.has_attr('status') == True:
            self.status = tag['status']
            
        if tag.has_attr('tstamp') == True:
            self.tstamp = tag['tstamp']



    def To_SVG(self, fp = False):
        if fp:
            linetype = 'fp_line'
        else:
            linetype = 'gr_line'
        
        tstamp = ''
        status = ''
        fill = ''
    
        if self.fill != '':
            fill = 'fill="' + self.fill + '" '
        if self.tstamp != '':
            tstamp = 'tstamp="' + self.tstamp + '" '
        if self.status != '':
            status = 'status="' + str(self.status) + '" '

        parameters = '<path style="fill:none;stroke-linecap:round;stroke-linejoin:miter;stroke-opacity:1'
        parameters += ';stroke:#' + Colour().Assign(self.layer)
        parameters += ';stroke-width:' + str(self.width) + 'mm'
        parameters += '" '
        parameters += 'd="M ' + str(float(self.start[0]) * pxToMM) + ',' + str(float(self.start[1]) * pxToMM) + ' ' + str(float(self.end[0]) * pxToMM) + ',' + str(float(self.end[1]) * pxToMM) + '" '
        # parameters += 'id="path' + str(id) + '" '
        parameters += 'layer="' + self.layer + '" '
        parameters += 'type="' + linetype + '" '
        parameters += fill
        parameters += tstamp
        parameters += status
        parameters += '/>'

        return parameters

