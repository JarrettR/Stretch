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




    def Convert_Pad_To_SVG(self, input, id, r_offset = 0):
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

        pin = input[1]

        process = input[2]

        for row in input:
            if len(row) > 1:
                if row[0] == 'at':
                    at.append(float(row[1]))
                    at.append(float(row[2]))

                    if len(row) > 3:
                        start = at[0] + at[1] * 1j
                        angle = math.radians(float(row[3]) - r_offset)
                        endangle = cmath.phase(start) - angle
                        end = cmath.rect(cmath.polar(start)[0], endangle)
                        
                        at[0] = end.real 
                        at[1] = end.imag
                        
                        rotate += 'transform=rotate(' + str(float(row[3]) - r_offset) + ') '
                        rotate += 'rotate = ' + str(float(row[3])) + ' '
                        

                if row[0] == 'size':
                    size.append(row[1])
                    size.append(row[2])

                if row[0] == 'roundrect_rratio':
                    ratio = row[1]
                    roundrect_rratio = 'roundrect_rratio="' + row[1] + '"'

                if row[0] == 'drill':
                    drill = 'drill="' + row[1] + '" '

                if row[0] == 'net':
                    net = 'net="' + row[1] + '" '
                    net += 'netname="' + row[2] + '"'

                if row[0] == 'layers':
                    row = row[1:]

                    for layer in row:
                        layers.append(layer)


        shape = input[3]

        svg = ''
        svgsize = ''
        roundcorners = ''
        first = True

        #Reverse list
        for layer in layers[::-1]:
            parameters = ''
            if shape == 'rect':

                # Corner coordinates to centre coordinate system
                x = at[0] - float(size[0]) / 2
                y = at[1] - float(size[1]) / 2

                parameters += '<rect style="stroke:none;stroke-linecap:round;stroke-linejoin:miter;fill-opacity:1'
                svgsize += 'x="' + str(x * pxToMM) + '" '
                svgsize += 'y="' + str(y * pxToMM) + '" '
                svgsize += 'width="' + str(float(size[0])  * pxToMM) + '" '
                svgsize += 'height="' + str(float(size[1])  * pxToMM) + '" '
            elif shape == 'roundrect':
                
                # Corner coordinates to centre coordinate system
                x = at[0] - float(size[0]) / 2
                y = at[1] - float(size[1]) / 2

                parameters += '<rect style="stroke:none;stroke-linecap:round;stroke-linejoin:miter;fill-opacity:1'
                roundcorners += 'rx="' + str(float(size[0]) * float(ratio)  * pxToMM) + '" '
                roundcorners += 'ry="' + str(float(size[1]) * float(ratio)  * pxToMM) + '" '
                svgsize += 'x="' + str(x * pxToMM) + '" '
                svgsize += 'y="' + str(y * pxToMM) + '" '
                svgsize += 'width="' + str(float(size[0])  * pxToMM) + '" '
                svgsize += 'height="' + str(float(size[1])  * pxToMM) + '" '
            elif shape == 'circle':
                parameters += '<circle style="stroke:none;stroke-linecap:round;stroke-linejoin:miter;fill-opacity:1'
                svgsize += 'cx="' + str(at[0] * pxToMM) + '" '
                svgsize += 'cy="' + str(at[1] * pxToMM) + '" '
                svgsize += 'r="' + str(float(size[0])  * (pxToMM / 2)) + '" '
                svgsize += 'height="' + str(float(size[1])  * pxToMM) + '" '
            elif shape == 'oval':
                parameters += '<circle style="stroke:none;stroke-linecap:round;stroke-linejoin:miter;fill-opacity:1'
                svgsize += 'cx="' + str(at[0] * pxToMM) + '" '
                svgsize += 'cy="' + str(at[1] * pxToMM) + '" '
                svgsize += 'r="' + str(float(size[0])  * (pxToMM / 2)) + '" '
                svgsize += 'height="' + str(float(size[1])  * pxToMM) + '" '
            elif shape == 'custom':
                # todo: Setting custom shape to rect for now
                x = at[0] - float(size[0]) / 2
                y = at[1] - float(size[1]) / 2

                parameters += '<rect style="stroke:none;stroke-linecap:round;stroke-linejoin:miter;fill-opacity:1'
                svgsize += 'x="' + str(x * pxToMM) + '" '
                svgsize += 'y="' + str(y * pxToMM) + '" '
                svgsize += 'width="' + str(float(size[0])  * pxToMM) + '" '
                svgsize += 'height="' + str(float(size[1])  * pxToMM) + '" '
            else:
                assert False,"Pad: Unfamiliar shape: " + shape
                return None

            parameters += ';fill:#' + self.Assign_Layer_Colour(layer)
            parameters += '" '
            parameters += 'id="path-' + str(id) + '-' + layer + '" '
            parameters += svgsize
            parameters += roundcorners
            parameters += roundrect_rratio
            parameters += net
            parameters += rotate
            parameters += drill
            parameters += 'process="' + process + '"'
            parameters += 'pin="' + pin + '"'
            if first == True:
                parameters += 'first="True"'
                parameters += 'layers="' + ','.join(layers) + '"'
            parameters += '/>'

            svg += parameters
            first = False

        #print(parameters)
        return svg
