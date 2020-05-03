import io

from parser_base import ParserBase
from sexpressions_parser import parse_sexpression

import json

class FlexParse(object):
    def __init__(self):
        self.filename_in = "example/simple.kicad_pcb"
        self.filename_json = "example/out.json"
        self.filename_svg = "example/out.svg"


    def Load(self):
        with io.open(self.filename_in, 'r', encoding='utf-8') as f:
            sexpression = parse_sexpression(f.read())
        return sexpression

    def Convert(self, obj):
        js = json.dumps(obj)
        return js

    def Print_Headings(self, dic):
        i = 0
        for item in dic:
            if type(item) is str:
                print(item)
            else:
                #print(item[0])
                if item[0] == 'segment':
                    self.Convert_Segment_To_SVG(item, i)
            i = i + 1

    def Save(self, xml):
        with open(self.filename_json, 'w') as f:
            f.write(xml)

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
        parameters += ';stroke:#000000'
        parameters += ';stroke-width:' + width
        parameters += '" '
        parameters += 'd="M ' + start[0] + ',' + start[1] + ' ' + end[0] + ',' + end[1] + '" '
        parameters += 'id="path' + str(id) + '" '
        parameters += 'layer="' + layer + '" '
        parameters += 'net="' + net + '" '
        parameters += '/>'

        print(parameters)


    def Run(self):
        dic = self.Load()
        self.Print_Headings(dic)
        js = self.Convert(dic)
        
        self.Save(js)


if __name__ == '__main__':
    e = FlexParse()
    e.Run()