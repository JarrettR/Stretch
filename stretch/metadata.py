    def Handle_Headings(self, items, base):
        # svg = ''
        dic = []
        segments = []
        #if items[0] != 'kicad_pcb':
        #    assert False,"kicad_pcb: Not a kicad_pcb"

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
            i = i + 1
                             
        for item in items:
            if type(item) is str:
                print(item)
            else:
                if item[0] == 'module':
                    base.svg.append(self.Convert_Module_To_SVG(item, i))
            i = i + 1
            
        base.svg.append(BeautifulSoup('<g inkscape:label="Vias" inkscape:groupmode="layer" id="layervia" user="True" />', 'html.parser'))


        for item in items:
            if type(item) is str:
                print(item)
            else:
                # print(item[0])
                if item[0] == 'segment':
                    tag = BeautifulSoup(self.Convert_Segment_To_SVG(item, i), 'html.parser')
                    layer = tag.path['layer']
                    base.svg.find('g', {'inkscape:label': layer}, recursive=False).append(tag)

                elif item[0] == 'gr_line':
                    tag = BeautifulSoup(self.Convert_Gr_Line_To_SVG(item, i), 'html.parser')
                    layer = tag.path['layer']
                    base.svg.find('g', {'inkscape:label': layer}, recursive=False).append(tag)
                    
                elif item[0] == 'gr_poly':
                    tag = BeautifulSoup(self.Convert_Gr_Poly_To_SVG(item, i), 'html.parser')
                    layer = tag.path['layer']
                    base.svg.find('g', {'inkscape:label': layer}, recursive=False).append(tag)

                elif item[0] == 'gr_arc':
                    tag = BeautifulSoup(self.Convert_Gr_Arc_To_SVG(item, i), 'html.parser')
                    layer = tag.path['layer']
                    base.svg.find('g', {'inkscape:label': layer}, recursive=False).append(tag)

                elif item[0] == 'gr_curve':
                    tag = BeautifulSoup(self.Convert_Gr_Curve_To_SVG(item, i), 'html.parser')
                    layer = tag.path['layer']
                    base.svg.find('g', {'inkscape:label': layer}, recursive=False).append(tag)

                elif item[0] == 'gr_text':
                    tag = BeautifulSoup(self.Convert_Gr_Text_To_SVG(item, i), 'html.parser')
                    layer = tag.find('text')['layer']
                    base.svg.find('g', {'inkscape:label': layer}, recursive=False).append(tag)

                elif item[0] == 'zone':
                    tag = BeautifulSoup(self.Convert_Zone_To_SVG(item, i), 'html.parser')
                    layer = tag.path['layer']
                    if layer:
                        base.svg.find('g', {'inkscape:label': layer}, recursive=False).append(tag)

                elif item[0] == 'via':
                    tag = BeautifulSoup(self.Convert_Via_To_SVG(item, i), 'html.parser')
                    base.svg.find('g', {'inkscape:label': 'Vias'}, recursive=False).append(tag)
                    
                elif item[0] != 'layers' and item[0] != 'module':
                    # Already handled above
                    svg = self.Convert_Metadata_To_SVG(item)
                    base.svg.kicad.append(BeautifulSoup(svg, 'html.parser'))
                    
            i = i + 1
        dic.append({'segment': segments})

        if debug == True:
            svg = base.prettify("utf-8")
        else:
            svg = base.encode()
        
        return svg


    def Convert_Metadata_To_SVG(self, input):
        # This will just take whatever data and store it in an XML tag as JSON
        # Hacky, but we don't care about it other than to be able to load it back in later

       
        tag = input[0]
        #input = input[1:]
        
        body = json.dumps(input)
        
        svg = '<' + tag + '>'
        svg += body
        svg += '</' + tag + '>'

        return body + ','


