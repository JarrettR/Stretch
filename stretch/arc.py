
from .colour import Colour
from svgpath import parse_path
import math
import cmath

# https://github.com/KiCad/kicad-source-mirror/blob/93466fa1653191104c5e13231dfdc1640b272777/pcbnew/plugins/kicad/pcb_parser.cpp#L2119

# 0 gr_arc
# 1
#   0 start
#   1 66.66
#   2 99.99
# 2
#   0 end
#   1 66.66
#   2 99.99
# 3
#   0 angle
#   1 -90
# 4
#   0 layer
#   1 Edge.Cuts
# 5
#   0 width
#   1 0.05
# 6
#   0 tstamp
#   1 5E451B20


pxToMM = 96 / 25.4

class Arc(object):

    def __init__(self):
        self.start = []
        self.end = []
        self.angle = 0
        self.width = 0
        self.layer = ''
        self.fill = ''
        self.tstamp = ''
        self.status = 0

    def Get_Angle(self, centre, point):
        vec1 = centre[0] + 1j * centre[1]
        vec2 = point[0] + 1j * point[1]
        vec3 = vec2 - vec1
        return math.degrees(cmath.phase(vec3))


    def From_PCB(self, input):
        start = []
        end = []
        centre = []
        tstamp = ''

        for item in input:
            if type(item) == str:
                continue

            if item[0] == 'start':
                self.start.append(item[1])
                self.start.append(item[2])

            if item[0] == 'end':
                self.end.append(item[1])
                self.end.append(item[2])

            if item[0] == 'angle':
                self.angle = float(item[1])

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


    def To_PCB(self):
        pcb = ['gr_arc']

        pcb.append(['start'] + self.start)
        pcb.append(['end'] + self.end)
        pcb.append(['angle', self.angle])
        pcb.append(['width', self.width])
        pcb.append(['layer', self.layer])
        if self.fill:
            pcb.append(['fill', self.fill])
        if self.tstamp:
            pcb.append(['tstamp', self.tstamp])
        if self.status:
            pcb.append(['status', self.status])
            
        return pcb

    def To_SVG(self, fp = False):
        if fp:
            arctype = 'fp_arc'
        else:
            arctype = 'gr_arc'
        # m 486.60713,151.00183 a 9.5535717,9.5535717 0 0 1 -9.55357,9.55357
        # (rx ry x-axis-rotation large-arc-flag sweep-flag x y)
        
        #What KiCad calls 'start' is actually the arc centre,
        #'end' is actually arc/svg start
        #SVG end is actual end, we need to calculate centre instead
        centre = [(float(self.start[0]) * pxToMM), (float(self.start[1]) * pxToMM)]
        start = [(float(self.end[0]) * pxToMM), (float(self.end[1]) * pxToMM)]
  
        r = (start[0] - centre[0]) + ((centre[1] - start[1]) * 1j)

        angle = math.radians(self.angle)
        endangle = cmath.phase(r) - angle

        end_from_origin = cmath.rect(cmath.polar(r)[0], endangle)
        end = end_from_origin - r
        
        sweep = str(int(((angle / abs(angle)) + 1) / 2))
        if angle > cmath.pi:
            large = '1'
        else:
            large = '0'

        radius = "{:.6f}".format(round(cmath.polar(r)[0], 6))
        end_x = "{:.6f}".format(round(end.real, 6))
        end_y = "{:.6f}".format(round(-end.imag, 6))

        a = ' '.join(['a', radius + ',' + radius, '0', large, sweep, end_x + ',' + end_y])

        print(a)
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
        parameters += ';stroke:#' + Colour.Assign(self.layer)
        parameters += ';stroke-width:' + self.width + 'mm'
        parameters += '" '
        parameters += 'd="M ' + str(start[0]) + ',' + str(start[1]) + ' ' + a + '" '
        # parameters += 'id="path' + str(id) + '" '
        parameters += 'layer="' + self.layer + '" '
        parameters += 'type="' + arctype + '" '
        parameters += fill
        parameters += tstamp
        parameters += status
        parameters += '/>'
       
        return parameters
        
        
    def From_SVG(self, tag, segment):
        path = parse_path(tag['d'])
        style = tag['style']

        width = style[style.find('stroke-width:') + 13:]
        self.width = width[0:width.find('mm')]
        
        if tag.has_attr('layer'):
            self.layer = tag['layer']
        elif tag.parent.has_attr('inkscape:label'):
            #XML metadata trashed, try to recover from parent tag
            self.layer = tag.parent['inkscape:label']
        else:
            assert False, "Arc not in layer"

        #KiCad 'start' is actually centre, 'end' is actually svg start
        #SVG end is actual end, we need to calculate centre instead
        self.start = [str(path[0].center.real / pxToMM), str(path[0].center.imag / pxToMM)]
        self.end = [str(path[0].start.real / pxToMM), str(path[0].start.imag / pxToMM)]

        self.angle = str(path[0].delta)
            
        if tag.has_attr('fill') == True:
            self.fill = tag['fill']
            
        if tag.has_attr('status') == True:
            self.status = tag['status']
            
        if tag.has_attr('tstamp') == True:
            self.tstamp = tag['tstamp']

