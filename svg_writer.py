import io
from bs4 import BeautifulSoup
import json

from parser_base import ParserBase
from sexpressions_parser import parse_sexpression
from sexpressions_writer import SexpressionWriter

pxToMM = 26.458


# kicad_pcb
# version
# host
# general
# page
# title_block
# layers
# setup
# net
# net_class
# module
# dimension
# gr_line
# gr_arc
# gr_text
# segment

class FlexParse(object):
    def __init__(self):
        self.filename_in = "example/simple.kicad_pcb"
        self.filename_json = "example/out.json"
        self.filename_svg = "example/out.svg"
        self.filename_base = "example/base.svg"


    def Load(self):
        with io.open(self.filename_in, 'r', encoding='utf-8') as f:
            sexpression = parse_sexpression(f.read())
        return sexpression

    def Convert(self, obj):
        js = json.dumps(obj)
        return js

    def Save(self, xml):
        with open(self.filename_json, 'w') as f:
            f.write(xml)

    def Print_Headings(self, dic):
        for item in dic:
            if type(item) is str:
                print(item)
            else:
                print(item[0])

    def Handle_Headings(self, items, base):
        # svg = ''
        dic = []
        segments = []
        if items[0] != 'kicad_pcb':
            assert "kicad_pcb: Not a kicad_pcb"

        base.svg.append(BeautifulSoup('<kicad />', 'html.parser'))
        
        i = 0
        for item in items:
            if type(item) is str:
                print(item)
            else:
                if item[0] == 'layers':
                    layers = self.Convert_Layers_To_SVG(item)
                   
                    for layer in layers:
                        tag = BeautifulSoup(layer, 'html.parser')
                        base.svg.append(tag)

                elif item[0] == 'segment':
                    tag = BeautifulSoup(self.Convert_Segment_To_SVG(item, i), 'html.parser')
                    layer = tag.path['layer']
                    base.svg.find('g', {'inkscape:label': layer}, recursive=False).append(tag)

                elif item[0] == 'gr_line':
                    tag = BeautifulSoup(self.Convert_Gr_Line_To_SVG(item, i), 'html.parser')
                    layer = tag.path['layer']
                    base.svg.find('g', {'inkscape:label': layer}, recursive=False).append(tag)
                else:
                    svg = self.Convert_Metadata_To_SVG(item)
                    base.svg.kicad.append(BeautifulSoup(svg, 'html.parser'))
            i = i + 1
        dic.append({'segment': segments})

        svg = base.prettify("utf-8")
        with open(self.filename_svg, "wb") as file:
            file.write(svg)

        return dic



    def Convert_Metadata_To_SVG(self, input):
        # This will just take whatever data and store it in an XML tag as JSON
        # Hacky, but we don't care about it other than to be able to load it back in later

       
        tag = input[0]
        input = input[1:]
        
        body = json.dumps(input)
        
        svg = '<' + tag + '>'
        svg += body
        svg += '</' + tag + '>'

        return svg


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
    
        if input[0] != 'layers':
            assert "Layers: Not a layer"
            return None

        for item in input:
            i = i + 1
            if i == 1:
                continue

            layerid = item[0]
            layername = item[1]

            user = ''
            hide = ''
            if 'user' in item:
                user = 'user="True" '
            if 'hide' in item:
                hide = 'hide="True" '


            parameters = '<g '
            parameters += 'inkscape:label="' + layername + '" '
            parameters += 'inkscape:groupmode="layer" '
            parameters += 'id="layer' + layerid + '"'
            parameters += user
            parameters += hide
            parameters += '/>'

            layers.append(parameters)
            i = i + 1
        
        # return {'layers': layers }
        return layers


    def Convert_Segment_To_SVG(self, input, id):
        # 0 segment
        # 1
        #   0 start
        #   1 66.66
        #   2 99.99
        # 2
        #   0 end
        #   1 66.66
        #   2 99.99
        # 3
        #   0 width
        #   1 0.25
        # 4
        #   0 layer
        #   1 B.Cu
        # 5
        #   0 net
        #   1 1

        start = []
        end = []

        if input[0] != 'segment':
            assert "Segment: Not a segment"
            return None

        if input[1][0] != 'start':
            assert "Segment: Start out of order"
            return None

        start.append(input[1][1])
        start.append(input[1][2])

        if input[2][0] != 'end':
            assert "Segment: End out of order"
            return None

        end.append(input[2][1])
        end.append(input[2][2])

        if input[3][0] != 'width':
            assert "Segment: Width out of order"
            return None

        width = input[3][1]

        if input[4][0] != 'layer':
            assert "Segment: Layer out of order"
            return None

        layer = input[4][1]

        if input[5][0] != 'net':
            assert "Segment: Net out of order"
            return None

        net = input[5][1]

        parameters = '<path style="fill:none;stroke-linecap:round;stroke-linejoin:miter;stroke-opacity:1'
        parameters += ';stroke:#' + self.Assign_Layer_Colour(layer)
        parameters += ';stroke-width:' + width + 'mm'
        parameters += '" '
        parameters += 'd="M ' + str(float(start[0]) * pxToMM) + ',' + str(float(start[1]) * pxToMM) + ' ' + str(float(end[0]) * pxToMM) + ',' + str(float(end[1]) * pxToMM) + '" '
        # parameters += 'd="M ' + start[0] + ',' + start[1] + ' ' + end[0] + ',' + end[1] + '" '
        parameters += 'id="path' + str(id) + '" '
        parameters += 'layer="' + layer + '" '
        parameters += 'net="' + net + '" '
        parameters += '/>'

        # print(parameters)
        return parameters

    def Convert_Gr_Line_To_SVG(self, input, id):
        # 0 gr_line
        # 1
        #   0 start
        #   1 66.66
        #   2 99.99
        # 2
        #   0 end
        #   1 66.66
        #   2 99.99
        # 3
        #   0 layer
        #   1 Edge.Cuts
        # 4
        #   0 width
        #   1 0.05
        # 5
        #   0 tstamp
        #   1 5E451B20

        start = []
        end = []

        if input[0] != 'gr_line':
            assert "Gr_line: Not a gr_line"
            return None

        if input[1][0] != 'start':
            assert "Gr_line: Start out of order"
            return None

        start.append(input[1][1])
        start.append(input[1][2])

        if input[2][0] != 'end':
            assert "Gr_line: End out of order"
            return None

        end.append(input[2][1])
        end.append(input[2][2])

        if input[3][0] != 'layer':
            assert "Gr_line: Layer out of order"
            return None

        layer = input[3][1]

        if input[4][0] != 'width':
            assert "Gr_line: Width out of order"
            return None

        width = input[4][1]


        if input[5][0] != 'tstamp':
            assert "Gr_line: tstamp out of order"
            return None

        tstamp = input[5][1]

        parameters = '<path style="fill:none;stroke-linecap:round;stroke-linejoin:miter;stroke-opacity:1'
        parameters += ';stroke:#' + self.Assign_Layer_Colour(layer)
        parameters += ';stroke-width:' + width + 'mm'
        parameters += '" '
        parameters += 'd="M ' + str(float(start[0]) * pxToMM) + ',' + str(float(start[1]) * pxToMM) + ' ' + str(float(end[0]) * pxToMM) + ',' + str(float(end[1]) * pxToMM) + '" '
        parameters += 'id="path' + str(id) + '" '
        parameters += 'layer="' + layer + '" '
        parameters += 'tstamp="' + tstamp + '" '
        parameters += '/>'

        return parameters

    def Assign_Layer_Colour(self, layername):
        colours = {
            'F.Cu': '840000',
            'In1.Cu': 'C2C200',
            'In2.Cu': 'C200C2',
            'B.Cu': '008400',
            'B.Adhes': 'FF',
            'F.Adhes': 'FF',
            'B.Paste': 'FF',
            'F.Paste': 'FF',
            'B.SilkS': 'FF',
            'F.SilkS': 'FF',
            'B.Mask': 'FF',
            'F.Mask': 'FF',
            'Dwgs.User': 'FF',
            'Cmts.User': 'FF',
            'Eco1.User': 'FF',
            'Eco2.User': 'FF',
            'Edge.Cuts': 'C2C200',
            'Margin': 'FF',
            'B.CrtYd': 'FF',
            'F.CrtYd': 'FF',
            'B.Fab': 'FF',
            'F.Fab': 'FF',
            'Default': 'FFFF00'
        }

        if layername in colours:
            return colours[layername]
        else:
            return colours['Default']
        
        


    def Run(self):
        dic = self.Load()
        # self.Print_Headings(dic)
        #js = self.Convert(dic)
        #self.Save(js)
        
        with open(self.filename_base, "r") as f:
    
            contents = f.read()
            base = BeautifulSoup(contents, 'html.parser')
        

        tags = self.Handle_Headings(dic, base)

        # writer = SvgWriter(tags)

        # writer.Display()


if __name__ == '__main__':
    e = FlexParse()
    e.Run()