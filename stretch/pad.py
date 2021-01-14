
from .colour import Colour

# https://github.com/KiCad/kicad-source-mirror/blob/93466fa1653191104c5e13231dfdc1640b272777/pcbnew/plugins/kicad/pcb_parser.cpp#L3530
# 0 pad
# 1 1/2/3
# 2 smd
# 3 rect
# 4
#   0 at
#   1 66.66
#   2 99.99
#   2 180
# 5
#   0 size
#   1 0.9
#   2 1.2
# 6
#   0 layers
#   1 F.Cu
#   2 F.Paste
#   3 F.Mask
# 7
#   0 net
#   1 16
#   2 Net-(D4-Pad1)
       

pxToMM = 96 / 25.4 
        
class Pad(object):

    def __init__(self):
        self.name = ''
        self.attribute = ''
        self.shape = ''
        self.size = []
        self.at = []
        self.rect_delta = []
        self.drill = []
        self.layers = []
        self.net = 0
        self.pinfunction = ''
        self.die_length = ''
        self.solder_mask_margin = ''
        self.solder_paste_margin = ''
        self.solder_paste_margin_ratio = ''
        self.clearance = ''
        self.zone_connect = ''
        self.thermal_width = ''
        self.thermal_gap = ''
        self.roundrect_rratio = ''
        self.chamfer_ratio = ''
        self.chamfer = ''
        self.property = ''
        self.options = ''
        self.primitives = ''
        self.remove_unused_layers = ''
        self.keep_end_layers = ''
        self.tstamp = ''
        
    def From_PCB(self, input):

        at = []
        size = []
        layers = []
        roundrect_rratio = ''
        net = ''
        drill = ''
        rotate = ''

        if input[0] != 'pad':
            assert False,"Pad: Not a pad"
            return None

        self.name = input[1]

        self.attribute = input[2]

        self.shape = input[3]

        for item in input[4:]:
            if item[0] == 'size':
                self.size = item[1:]
                
            if item[0] == 'at':
                for at in item[1:]:
                    self.at.append(float(at))
                    
            #Todo: proper handling for many of these
            if item[0] == 'rect_delta':
                self.rect_delta = item[1]
            if item[0] == 'drill':
                self.drill = item[1] 
            if item[0] == 'layers':
                for layer in item[1:]:
                    self.layers.append(layer)
            if item[0] == 'net':
                self.net = item[1] 
            if item[0] == 'pinfunction':
                self.pinfunction = item[1] 
            if item[0] == 'die_length':
                self.die_length = item[1] 
            if item[0] == 'solder_mask_margin':
                self.solder_mask_margin = item[1] 
            if item[0] == 'solder_paste_margin':
                self.solder_paste_margin = item[1] 
            if item[0] == 'solder_paste_margin_ratio':
                self.solder_paste_margin_ratio = item[1] 
            if item[0] == 'clearance':
                self.clearance = item[1] 
            if item[0] == 'zone_connect':
                self.zone_connect = item[1] 
            if item[0] == 'thermal_width':
                self.thermal_width = item[1] 
            if item[0] == 'thermal_gap':
                self.thermal_gap = item[1] 
            if item[0] == 'roundrect_rratio':
                self.roundrect_rratio = item[1] 
            if item[0] == 'chamfer_ratio':
                self.chamfer_ratio = item[1] 
            if item[0] == 'chamfer':
                self.chamfer = item[1] 
            if item[0] == 'property':
                self.property = item[1] 
            if item[0] == 'options':
                self.options = item[1] 
            if item[0] == 'primitives':
                self.primitives = item[1] 
            if item[0] == 'remove_unused_layers':
                self.remove_unused_layers = item[1] 
            if item[0] == 'keep_end_layers':
                self.keep_end_layers = item[1] 
            if item[0] == 'tstamp':
                self.tstamp = item[1] 



    def To_SVG(self):

        layers = []
        roundrect_rratio = ''
        net = ''
        drill = ''
        rotate = ''
        parameters = ''

        if len(self.at) > 2:
            # start = self.at[0] + self.at[1] * 1j
            # angle = math.radians(float(row[3]) - r_offset)
            # endangle = cmath.phase(start) - angle
            # end = cmath.rect(cmath.polar(start)[0], endangle)
            
            # at[0] = end.real 
            # at[1] = end.imag
            
            # rotate += 'transform=rotate(' + str(float(row[3]) - r_offset) + ') '
            rotate += 'rotate = ' + str(float(self.at[2])) + ' '
                        
        if self.roundrect_rratio != '':
            roundrect_rratio = 'roundrect_rratio="' + self.roundrect_rratio + '"'

        if len(self.drill) > 0:
            drill = 'drill="' + self.drill[1] + '" '

        # if row[0] == 'net':
            # net = 'net="' + row[1] + '" '
            # net += 'netname="' + row[2] + '"'

        svg = ''
        svgsize = ''
        roundcorners = ''
        first = True
        
        if self.shape == 'rect':

            # Corner coordinates to centre coordinate system
            x = self.at[0] - float(self.size[0]) / 2
            y = self.at[1] - float(self.size[1]) / 2

            parameters += '<rect style="stroke:none;stroke-linecap:round;stroke-linejoin:miter;fill-opacity:1'
            svgsize += 'x="' + str(x * pxToMM) + '" '
            svgsize += 'y="' + str(y * pxToMM) + '" '
            svgsize += 'width="' + str(float(self.size[0])  * pxToMM) + '" '
            svgsize += 'height="' + str(float(self.size[1])  * pxToMM) + '" '
            
        elif self.shape == 'roundrect':
            
            # Corner coordinates to centre coordinate system
            x = self.at[0] - float(self.size[0]) / 2
            y = self.at[1] - float(self.size[1]) / 2

            parameters += '<rect style="stroke:none;stroke-linecap:round;stroke-linejoin:miter;fill-opacity:1'
            roundcorners += 'rx="' + str(float(self.size[0]) * float(self.roundrect_rratio)  * pxToMM) + '" '
            roundcorners += 'ry="' + str(float(self.size[1]) * float(self.roundrect_rratio)  * pxToMM) + '" '
            svgsize += 'x="' + str(x * pxToMM) + '" '
            svgsize += 'y="' + str(y * pxToMM) + '" '
            svgsize += 'width="' + str(float(self.size[0])  * pxToMM) + '" '
            svgsize += 'height="' + str(float(self.size[1])  * pxToMM) + '" '
            
        elif self.shape == 'circle':
            parameters += '<circle style="stroke:none;stroke-linecap:round;stroke-linejoin:miter;fill-opacity:1'
            svgsize += 'cx="' + str(self.at[0] * pxToMM) + '" '
            svgsize += 'cy="' + str(self.at[1] * pxToMM) + '" '
            svgsize += 'r="' + str(float(self.size[0])  * (pxToMM / 2)) + '" '
            svgsize += 'height="' + str(float(self.size[1])  * pxToMM) + '" '
            
        elif self.shape == 'oval':
            parameters += '<circle style="stroke:none;stroke-linecap:round;stroke-linejoin:miter;fill-opacity:1'
            svgsize += 'cx="' + str(self.at[0] * pxToMM) + '" '
            svgsize += 'cy="' + str(self.at[1] * pxToMM) + '" '
            svgsize += 'r="' + str(float(self.size[0])  * (pxToMM / 2)) + '" '
            svgsize += 'height="' + str(float(self.size[1])  * pxToMM) + '" '
            
        elif self.shape == 'custom':
            # todo: Setting custom shape to rect for now
            x = at[0] - float(self.size[0]) / 2
            y = at[1] - float(self.size[1]) / 2

            parameters += '<rect style="stroke:none;stroke-linecap:round;stroke-linejoin:miter;fill-opacity:1'
            svgsize += 'x="' + str(x * pxToMM) + '" '
            svgsize += 'y="' + str(y * pxToMM) + '" '
            svgsize += 'width="' + str(float(self.size[0])  * pxToMM) + '" '
            svgsize += 'height="' + str(float(self.size[1])  * pxToMM) + '" '
            
        else:
            assert False,"Pad: Unfamiliar shape: " + shape
            return None

        parameters += ';fill:#' + Colour.Assign(self.layers[0])
        parameters += '" '
        parameters += svgsize
        parameters += roundcorners
        parameters += roundrect_rratio
        parameters += net
        parameters += rotate
        parameters += drill
        if first == True:
            parameters += 'first="True"'
            parameters += 'layers="' + ','.join(self.layers) + '"'
        parameters += '/>'

        svg += parameters
        #print(parameters)
        return svg


    def Parse_Pad(self, tag, padtype):
        # print(tag['id'])

        if tag.has_attr('first') == False:
            return None

        pin = tag['pin']
        process = tag['process']

        if padtype == 'rect':

            width = float(tag['width']) / pxToMM
            height = float(tag['height']) / pxToMM
            x = str((float(tag['x']) / pxToMM) + (width / 2))
            y = str((float(tag['y']) / pxToMM) + (height / 2))
            width = str(width)
            height = str(height)

            size = ['size', width, height]

        elif padtype == 'circle':
            r = str((float(tag['r']) * 2) / pxToMM)
            size = ['size', r, r]
            x = str(float(tag['cx']) / pxToMM)
            y = str(float(tag['cy']) / pxToMM)


        at = ['at', x, y]
        if tag.has_attr('rotate'):
            at.append(tag['rotate'])

        pad = ['pad', pin, process, padtype, at, size]

        if tag.has_attr('drill'):
            pad.append(['drill',tag['drill']])
            
        layers = ['layers'] + tag['layers'].split(',')
        pad.append(layers)
            
        if tag.has_attr('roundrect_rratio'):
            pad.append(['roundrect_rratio',tag['roundrect_rratio']])
            pad[3] = 'roundrect'

        if tag.has_attr('net'):
            pad.append(['net',tag['net'],tag['netname']])


        return pad



