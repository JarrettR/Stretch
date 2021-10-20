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
        #thru_hole, smd, connect, or np_thru_hole
        self.attribute = ''
        self.shape = ''
        self.size = []
        self.at = []
        self.rect_delta = []
        self.drill = []
        self.layers = []
        self.net = []
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
                self.net = item[1:] 
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

    def To_PCB(self):
        pcb = ['pad']

        pcb.append(self.name)
        pcb.append(self.attribute)
        pcb.append(self.shape)

        pcb.append(['at'] + self.at)
        pcb.append(['size'] + self.size)
        pcb.append(['layers'] + self.layers)
        pcb.append(['net'] + self.net)

        if self.tstamp:
            pcb.append(['tstamp', self.tstamp])
            
        return pcb
        


    def To_SVG(self):

        layers = []
        roundrect_rratio = ''
        net = ''
        drill = ''
        rotate = ''
        parameters = ''
        
        # Corner coordinates to centre coordinate system
        x = self.at[0] - float(self.size[0]) / 2
        y = self.at[1] - float(self.size[1]) / 2

        if len(self.at) > 2:
            rotate += 'transform="rotate(' + str(self.at[2]) + ', ' + str(self.at[0] * pxToMM) + ', ' + str(self.at[1] * pxToMM) + ')" '
                        
        if self.roundrect_rratio != '':
            roundrect_rratio = 'roundrect_rratio="' + self.roundrect_rratio + '" '

        if self.drill:
            drill = 'drill="' + self.drill + '" '

        svg = ''
        svgsize = ''
        roundcorners = ''
        
        if self.shape == 'rect':
            parameters += '<rect style="stroke:none;stroke-linecap:round;stroke-linejoin:miter;fill-opacity:1'
            svgsize += 'x="' + str(x * pxToMM) + '" '
            svgsize += 'y="' + str(y * pxToMM) + '" '
            svgsize += 'width="' + str(float(self.size[0])  * pxToMM) + '" '
            svgsize += 'height="' + str(float(self.size[1])  * pxToMM) + '" '
            
        elif self.shape == 'roundrect':

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
        parameters += 'type="pad" '
        parameters += 'name="' + self.name + '" '
        parameters += 'attribute="' + self.attribute + '" '
        parameters += 'netid="' + self.net[0] + '" '
        parameters += 'netname="' + self.net[1] + '" '
        parameters += 'shape="' + self.shape + '" '
        parameters += rotate
        parameters += drill
        parameters += 'layers="' + ','.join(self.layers) + '" '
        parameters += '/>'

        svg += parameters
        # print(parameters)
        return svg


    def From_SVG(self, tag):

        self.name = tag['name']
        self.attribute = tag['attribute']

        if tag.has_attr('shape'):
            self.shape = tag['shape']

        if self.shape == 'rect':

            width = float(tag['width']) / pxToMM
            height = float(tag['height']) / pxToMM
            x = str((float(tag['x']) / pxToMM) + (width / 2))
            y = str((float(tag['y']) / pxToMM) + (height / 2))
            width = str(width)
            height = str(height)

            self.size = [width, height]

        elif self.shape == 'circle' or self.shape == 'oval':
            r = str((float(tag['r']) * 2) / pxToMM)
            self.size = [r, r]
            x = str(float(tag['cx']) / pxToMM)
            y = str(float(tag['cy']) / pxToMM)


        self.at = [x, y]
        if tag.has_attr('rotate'):
            at.append(tag['rotate'])


        if tag.has_attr('drill'):
            self.drill = tag['drill']
            
        self.layers = tag['layers'].split(',')
            
        if tag.has_attr('roundrect_rratio'):
            self.roundrect_rratio = tag['roundrect_rratio']
            self.shape = 'roundrect'

        if tag.has_attr('netid'):
            self.net = [tag['netid'], tag['netname']]





