
class Colour(object):

    def Assign(self, layername):
        if type(layername) == unicode:
            layername = str(layername)
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
            '*.Cu': '840000',
            'Default': 'FFFF00'
        }

        if layername in colours:
            return colours[layername]
        else:
            return colours['Default']
       

