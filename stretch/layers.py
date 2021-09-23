#https://github.com/KiCad/kicad-source-mirror/blob/93466fa1653191104c5e13231dfdc1640b272777/pcbnew/plugins/kicad/pcb_parser.cpp#L1360

# 0 layers
# 1
#   0 1-whatever layerid
#   1 F.Cu
#   2/3 user/hide(optional)
# 2 ...
# 3 ...

class Layers(object):

    def __init__(self):
        self.names = {}
        self.attribs = {}
        
        
    def From_PCB(self, pcblist):
    
        if pcblist[0] != 'layers':
            assert False,"Layers: Not a layer"
            return None

        for item in pcblist:
        
            if item == 'layers':
                continue
                
            self.names[item[0]] = item[1]

            attribs = []
            if 'user' in item:
                attribs.append('user')
            if 'hide' in item:
                attribs.append('hide')
            if 'signal' in item:
                attribs.append('signal')
            if 'power' in item:
                attribs.append('power')
                
            self.attribs[item[0]] = attribs
     
    def To_PCB(self):

        layers = []

        for number in self.names:
            layer = [str(number), self.names[number]]
            layer += self.attribs[number]
            layers.append(layer)

        layers.append('layers')
        layers.reverse()

        return layers

    def From_SVG(self, svg):

        for tag in svg.svg.find_all('g'):
            if tag.has_attr('id') == True:
                if tag['id'].startswith('layer'):
                    if tag.has_attr('number') == True:
                        self.names[tag['number']] = tag['inkscape:label']

                        if tag.has_attr('attribs'):
                            self.attribs[tag['number']] = tag['attribs'].split(',')
                        # if tag.has_attr('signal'):
                        #     attribs.append('signal')
                        # if tag.has_attr('power'):
                        #     attribs.append('power')
                        # if tag.has_attr('hide'):
                        #     attribs.append('hide')

                        # print('-')
                        # print(tag)

                        # self.attribs[tag['number']] = attribs

     
    def To_SVG(self):
        layers = []
        
        for item in self.names:

            parameters = '<g '
            parameters += 'inkscape:label="' + self.names[item] + '" '
            parameters += 'inkscape:groupmode="layer" '
            parameters += 'id="layer' + item + '"'
            parameters += 'number="' + item + '"'
            parameters += 'attribs="' + ','.join(self.attribs[item]) + '"'
            parameters += '/>'

            layers.insert(0, parameters)
        
        return layers
