    def Parse_Vias(self, tag):
        # (via (at 205.486 133.731) (size 0.6) (drill 0.3) (layers F.Cu B.Cu) (net 0) (tstamp 5EA04144) (status 30))
        vias = []
        for via_in in tag.find_all('g'):
            if not via_in.has_attr('type'):
                continue
            if not via_in['type'] == "via":
                continue
            x = via_in['x']
            y = via_in['y']
            at = ['at', str(float(x) / pxToMM), str(float(y) / pxToMM)]

            via = [ 'via', at, ['size', via_in['size']], ['drill', via_in['drill']]]

            layers = via_in['layers'].split(',')
            layers = ['layers'] + layers

            via.append(layers)

            via.append(['net', via_in['net']])

            if via_in.has_attr('tstamp'):
                via.append(['tstamp', via_in['tstamp']])
            if via_in.has_attr('status'):
                via.append(['status', via_in['status']])

            vias.append(via)
        return vias
       

       def Convert_Via_To_SVG(self, input, id):
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

        at = []
        layers = []
        blind = ''
        status = ''
        tstamp = ''

        if input[0] != 'via':
            assert False,"Via: Not a via"
            return None


        for item in input:
            if item[0] == 'at':
                at.append(item[1])
                at.append(item[2])

            if item[0] == 'size':
                size = item[1]

            if item[0] == 'drill':
                drill = item[1]

            if item[0] == 'layers':
                layers.append(item[1])
                layers.append(item[2])

            if item[0] == 'net':
                net = item[1]

            if item == 'blind':
                blind = 'blind=true '

            if item[0] == 'tstamp':
                tstamp = 'tstamp="' + item[1] + '" '
            
            if item[0] == 'status':
                status = 'status="' + item[1] + '" '
         
        parameters = '<g '
        parameters += 'x="' + str(float(at[0]) * pxToMM) + '" '
        parameters += 'y="' + str(float(at[1]) * pxToMM) + '" '
        parameters += 'id="via' + str(id) + '" '
        parameters += 'type="via" '
        parameters += 'layers="' + layers[0] + ',' + layers[1] + '" '
        parameters += 'size="' + size + '" '
        parameters += 'drill="' + drill + '" '
        parameters += 'net="' + net + '" '
        parameters += blind
        parameters += tstamp
        parameters += status
        parameters += '>'

        hole = '<circle style="stroke:none;stroke-linecap:round;stroke-linejoin:miter;fill-opacity:1'
        hole += ';fill:#' + self.Assign_Layer_Colour('Via.Inner')
        hole += '" '
        hole += 'cx="' + str(float(at[0]) * pxToMM) + '" '
        hole += 'cy="' + str(float(at[1]) * pxToMM) + '" '
        hole += 'id="viai' + str(id) + '" '
        #hole += 'drill="true" '
        hole += 'r="' + str(float(drill)  * (pxToMM / 2)) + '" '
        hole += '/>'

        parameters += '<circle style="stroke:none;stroke-linecap:round;stroke-linejoin:miter;fill-opacity:1'
        parameters += ';fill:#' + self.Assign_Layer_Colour('Via.Outer')
        parameters += '" '
        parameters += 'cx="' + str(float(at[0]) * pxToMM) + '" '
        parameters += 'cy="' + str(float(at[1]) * pxToMM) + '" '
        parameters += 'id="viao' + str(id) + '" '
        parameters += 'r="' + str(float(size)  * (pxToMM / 2)) + '" '
        parameters += 'layers="' + layers[0] + ',' + layers[1] + '" '
        parameters += 'size="' + size + '" '
        parameters += 'drill="' + drill + '" '
        parameters += 'net="' + net + '" '
        parameters += blind
        parameters += tstamp
        parameters += status
        parameters += '/>' + hole 

        parameters += '</g>'

        #print(parameters)
        return parameters
 
        
