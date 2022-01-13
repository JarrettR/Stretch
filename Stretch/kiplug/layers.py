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
        self.layer = []
        
        
    def From_PCB(self, pcblist):
    
        if pcblist[0] != 'layers':
            assert False,"Layers: Not a layer"
            return None

        for item in pcblist:
        
            if item == 'layers':
                continue
                
            layer = [str(item[0]), item[1]]

            if 'user' in item:
                layer.append('user')
            if 'signal' in item:
                layer.append('signal')
            if 'power' in item:
                layer.append('power')
            if 'mixed' in item:
                layer.append('mixed')
            if 'hide' in item:
                layer.append('hide')
                
            self.layer.append(layer)
     
    def To_PCB(self):

        layers = []

        for layer in self.layer:
            # layer = layername
            # layer += self.attribs[layernum]
            layers.append(layer)

        layers.append('layers')
        layers.reverse()

        return layers

    def From_SVG(self, svg):

        for tag in svg.svg.find_all('g'):
            if tag.has_attr('id') == True:
                if tag['id'].startswith('layer'):
                    if tag.has_attr('number') == True:
                        layer = [tag['number'], tag['inkscape:label']]

                        if tag.has_attr('attribs'):
                            attribs = tag['attribs'].split(',')
                            layer += attribs
                            
                        self.layer.append(layer)

     
    def To_SVG(self):
        layers = []
        
        for item in self.layer:
        
            hiddenlayer = ''
            if 'hide' in item[2:]:
                hiddenlayer = "style=display:none "

            parameters = '<g '
            parameters += 'inkscape:label="' + item[1] + '" '
            parameters += 'inkscape:groupmode="layer" '
            parameters += hiddenlayer
            parameters += 'id="layer' + item[0] + '"'
            parameters += 'number="' + item[0] + '"'
            parameters += 'attribs="' + ','.join(item[2:]) + '"'
            parameters += '/>'

            layers.insert(0, parameters)
        
        return layers
