
class Layer(object):

    def __init__(self):
        self.tstamp = ''
        
        
    def Convert_Layers_To_SVG(self, input):
        # 0 layers
        # 1
        #   0 1-whatever layerid
        #   1 F.Cu
        #   2/3 user/hide(optional)
        # 2 ...
        # 3 ...

        i = 0
        layers = []
        #print(input)
    
        # if input[0] != 'layers':
        #     assert False,"Layers: Not a layer"
        #     return None

        for item in input:
            i = i + 1
            if i == 1:
                continue

            layerid = item[0]
            layername = item[1]

            user = ''
            hide = ''
            signal = ''
            power = ''
            if 'user' in item:
                user = 'user="True" '
            if 'hide' in item:
                hide = 'hide="True" '
                self.hiddenLayers.append(layername)
            if 'signal' in item:
                signal = 'signal="True" '
            if 'power' in item:
                power = 'power="True" '


            parameters = '<g '
            parameters += 'inkscape:label="' + layername + '" '
            parameters += 'inkscape:groupmode="layer" '
            parameters += 'id="layer' + layerid + '"'
            parameters += 'number="' + layerid + '"'
            parameters += user
            parameters += hide
            parameters += signal
            parameters += power
            parameters += '/>'

            layers.insert(0, parameters)
            i = i + 1
        
        # return {'layers': layers }
        return layers


    def Assign_Layer_Colour(self, layername):
        colours = {
            'F.Cu': '840000',
            'In1.Cu': 'C2C200',
            'In2.Cu': 'C200C2',
            'B.Cu': '008400',
            'B.Adhes': '840084',
            'F.Adhes': '000084',
            'B.Paste': '000084',
            'F.Paste': '840000',
            'B.SilkS': '840084',
            'F.SilkS': '008484',
            'B.Mask': '848400',
            'F.Mask': '840084',
            'Dwgs.User': 'c2c2c2',
            'Cmts.User': '000084',
            'Eco1.User': '008400',
            'Eco2.User': 'c2c200',
            'Edge.Cuts': 'C2C200',
            'Margin': 'c200c2',
            'B.CrtYd': '848484',
            'F.CrtYd': 'c2c2c2',
            'B.Fab': '000084',
            'F.Fab': '848484',
            'Via.Outer': 'c2c2c2',
            'Via.Inner': '8c7827',
            'Default': 'FFFF00'
        }

        if layername in colours:
            return colours[layername]
        else:
            return colours['Default']
       