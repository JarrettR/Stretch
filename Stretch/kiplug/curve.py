
from .colour import Colour
from .svgpath import parse_path

# 0 gr_curve
# 1
#   0 pts
#   1
#       0 xy
#       1 99.99
#       2 99.99
#   2
#       0 xy
#       1 99.99
#       2 99.99
#   3
#       0 xy
#       1 99.99
#       2 99.99
#   4
#       0 xy
#       1 99.99
#       2 99.99
# 2
#   0 layer
#   1 Edge.Cuts
# 3
#   0 width
#   1 0.05
# 4
#   0 tstamp
#   1 5E451B20

pxToMM = 96 / 25.4


class Curve(object):

    def __init__(self):
        self.pts = []
        self.width = 0
        self.layer = ''
        self.fill = ''
        self.tstamp = ''
        self.status = ''
      
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
            pcb = ['fp_curve']
        else:
            pcb = ['gr_curve']

        pts = ['pts']

        for item in self.pts:
            xy = ['xy'] + item
            pts += [xy]

        pcb.append(pts)
        pcb.append(['layer', self.layer])
        pcb.append(['width', self.width])
        # pcb.append(['fill', self.fill])
        pcb.append(['tstamp', self.tstamp])
        pcb.append(['status', self.status])
                        
        return pcb 
                
    def To_SVG(self, fp = False):
        if fp:
            polytype = 'fp_curve'
        else:
            polytype = 'gr_curve'
        

        points = []
        tstamp = ''
        status = ''
        fill = ''

        #This might have a problem with random list ordering in certain versions of Python
        for xy in self.pts:
            points.append(float(xy[0]))
            points.append(float(xy[1]))

        if self.tstamp != '':
            tstamp = 'tstamp="' + self.tstamp + '" '
        if self.status != '':
            status = 'status="' + self.status + '" '
        if self.fill != '':
            fill = 'fill="' + self.fill + '" '


        parameters = '<path style="fill:none;stroke-linecap:round;stroke-linejoin:miter;stroke-opacity:1'
        parameters += ';stroke:#' + Colour().Assign(self.layer)
        parameters += ';stroke-width:' + self.width + 'mm'
        parameters += '" '
        parameters += 'd="M ' + str(points[0] * pxToMM) + ',' + str(points[1] * pxToMM) + ' C '
        parameters += str(points[2] * pxToMM) + ',' + str(points[3] * pxToMM) + ' '
        parameters += str(points[4] * pxToMM) + ',' + str(points[5] * pxToMM) + ' '
        parameters += str(points[6] * pxToMM) + ',' + str(points[7] * pxToMM) + '" '
        parameters += 'layer="' + self.layer + '" '
        parameters += 'type="gr_curve" '
        parameters += tstamp
        parameters += status
        parameters += fill
        parameters += '/>'

        return parameters

  
    def From_SVG(self, tag):
        style = tag['style']

        styletag = style[style.find('stroke-width:') + 13:]
        width = styletag[0:styletag.find('mm')]

        if tag.has_attr('layer'):
            layer = tag['layer']
        elif tag.parent.has_attr('inkscape:label'):
            #XML metadata trashed, try to recover from parent tag
            layer = tag.parent['inkscape:label']
        else:
            assert False, "Curve not in layer"
            
        #Todo: fix up this... 
        #----------------
        # path = parse_path(tag['d'])
        
        # pts = []
        # for point in path:
        #     xy = []
        #     xy.append(str(point.start.real / pxToMM))
        #     xy.append(str(point.start.imag / pxToMM))
        #     pts.append(xy)

        # xy = []
        # xy.append(str(path[0].start.real / pxToMM))
        # xy.append(str(path[0].start.imag / pxToMM))
        # pts.append(xy)
        #----------------
        #Because this old method is real bad:

        xy_float = 4 * [0.0]

        unparsed_path = tag['d'].split(' ')
        xy_str = unparsed_path[1].split(',')
        xy_float[0] = [float(xy_str[0]), float(xy_str[1])]
        xy_str = unparsed_path[3].split(',')
        xy_float[1] = [float(xy_str[0]), float(xy_str[1])]
        xy_str = unparsed_path[4].split(',')
        xy_float[2] = [float(xy_str[0]), float(xy_str[1])]
        xy_str = unparsed_path[5].split(',')
        xy_float[3] = [float(xy_str[0]), float(xy_str[1])]
        
        
        #relative / absolute compensation
        if unparsed_path[2] == 'c':
            xy_float[1][0] = xy_float[0][0] - xy_float[1][0] * -1
            xy_float[1][1] = xy_float[0][1] - xy_float[1][1] * -1
            xy_float[2][0] = xy_float[0][0] - xy_float[2][0] * -1
            xy_float[2][1] = xy_float[0][1] - xy_float[2][1] * -1
            xy_float[3][0] = xy_float[0][0] - xy_float[3][0] * -1
            xy_float[3][1] = xy_float[0][1] - xy_float[3][1] * -1
        
        
        xy = [str(xy_float[0][0] / pxToMM), str(xy_float[0][1] / pxToMM)]
        
        pts = [xy]
        
        xy = [str(xy_float[1][0] / pxToMM), str(xy_float[1][1] / pxToMM)]
        pts.append(xy)

        xy = [str(xy_float[2][0] / pxToMM), str(xy_float[2][1] / pxToMM)]
        pts.append(xy)

        xy = [str(xy_float[3][0] / pxToMM), str(xy_float[3][1] / pxToMM)]
        pts.append(xy)


        self.pts = pts
        self.width = width
        self.layer = layer

        if tag.has_attr('tstamp'):
            self.tstamp = tag['tstamp']
        if tag.has_attr('fill'):
            self.fill = tag['fill']
        if tag.has_attr('status'):
            self.status = tag['status']
            
        