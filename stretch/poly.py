
from .colour import Colour
from svgpath import parse_path

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

pxToMM = 96 / 25.4
        
class Poly(object):

    def __init__(self):
        self.pts = []
        self.width = 0
        self.layer = ''
        self.fill = ''
        self.tstamp = ''
        self.status = 0
        
    def From_PCB(self, input):
        for item in input:
            if item[0] == 'pts':
                for xy in item:
                    if xy[0] == 'xy':
                        self.pts.append([xy[1], xy[2]])

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
            pcb = ['fp_poly']
        else:
            pcb = ['gr_poly']

        pts = ['pts']

        for item in self.pts:
            xy = ['xy'] + item
            pts += [xy]

        pcb.append(pts)
        if self.width != 0:
            pcb.append(['width', self.width])
        pcb.append(['layer', self.layer])
        if self.tstamp != '':
            pcb.append(['fill', self.fill])
        if self.tstamp != '':
            pcb.append(['tstamp', self.tstamp])
        if self.status != 0:
            pcb.append(['status', self.status])

        # print(pcb)
            
        return pcb

    def To_SVG(self, fp = False):
        if fp:
            polytype = 'fp_poly'
        else:
            polytype = 'gr_poly'
        
        xy_text = ''
                
        for xy in self.pts:
            xy_text += ' ' + str(float(xy[0]) * pxToMM)
            xy_text += ',' + str(float(xy[1]) * pxToMM)
   
        parameters = '<path style="stroke-linecap:round;stroke-linejoin:miter;stroke-opacity:1'
        parameters += ';fill:#' + Colour.Assign(self.layer)
        parameters += ';stroke:#' + Colour.Assign(self.layer)
        parameters += ';stroke-width:' + self.width + 'mm'
        parameters += '" '
        parameters += 'd="M ' + xy_text + ' Z" '
        parameters += 'layer="' + self.layer + '" '
        parameters += 'type="' + polytype + '" />'
        
        print(parameters)
        return parameters
        

    def From_SVG(self, tag):
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
            assert False, "Poly not in layer"
            
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

        self.pts = pts
        self.width = width
        self.layer = layer
