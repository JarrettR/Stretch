
from .colour import Colour

#https://github.com/KiCad/kicad-source-mirror/blob/93466fa1653191104c5e13231dfdc1640b272777/pcbnew/plugins/kicad/pcb_parser.cpp#L4275

# 0 via
# 1
#   0 at
#   1 66.66
#   2 99.99
# 2
#   0 size
#   1 0.6
# 3
#   0 drill
#   1 0.3
# 4
#   0 layers
#   1 F.Cu
#   2 B.Cu
# 5
#   0 net
#   1 16


pxToMM = 96 / 25.4

class Via(object):

    def __init__(self):
        self.blind = False
        self.micro = False
        self.at = []
        self.size = 0
        self.drill = 0
        self.layers = []
        self.net = 0
        self.remove_unused_layers = False
        self.keep_end_layers = False
        self.tstamp = ''
        self.status = ''
        self.locked = False
        self.free = False


    def From_SVG(self, tag):
        if not tag.has_attr('type'):
            return
        if not tag['type'] == "via":
            return
            
        x = tag['x']
        y = tag['y']
        self.at = [(float(x) / pxToMM), (float(y) / pxToMM)]

        self.size = float(tag['size']) / pxToMM
        self.drill = float(tag['drill']) / pxToMM

        self.layers = tag['layers'].split(',')

        self.net = tag['net']

        if tag.has_attr('tstamp'):
            self.tstamp = tag['tstamp']
        if tag.has_attr('status'):
            self.status = tag['status']
        if tag.has_attr('blind'):
            self.blind = True
        if tag.has_attr('micro'):
            self.micro = True
        if tag.has_attr('remove_unused_layers'):
            self.remove_unused_layers = True
        if tag.has_attr('keep_end_layers'):
            self.keep_end_layers = True
        if tag.has_attr('locked'):
            self.locked = True
        if tag.has_attr('free'):
            self.free = True

    def To_PCB(self):
        at = ['at'] + self.at

        via = [ 'via', at, ['size', self.size], ['drill', self.drill]]

        via.append(['layers'] + self.layers)

        via.append(['net', self.net])

        if self.tstamp != '':
            via.append(['tstamp', self.tstamp])
        if self.status != '':
            via.append(['status', self.status])
        if self.blind != False:
            via.append(['blind'])
        if self.micro != False:
            via.append(['micro'])
        if self.remove_unused_layers != False:
            via.append(['remove_unused_layers'])
        if self.keep_end_layers != False:
            via.append(['keep_end_layers'])
        if self.locked != False:
            via.append(['locked'])
        if self.free != False:
            via.append(['free'])

        return via
       

    def From_PCB(self, pcblist):
        at = []
        layers = []
        blind = ''
        status = ''
        tstamp = ''

        if pcblist[0] != 'via':
            assert False,"Via: Not a via"
            return None

        for item in pcblist:
            if item[0] == 'at':
                self.at = [item[1], item[2]]

            if item[0] == 'size':
                self.size = item[1]

            if item[0] == 'drill':
                self.drill = item[1]

            if item[0] == 'layers':
                self.layers = [item[1], item[2]]

            if item[0] == 'net':
                self.net = item[1]

            if item == 'blind':
                self.blind = True

            if item[0] == 'tstamp':
                self.tstamp = item[1] 
            
            if item[0] == 'status':
                self.status = item[1]
                
                
    def To_SVG(self):
        tstamp = ''
        status = ''
        blind = ''
        micro = ''
        remove_unused_layers = ''
        keep_end_layers = ''
        locked = ''
        free = ''
        
        if self.tstamp != '':
            tstamp = 'tstamp="' + self.tstamp + '" '
        if self.status != '':
            status = 'status="' + self.status + '" '
        if self.blind != False:
            blind = 'blind="true" '
        if self.micro != False:
            micro = 'micro="true" '
        if self.remove_unused_layers != False:
            remove_unused_layers = 'remove_unused_layers="true" '
        if self.keep_end_layers != False:
            keep_end_layers = 'keep_end_layers="true" '
        if self.locked != False:
            locked = 'locked="true" '
        if self.free != False:
            free = 'free="true" '

        parameters = '<g '
        parameters += 'x="' + str(float(self.at[0]) * pxToMM) + '" '
        parameters += 'y="' + str(float(self.at[1]) * pxToMM) + '" '
        #parameters += 'id="via' + str(id) + '" '
        parameters += 'type="via" '
        parameters += 'layers="' + self.layers[0] + ',' + self.layers[1] + '" '
        parameters += 'size="' + self.size + '" '
        parameters += 'drill="' + self.drill + '" '
        parameters += 'net="' + self.net + '" '
        parameters += blind
        parameters += tstamp
        parameters += status
        parameters += micro
        parameters += remove_unused_layers
        parameters += keep_end_layers
        parameters += locked
        parameters += free
        parameters += '>'

        hole = '<circle style="stroke:none;stroke-linecap:round;stroke-linejoin:miter;fill-opacity:1'
        hole += ';fill:#' + Colour.Assign('Via.Inner')
        hole += '" '
        hole += 'cx="' + str(float(self.at[0]) * pxToMM) + '" '
        hole += 'cy="' + str(float(self.at[1]) * pxToMM) + '" '
        #hole += 'id="viai' + str(id) + '" '
        #hole += 'drill="true" '
        hole += 'r="' + str(float(self.drill)  * (pxToMM / 2)) + '" '
        hole += '/>'

        parameters += '<circle style="stroke:none;stroke-linecap:round;stroke-linejoin:miter;fill-opacity:1'
        parameters += ';fill:#' + Colour.Assign('Via.Outer')
        parameters += '" '
        parameters += 'cx="' + str(float(self.at[0]) * pxToMM) + '" '
        parameters += 'cy="' + str(float(self.at[1]) * pxToMM) + '" '
        #parameters += 'id="viao' + str(id) + '" '
        parameters += 'r="' + str(float(self.size)  * (pxToMM / 2)) + '" '
        parameters += 'layers="' + self.layers[0] + ',' + self.layers[1] + '" '
        parameters += 'size="' + self.size + '" '
        parameters += 'drill="' + self.drill + '" '
        parameters += 'net="' + self.net + '" '
        parameters += blind
        parameters += tstamp
        parameters += status
        parameters += micro
        parameters += remove_unused_layers
        parameters += keep_end_layers
        parameters += locked
        parameters += free
        parameters += '/>' + hole 

        parameters += '</g>'

        #print(parameters)
        return parameters
        