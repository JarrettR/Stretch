    def Parse_Module(self, tag):
        # print(tag['id'])
        module = ['module', tag['name'], ['layer', tag['layer']]]
        segments = []
        gr_lines = []
        gr_arcs = []
        gr_curves = []
        gr_polys = []
        pads = []
        zones = []
        transform = tag['transform']
        
        translate = transform[transform.find('translate(') + 10:]
        translate = translate[0:translate.find(')')]
        x = translate[0:translate.find(',')]
        y = translate[len(x) + 1:]
        x = float(x) / pxToMM
        y = float(y) / pxToMM

        rotate = 0
        if 'rotate(' in transform:
            rotate = transform[transform.find('rotate(') + 7:]
            rotate = float(rotate[0:-1]) * -1

        
        if tag.has_attr('tedit'):
            module.append(['tedit', tag['tedit']])

        if tag.has_attr('tstamp'):
            module.append(['tstamp', tag['tstamp']])

        at = ['at', str(x), str(y), str(rotate)]
        module.append(at)
        
        if tag.has_attr('descr'):
            module.append(['descr', tag['descr']])

        if tag.has_attr('tags'):
            module.append(['tags', tag['tags']])

        if tag.has_attr('path'):
            module.append(['path', tag['path']])

        if tag.has_attr('attr'):
            module.append(['attr', tag['attr']])
            
        for text in tag.find_all('text'):
            module.append(self.Parse_Text(text))

        if tag.has_attr('model'):
            modeltag = tag['model']
            model = ['model']
            model.append(modeltag[0:modeltag.find(';')])
            modeltag = modeltag[modeltag.find(';') + 1:]
            offset = ['xyz'] + modeltag[0:modeltag.find(';')].split(',')
            modeltag = modeltag[modeltag.find(';') + 1:]
            scale = ['xyz'] + modeltag[0:modeltag.find(';')].split(',')
            modeltag = modeltag[modeltag.find(';') + 1:]
            rotate = ['xyz'] + modeltag[0:modeltag.find(';')].split(',')
            model.append(['offset', offset])
            model.append(['scale', scale])
            model.append(['rotate', rotate])
            
            module.append(model)

        for path in tag.find_all('path'):
            if path.has_attr('type') == True and path['type'] == 'zone':
                zones.append(self.Parse_Zone(path))
            else:
                segment, gr_line, gr_arc, gr_curve = self.Parse_Segment(path)
                segments = segments + segment
                gr_line[0][0] = 'fp_line'
                gr_lines += gr_line
                gr_arcs += gr_arc
                gr_curves += gr_curve

        for rect in tag.find_all('rect'):
            pad = self.Parse_Pad(rect, 'rect')
            if pad != None:
                pads.append(pad)
        for circle in tag.find_all('circle'):
            pad = self.Parse_Pad(circle, 'circle')
            if pad != None:
                pads.append(pad)

        if len(segments) > 0:
            module.append(segments)
        if len(pads) > 0:
            module = module + pads
            
        gr_lines.reverse()
        gr_arcs.reverse()
        gr_curves.reverse()
        gr_polys.reverse()
        zones.reverse()
            
        module = module + gr_lines + gr_arcs + gr_curves + gr_polys + zones
        return module


    def Convert_Module_To_SVG(self, input, id):
        # 0 module
        # 1 Diode_SMD:D_SMD_SOD123
        # 2
        #   0 layer
        #   1 B.Cu
        # 3
        #   0 tstamp
        #   1 0DF
        # 4
        #   0 at
        #   1 66.66
        #   2 99.99
        # 3
        #   0 descr
        #   1 0.25
        # 4
        #   0 tags
        #   1 B.Cu
        # 5
        #   0 path
        #   1 1
        # 5
        #   0 attr
        #   1 1
        # 5
        #   0 fp_text / fp_line / fp_text / pad
        #   1 1
        #....
        #....
        # 5
        #   0 model
        #   1 ${KISYS3DMOD}/Package_TO_SOT_SMD.3dshapes/SOT-23-6.wrl
        #   2 offset
        #     0 xyz
        #     1 0
        #     2 0
        #     3 0
        #   3 scale
        #     0 xyz
        #     1 1
        #     2 1
        #     3 1
        #   4 rotate
        #     0 xyz
        #     1 0
        #     2 0
        #     3 0

        at = []
        # svg = BeautifulSoup('<g inkscape:groupmode="layer" type="module" inkscape:label="module' + str(id) + '" id="module' + str(id) + '">', 'html.parser')
        svg = BeautifulSoup('<g type="module" inkscape:label="module' + str(id) + '" id="module' + str(id) + '" name="' + input[1] + '">', 'html.parser')
        
        if input[0] != 'module':
            assert False,"Module: Not a module"
            return None

        a = 0

        for item in input:


            if item[0] == 'at':
                x = float(item[1]) * pxToMM
                y = float(item[2]) * pxToMM
                rotate = 0

                at.append(item[1])
                at.append(item[2])
                transform = 'translate(' + str(x) + ',' + str(y) + ')'

                if len(item) > 3:
                    rotate = float(item[3])
                    transform += ' rotate(' + str(-1 * rotate) + ')'

                svg.g['transform'] = transform

            if item[0] == 'layer':
                svg.g['layer'] = item[1]

            if item[0] == 'tedit':
                svg.g['tedit'] = item[1]

            if item[0] == 'tstamp':
                svg.g['tstamp'] = item[1]

            if item[0] == 'descr':
                svg.g['descr'] = item[1]

            if item[0] == 'tags':
                svg.g['tags'] = item[1]

            if item[0] == 'path':
                svg.g['path'] = item[1]

            if item[0] == 'attr':
                svg.g['attr'] = item[1]

            if item[0] == 'model':
                svg.g['model'] = item[1] + ';'
                #offset
                svg.g['model'] += item[2][1][1] + ',' + item[2][1][2] + ',' + item[2][1][3] + ';'
                #scale
                svg.g['model'] += item[3][1][1] + ',' + item[3][1][2] + ',' + item[3][1][3] + ';'
                #rotate
                svg.g['model'] += item[4][1][1] + ',' + item[4][1][2] + ',' + item[4][1][3] + ';'

            if item[0] == 'fp_line':
                tag = BeautifulSoup(self.Convert_Gr_Line_To_SVG(item, str(id) + '-' + str(a)), 'html.parser')
                svg.g.append(tag)

            if item[0] == 'fp_curve':
                tag = BeautifulSoup(self.Convert_Gr_Curve_To_SVG(item, str(id) + '-' + str(a)), 'html.parser')
                svg.g.append(tag)

            if item[0] == 'fp_text':
                tag = BeautifulSoup(self.Convert_Gr_Text_To_SVG(item, str(id) + '-' + str(a), rotate), 'html.parser')
                svg.g.append(tag)

            elif item[0] == 'pad':
                tag = BeautifulSoup(self.Convert_Pad_To_SVG(item, str(id) + '-' + str(a), rotate), 'html.parser')
                svg.g.append(tag)

            a += 1

        return svg

