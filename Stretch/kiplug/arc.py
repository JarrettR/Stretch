from .colour import Colour
from .svgpath import parse_path
import math
import cmath

# https://gitlab.com/kicad/code/kicad/-/blob/14c5f744ff2edd527dec17653fd7795cb6a74299/pcbnew/plugins/kicad/pcb_parser.cpp#L4765

# 0 gr_arc
# 1
#   0 start
#   1 66.66
#   2 99.99
# 2
#   0 mid
#   1 66.66
#   2 99.99
# 3
#   0 end
#   1 66.66
#   2 99.99
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
        self.mid = []
        self.end = []
        self.width = 0
        self.layer = ''
        self.fill = ''
        self.tstamp = ''
        self.net = ''
        self.status = 0

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

            if item[0] == 'mid':
                self.mid.append(item[1])
                self.mid.append(item[2])

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
                
            if item[0] == 'net':
                self.net = item[1]
                
            if item[0] == 'status':
                self.status = item[1]


    def To_PCB(self, fp = False):
        if fp:
            pcb = ['fp_arc']
        else:
            pcb = ['gr_arc']

        pcb.append(['start'] + self.start)
        pcb.append(['mid'] + self.mid)
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

    def To_SVG(self, fp = False):
        if fp:
            arctype = 'fp_arc'
        else:
            arctype = 'gr_arc'
        # m 486.60713,151.00183 a 9.5535717,9.5535717 0 0 1 -9.55357,9.55357
        # (rx ry x-axis-rotation large-arc-flag sweep-flag x y)
        
        start = [(float(self.start[0]) * pxToMM), (float(self.start[1]) * pxToMM)]
        mid = [(float(self.mid[0]) * pxToMM), (float(self.mid[1]) * pxToMM)]
        end = [(float(self.end[0]) * pxToMM), (float(self.end[1]) * pxToMM)]

        a = self.calcCirclePath(start, end, mid)

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
        parameters += ';stroke-width:' + self.width + 'mm'
        parameters += '" '
        parameters += 'd="' + a + '" '
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

        self.start = [str(path[0].start.real / pxToMM), str(path[0].start.imag / pxToMM)]
        self.mid = [str(path[0].point(0.5).real / pxToMM), str(path[0].point(0.5).imag / pxToMM)]
        self.end = [str(path[0].point(1).real / pxToMM), str(path[0].point(1).imag / pxToMM)]
            
        if tag.has_attr('fill') == True:
            self.fill = tag['fill']
            
        if tag.has_attr('status') == True:
            self.status = tag['status']
            
        if tag.has_attr('tstamp') == True:
            self.tstamp = tag['tstamp']

    def calcCirclePath(self, a, b, c):
        def dist(a, b):
            return math.sqrt(math.pow(a[0] - b[0], 2) + math.pow(a[1] - b[1], 2))


        A = dist(b, c)
        B = dist(c, a)
        C = dist(a, b)

        angle = math.acos((A*A + B*B - C*C)/(2*A*B))

        center = [0,0]
        
        temp = b[0]*b[0]+b[1]*b[1]
        bc = (a[0]*a[0] + a[1]*a[1] - temp)/2.0
        cd = (temp - c[0]*c[0] - c[1]*c[1])/2.0
        det = (a[0]-b[0])*(b[1]-c[1])-(b[0]-c[0])*(a[1]-b[1])

        if (abs(det) < 1.0e-6):
            center[0] = 1.0
            center[1] = 1.0
        else:
            det = 1/det
            center[0] = (bc*(b[1]-c[1])-cd*(a[1]-b[1]))*det
            center[1] = ((a[0]-b[0])*cd-(b[0]-c[0])*bc)*det
        r = math.sqrt((b[0]-center[0])*(b[0]-center[0])+(b[1]-center[1])*(b[1]-center[1]))

        #large arc flag
        if math.pi/2 > angle:
            laf = '1'
        else:
            laf = '0'

        #sweep flag
        if ((b[0] - a[0])*(c[1] - a[1]) - (b[1] - a[1])*(c[0] - a[0])) < 0:
            saf = '1'
        else:
            saf = '0'

        svg = ' '.join(['M', str(a[0]), str(a[1]), 'A', str(r), str(r), '0', laf, saf, str(b[0]), str(b[1])])

        return svg