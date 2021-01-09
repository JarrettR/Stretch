
class Text(object):

    def __init__(self):
        self.tstamp = ''


    def Parse_Text(self, tag):
        # 0 gr_text
        # 1 text
        # 2
        #   0 at
        #   1 66.66
        #   2 99.99
        # 3
        #   0 layer
        #   1 F.SilkS
        # 4
        #   0 tstamp
        #   1 F.SilkS
        # 5
        #   0 effects
        #   1 
        #       0 font
        #           1
        #               0 size
        #               1 1.5
        #               2 1.5
        #           2
        #               0 thickness
        #               1 0.3
        #   2
        #       0 justify
        #       1 mirror
        
        text = []
        
        if tag['type'] == 'gr_text':
            text.append('gr_text')
        else:
            text.append('fp_text')
            text.append(tag['type'])
            
        text.append(tag.contents[0])
        x = str(float(tag['x']) / pxToMM)
        y = str(float(tag['y']) / pxToMM)
        
        attribs  = ['justify']
        
        if tag.has_attr('mirrored'):
            if tag['mirrored'] == 'true':
                attribs.append('mirror')
                x = str(float(x) * -1.0)
            
            
        text.append(['at', x, y])
        
        if tag.has_attr('layer'):
            layer = ['layer', tag['layer']]
        elif tag.parent.has_attr('inkscape:label'):
            #XML metadata trashed, try to recover from parent tag
            layer = ['layer', tag.parent['inkscape:label']]
        else:
            assert False, "Text not in layer"
            
        text.append(layer)
        
        if tag.has_attr('hide'):
            if tag['hide'] == 'True':
                text.append('hide')
        
        if tag.has_attr('tstamp'):
            text.append(['tstamp', tag['tstamp']])
        
        style = tag['style']

        styletag = style[style.find('font-size:') + 10:]
        
        size = styletag[0:styletag.find('px')]
        size = str(float(size) / pxToMM)
        
        font = ['font', ['size', size, size], ['thickness', tag['thickness']]]
        
        effects = ['effects', font, attribs]
        
        text.append(effects)
        
        return text



    def Convert_Gr_Text_To_SVG(self, input, id, r_offset = 0):
    
    
        # 0 gr_text
        # 1 text
        # 2
        #   0 at
        #   1 66.66
        #   2 99.99
        # 3
        #   0 layer
        #   1 F.SilkS
        # 4
        #   0 hide
        # 5
        #   0 tstamp
        #   1 F.SilkS
        # 6
        #   0 effects
        #   1 
        #       0 font
        #           1
        #               0 size
        #               1 1.5
        #               2 1.5
        #           2
        #               0 thickness
        #               1 0.3
        #   2
        #       0 justify
        #       1 mirror
        #
        # ---
        # 0 fp_text
        # 1 reference / value / user
        # 2 text
        # 3
        #   0 at
        at = []

        #gr_text is user-created label, fp_text is module ref/value
        if input[0] == 'gr_text':
            type_text = 'gr_text'
            text = input[1]

        if input[0] == 'fp_text':
            type_text = input[1]
            text = input[2]

        effect_text = ''
        transform = ''
        hide = ''
        hidelayer = ''
        tstamp = ''
        mirror_text = ''
        mirror = 1

        for item in input:
            if type(item) == str:
                if item == 'hide':
                    hide = 'hide="True" '

            if item[0] == 'at':
                at.append(item[1])
                at.append(item[2])
                if len(item) > 3:
                    transform += 'rotate(' + str(float(item[3]) + r_offset)+ ')'

            if item[0] == 'layer':
                layer = item[1]
                
            if item[0] == 'tstamp':
                tstamp = 'tstamp="' + item[1] + '" '

            if item[0] == 'effects':
                for effect in item[1:]:
                    if effect[0] == 'font':
                        for param in effect[1:]:
                            if param[0] == 'size':
                                size = [param[1], param[2]]
                            if param[0] == 'thickness':
                                thickness = param[1]
                    elif effect[0] == 'justify':
                        if len(effect) > 1:
                            if effect[1] == 'mirror':
                                transform += ' scale(-1,1)'
                                mirror = -1
                                mirror_text = 'mirrored="true" '
                        
                    else:
                        effect_text = 'effects="' + ';'.join(effect) + '" '
                            


        if len(transform) > 0:
            transform = 'transform="' + transform + '" '
            
        if layer in self.hiddenLayers:
            hidelayer = ';display:none'
            
        parameters = '<text '
        parameters += 'xml:space="preserve" '
        parameters += 'style="font-style:normal;font-weight:normal;font-family:sans-serif'
        parameters += ';fill-opacity:1;stroke:none'
        parameters += hidelayer
        parameters += ';font-size:' + str(float(size[0]) * pxToMM) + 'px'
        parameters += ';fill:#' + self.Assign_Layer_Colour(layer)
        parameters += '" '
        parameters += 'x="' + str(float(at[0]) * pxToMM * mirror) + '" '
        parameters += 'y="' + str(float(at[1]) * pxToMM) + '" '
        parameters += 'id="text' + str(id) + '" '
        parameters += effect_text
        parameters += mirror_text
        parameters += 'layer="' + layer + '" '
        parameters += 'text-anchor="middle" '
        parameters += 'thickness="' + thickness + '" '
        parameters += 'type="' + type_text + '" '
        parameters += tstamp
        parameters += hide
        parameters += transform
        parameters += '>' + text
        parameters += '</text>'

        return parameters
