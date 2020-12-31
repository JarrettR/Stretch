
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

        for item in input:
            if type(item) == str:
                #if item == 'gr_line' or item == 'fp_line':
                continue

            if item[0] == 'start':
                start.append(item[1])
                start.append(item[2])

            if item[0] == 'end':
                end.append(item[1])
                end.append(item[2])

            if item[0] == 'layer':
                layer = item[1]

            if item[0] == 'width':
                width = item[1]

            tstamp = ''
            if item[0] == 'tstamp':
                tstamp = 'tstamp="' + item[1] + '" '

        parameters = '<path style="fill:none;stroke-linecap:round;stroke-linejoin:miter;stroke-opacity:1'
        parameters += ';stroke:#' + self.Assign_Layer_Colour(layer)
        parameters += ';stroke-width:' + width + 'mm'
        parameters += '" '
        parameters += 'd="M ' + str(float(start[0]) * pxToMM) + ',' + str(float(start[1]) * pxToMM) + ' ' + str(float(end[0]) * pxToMM) + ',' + str(float(end[1]) * pxToMM) + '" '
        parameters += 'id="path' + str(id) + '" '
        parameters += 'layer="' + layer + '" '
        parameters += 'type="gr_line" '
        parameters += tstamp
        parameters += '/>'

        return parameters

