
import math
from .colour import Colour

# https://github.com/KiCad/kicad-source-mirror/blob/93466fa1653191104c5e13231dfdc1640b272777/pcbnew/plugins/kicad/pcb_parser.cpp#L2209


# 0 gr_circle
# 1
#   0 center
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


class Circle(object):

    def __init__(self):
        self.center = []
        self.end = []
        self.width = '0'
        self.layer = ''
        self.fill = ''
        self.tstamp = ''
        self.status = ''
        
        
    def From_PCB(self, input):


        start = []
        end = []

        for item in input:
            if type(item) == str:
                continue

            if item[0] == 'center':
                self.center.append(float(item[1]))
                self.center.append(float(item[2]))

            if item[0] == 'end':
                self.end.append(float(item[1]))
                self.end.append(float(item[2]))

            # if item[0] == 'angle':
                # self.angle = item[1]
                # assert False,"Gr_circle: Please report this! Never seen before."

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
            pcb = ['fp_circle']
        else:
            pcb = ['gr_circle']

        pcb.append(['center'] + self.center)
        pcb.append(['end'] + self.end)
        pcb.append(['width', self.width])
        # pcb.append(['angle', self.angle])
        pcb.append(['layer', self.layer])
        if self.fill != '':
            pcb.append(['fill', self.fill])
        pcb.append(['tstamp', self.tstamp])
        pcb.append(['status', self.status])
            
        return pcb
        
    def To_SVG(self, fp = False):
        if fp:
            circletype = 'fp_circle'
        else:
            circletype = 'gr_circle'
        tstamp = ''
        status = ''
        fill = ''
    
        if self.fill != '':
            fill = 'fill="' + self.fill + '" '
        if self.tstamp != '':
            tstamp = 'tstamp="' + self.tstamp + '" '
        if self.status != '':
            status = 'status="' + str(self.status) + '" '
            
        r = abs(math.hypot(self.center[0] - self.end[0], self.center[1] - self.end[1]))

        parameters = '<circle style="stroke:none;stroke-linecap:round;stroke-linejoin:miter;fill-opacity:1'
        parameters += ';stroke:#' + Colour().Assign(self.layer)
        parameters += ';stroke-width:' + self.width + 'mm'
        parameters += '" '
        parameters += 'cx="' + str(self.center[0] * pxToMM) + '" '
        parameters += 'cy="' + str(self.center[1] * pxToMM) + '" '
        parameters += 'r="' + str(r * pxToMM) + '" '
        parameters += 'layer="' + self.layer + '" '
        parameters += 'type="' + circletype + '" '
        parameters += fill
        parameters += tstamp
        parameters += status
        parameters += '/>'

        return parameters

        
        
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
            assert False, "Circle not in layer"


        r = str((float(tag['r']) +float(tag['cx'] )) / pxToMM)
        x = str(float(tag['cx']) / pxToMM)
        y = str(float(tag['cy']) / pxToMM)
        self.center = [x, y]
        self.end = [r, y]
            
        if tag.has_attr('fill') == True:
            self.fill = tag['fill']
            
        if tag.has_attr('status') == True:
            self.status = tag['status']
            
        if tag.has_attr('tstamp') == True:
            self.tstamp = tag['tstamp']


