
class Curve(object):

    def __init__(self):
        self.tstamp = ''
        
        
    def Parse_Curves(self, tag, segments):
        # 0 gr_curve
        # 1
        #   0 pts
        #   1
        #       0 xy
        #       1 99.99
        #       2 99.99
        #   2
        #       0 xy
        #       1 99.99
        #       2 99.99
        #   3
        #       0 xy
        #       1 99.99
        #       2 99.99
        #   4
        #       0 xy
        #       1 99.99
        #       2 99.99
        # 2
        #   0 layer
        #   1 Edge.Cuts
        # 3
        #   0 width
        #   1 0.05
        # 4
        #   0 tstamp
        #   1 5E451B20
        
        xy_float = 4 * [0.0]

        unparsed_path = tag['d'].split(' ')
        # print(tag)
        # print(tag['d'])
        # print(unparsed_path)
        # print(segments)
        
        #['M', '61.632,52.32', 'C', '66.48,54.91', '59.52,63.45', '56.42,57.52']
        
        xy_str = unparsed_path[1].split(',')
        xy_float[0] = [float(xy_str[0]), float(xy_str[1])]
        xy_str = unparsed_path[3].split(',')
        xy_float[1] = [float(xy_str[0]), float(xy_str[1])]
        xy_str = unparsed_path[4].split(',')
        xy_float[2] = [float(xy_str[0]), float(xy_str[1])]
        xy_str = unparsed_path[5].split(',')
        xy_float[3] = [float(xy_str[0]), float(xy_str[1])]
        
        
        #relative / absolute compensation
        if unparsed_path[2] == 'c':
            xy_float[1][0] = xy_float[0][0] - xy_float[1][0] * -1
            xy_float[1][1] = xy_float[0][1] - xy_float[1][1] * -1
            xy_float[2][0] = xy_float[0][0] - xy_float[2][0] * -1
            xy_float[2][1] = xy_float[0][1] - xy_float[2][1] * -1
            xy_float[3][0] = xy_float[0][0] - xy_float[3][0] * -1
            xy_float[3][1] = xy_float[0][1] - xy_float[3][1] * -1
        
        
        xy = ['xy', str(xy_float[0][0] / pxToMM), str(xy_float[0][1] / pxToMM)]
        
        pts = ['pts', xy]
        
        xy = ['xy', str(xy_float[1][0] / pxToMM), str(xy_float[1][1] / pxToMM)]
        pts.append(xy)

        xy = ['xy', str(xy_float[2][0] / pxToMM), str(xy_float[2][1] / pxToMM)]
        pts.append(xy)

        xy = ['xy', str(xy_float[3][0] / pxToMM), str(xy_float[3][1] / pxToMM)]
        pts.append(xy)

        data = ['gr_curve']
        data.append(pts)
        data.append(segments[3])
        data.append(segments[2])
        
        if tag.has_attr('tstamp') == True:
            data.append(['tstamp', tag['tstamp']])
        
        return data


    def Convert_Gr_Curve_To_SVG(self, input, id):
        # 0 gr_curve
        # 1
        #   0 pts
        #   1
        #       0 xy
        #       1 99.99
        #       2 99.99
        #   2
        #       0 xy
        #       1 99.99
        #       2 99.99
        #   3
        #       0 xy
        #       1 99.99
        #       2 99.99
        #   4
        #       0 xy
        #       1 99.99
        #       2 99.99
        # 2
        #   0 layer
        #   1 Edge.Cuts
        # 3
        #   0 width
        #   1 0.05
        # 4
        #   0 tstamp
        #   1 5E451B20

        points = []
        
        for item in input:
            if type(item) == str:
                #if item == 'gr_curve' or item == 'fp_curve':
                continue

            #This might have a problem with random list ordering in certain versions of Python
            if item[0] == 'pts':
                for xy in item:
                    if xy[0] == 'xy':
                        points.append(float(xy[1]))
                        points.append(float(xy[2]))

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
        parameters += 'd="M ' + str(points[0] * pxToMM) + ',' + str(points[1] * pxToMM) + ' C '
        parameters += str(points[2] * pxToMM) + ',' + str(points[3] * pxToMM) + ' '
        parameters += str(points[4] * pxToMM) + ',' + str(points[5] * pxToMM) + ' '
        parameters += str(points[6] * pxToMM) + ',' + str(points[7] * pxToMM) + '" '
        parameters += 'id="path' + str(id) + '" '
        parameters += 'layer="' + layer + '" '
        parameters += 'type="gr_curve" '
        parameters += tstamp
        parameters += '/>'

        return parameters

