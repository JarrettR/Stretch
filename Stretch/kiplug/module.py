import sys


from bs4 import BeautifulSoup

import base64
import math
from .svgpath import parse_path

from .arc import Arc
from .circle import Circle
from .curve import Curve
from .layers import Layers
from .line import Line
from .metadata import Metadata
from .pad import Pad
from .poly import Poly
from .segment import Segment
from .text import Text
from .via import Via
from .zone import Zone


# https://github.com/KiCad/kicad-source-mirror/blob/93466fa1653191104c5e13231dfdc1640b272777/pcbnew/plugins/kicad/pcb_parser.cpp#L2839

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


pxToMM = 96 / 25.4

class Module(object):

    def __init__(self):
        self.symbol = ''
        self.version = ''
        self.generator = ''
        self.locked = False
        self.placed = False
        self.layer = ''
        self.tedit = ''
        self.tstamp = ''
        self.at = []
        self.descr = ''
        self.tags = ''
        self.property = []
        self.path = ''
        self.autoplace_cost90 = ''
        self.autoplace_cost180 = ''
        self.solder_mask_margin = ''
        self.solder_paste_margin = ''
        self.solder_paste_ratio = ''
        self.clearance = ''
        self.zone_connect = ''
        self.thermal_width = ''
        self.thermal_gap = ''
        self.attr = ''
        self.fp_text = []
        self.fp_arc = []
        self.fp_circle = []
        self.fp_curve = []
        self.fp_rect = []
        self.fp_line = []
        self.fp_poly = []
        self.pad = []
        self.model = ''
        self.zone = []
        self.group = ''
        
        
    def From_PCB(self, pcblist):

        # Why is this necessary?
        if sys.version_info[0] != 3:
            if type(pcblist[1]) == unicode:
                pcblist[1] = str(pcblist[1])
            
        if type(pcblist[1]) != str:
            assert False,"Module: Unexpected symbol type {}: {}".format(type(pcblist[1]), pcblist[1])
            return None

        self.symbol = pcblist[1]

        for item in pcblist[2:]:


            if item[0] == 'version':
                self.version = item[1]
                
            if item[0] == 'generator':
                self.generator = item[1]
                
            if item[0] == 'locked':
                self.locked = True
                
            if item[0] == 'placed':
                self.placed = True
                
            if item[0] == 'layer':
                self.layer = item[1]
                
            if item[0] == 'tedit':
                self.tedit = item[1]
                
            if item[0] == 'tstamp':
                self.tstamp = item[1]
            
            if item[0] == 'at':
                self.at += item[1:]
                
            if item[0] == 'descr':
                self.descr = item[1]
                
            if item[0] == 'tags':
                self.tags = item[1]
                
            if item[0] == 'property':
                self.property.append(item[1:])
                
            if item[0] == 'path':
                self.path = item[1]
                
            if item[0] == 'autoplace_cost90':
                self.autoplace_cost90 = item[1]
                
            if item[0] == 'autoplace_cost180':
                self.autoplace_cost180 = item[1]
                
            if item[0] == 'solder_mask_margin':
                self.solder_mask_margin = item[1]
                
            if item[0] == 'solder_paste_margin':
                self.solder_paste_margin = item[1]
                
            if item[0] == 'solder_paste_ratio':
                self.solder_paste_ratio = item[1]
                
            if item[0] == 'clearance':
                self.clearance = item[1]
                
            if item[0] == 'zone_connect':
                self.zone_connect = item[1]
                
            if item[0] == 'thermal_width':
                self.thermal_width = item[1]
                
            if item[0] == 'thermal_gap':
                self.thermal_gap = item[1]
                
            if item[0] == 'attr':
                self.attr = ','.join(item[1:])
                
            if item[0] == 'fp_text':
                text = Text()
                text.From_PCB(item)
                self.fp_text.append(text)
                
            if item[0] == 'fp_arc':
                arc = Arc()
                arc.From_PCB(item)
                self.fp_arc.append(arc)
                
            if item[0] == 'fp_circle':
                circle = Circle()
                circle.From_PCB(item)
                self.fp_circle.append(circle)
                
            # if item[0] == 'fp_circle':
            # if item[0] == 'fp_curve':
            # if item[0] == 'fp_rect':
                
            if item[0] == 'fp_line':
                line = Line()
                line.From_PCB(item)
                self.fp_line.append(line)
                
            if item[0] == 'fp_poly':
                poly = Poly()
                poly.From_PCB(item)
                self.fp_poly.append(poly)
            
            if item[0] == 'pad':
                pad = Pad()
                pad.From_PCB(item)
                self.pad.append(pad)

            if item[0] == 'model':
                model = item[1] + ';'
                #offset
                model += item[2][1][1] + ',' + item[2][1][2] + ',' + item[2][1][3] + ';'
                #scale
                model += item[3][1][1] + ',' + item[3][1][2] + ',' + item[3][1][3] + ';'
                #rotate
                model += item[4][1][1] + ',' + item[4][1][2] + ',' + item[4][1][3] + ';'
                self.model = model

            # if item[0] == 'zone':
            # if item[0] == 'group':


    def To_PCB(self):
        module = ['module', self.symbol]
        if self.version:
            module.append(self.version)
            
        module.append(['layer', self.layer])

        if self.version:
            module.append(['version', self.version])

        if self.generator:
            module.append(['generator', self.generator])

        module.append(self.at)

        if self.locked == True:
            module.append('locked')

        if self.placed == True:
            module.append('placed')

        if self.tedit:
            module.append(['tedit', self.tedit])

        if self.tstamp:
            module.append(['tstamp', self.tstamp])

        if self.descr:
            module.append(['descr', self.descr.replace('"', '\\"')])

        if self.tags:
            module.append(['tags', self.tags])

        if self.property:
            for prop in self.property:
                module.append(['property'] + prop)

        # if self.path:
        #     module.append(['tstamp', self.tstamp])

        if self.autoplace_cost90:
            module.append(['autoplace_cost90', self.autoplace_cost90])

        if self.autoplace_cost180:
            module.append(['autoplace_cost180', self.autoplace_cost180])

        if self.solder_mask_margin:
            module.solder_mask_margin(['solder_mask_margin', self.solder_mask_margin])

        if self.solder_paste_margin:
            module.append(['solder_paste_margin', self.solder_paste_margin])

        if self.solder_paste_ratio:
            module.append(['solder_paste_ratio', self.solder_paste_ratio])

        if self.clearance:
            module.append(['clearance', self.clearance])

        if self.zone_connect:
            module.append(['zone_connect', self.zone_connect])

        if self.thermal_width:
            module.append(['thermal_width', self.thermal_width])

        if self.thermal_gap:
            module.append(['thermal_gap', self.thermal_gap])

        if self.path:
            module.append(['path', self.path])

        if self.attr:
            attr = self.attr.split(',')
            module.append(['attr'] + attr)

        for text in self.fp_text:
            module.append(text.To_PCB())

        for poly in self.fp_poly:
            module.append(poly.To_PCB(fp = True))

        for line in self.fp_line:
            module.append(line.To_PCB(fp = True))

        for arc in self.fp_arc:
            module.append(arc.To_PCB(fp = True))

        for curve in self.fp_curve:
            module.append(curve.To_PCB(fp = True))

        for circle in self.fp_circle:
            module.append(circle.To_PCB(fp = True))

        for pad in self.pad:
            module.append(pad.To_PCB())

        if self.model:
            module.append(['model'] + self.model)

        if self.group:
            module.append(['group', self.group])


        return module



    def To_SVG(self, hiddenLayers = []):
        svg = BeautifulSoup('<g type="module" name="' + self.symbol + '">', 'html.parser')
        

        if self.version != '':
            svg.g['version'] = self.version
            
        if self.generator != '':
            svg.g['generator'] = self.generator
            
        if self.locked == True:
            svg.g['locked'] = 'true'
            
        if self.placed == True:
            svg.g['placed'] = 'true'
            
        if self.layer != '':
            svg.g['layer'] = self.layer
        else:
            svg.g['layer'] = 'F.Cu'
            
        if self.tedit != '':
            svg.g['tedit'] = self.tedit
            
        if self.tstamp != '':
            svg.g['tstamp'] = self.tstamp

        #at
        x = float(self.at[0]) * pxToMM
        y = float(self.at[1]) * pxToMM
        rotate = 0

        transform = 'translate(' + str(x) + ',' + str(y) + ')'

        if len(self.at) > 2:
            rotate = float(self.at[2])
            transform += ' rotate(' + str(-1 * rotate) + ')'

        svg.g['transform'] = transform

        if self.descr != '':
            svg.g['descr'] = self.descr

        if self.tags != '':
            svg.g['tags'] = self.tags

        if len(self.property) > 0:
            propstr = ''
            for prop in self.property:
                propstr += "{}:{} ".format(str(base64.b64encode(prop[0].encode("utf-8")), "utf-8"), str(base64.b64encode(prop[1].encode("utf-8")), "utf-8"))
            svg.g['property'] = propstr

        if self.path != '':
            svg.g['path'] = self.path

        if self.autoplace_cost90 != '':
            svg.g['autoplace_cost90'] = self.autoplace_cost90

        if self.autoplace_cost180 != '':
            svg.g['autoplace_cost180'] = self.autoplace_cost180

        if self.solder_mask_margin != '':
            svg.g['solder_mask_margin'] = self.solder_mask_margin

        if self.solder_paste_margin != '':
            svg.g['solder_paste_margin'] = self.solder_paste_margin

        if self.solder_paste_ratio != '':
            svg.g['solder_paste_ratio'] = self.solder_paste_ratio

        if self.solder_paste_ratio != '':
            svg.g['solder_paste_ratio'] = self.solder_paste_ratio

        if self.zone_connect != '':
            svg.g['zone_connect'] = self.zone_connect

        if self.thermal_width != '':
            svg.g['thermal_width'] = self.thermal_width

        if self.thermal_gap != '':
            svg.g['thermal_gap'] = self.thermal_gap

        if self.attr != '':
            svg.g['attr'] = self.attr
            
        for item in self.fp_text:
            # tag = BeautifulSoup(item.To_SVG(), 'html.parser')
            # layer = item.layer
            #  svg.find('g', {'inkscape:label': layer}, recursive=False).append(tag)
            tag = BeautifulSoup(item.To_SVG(rotate * -1, hiddenLayers), 'html.parser')
            svg.g.append(tag)
            #Todo: hide elements that are supposed to be on hiddenlayers
        
        for item in self.fp_arc:
            tag = BeautifulSoup(item.To_SVG(fp = True), 'html.parser')
            svg.g.append(tag)
            
        for item in self.fp_circle:
            tag = BeautifulSoup(item.To_SVG(fp = True), 'html.parser')
            svg.g.append(tag)

        for item in self.fp_curve:
            tag = BeautifulSoup(item.To_SVG(fp = True), 'html.parser')
            svg.g.append(tag)

        for item in self.fp_rect:
            tag = BeautifulSoup(item.To_SVG(fp = True), 'html.parser')
            svg.g.append(tag)
        
        for item in self.fp_line:
            tag = BeautifulSoup(item.To_SVG(fp = True), 'html.parser')
            svg.g.append(tag)
            
        for item in self.fp_poly:
            tag = BeautifulSoup(item.To_SVG(fp = True), 'html.parser')
            svg.g.append(tag)
        
        for item in self.pad:
            tag = BeautifulSoup(item.To_SVG(rotate * -1), 'html.parser')
            svg.g.append(tag)
            
        if self.model != '':
            svg.g['model'] = self.model
        # if self.zone != '':
        # if self.group != '':
            

        return svg


        
    def From_SVG(self, tag):
        transform = tag['transform'].strip()
        
        x = 0.0
        y = 0.0
        if 'translate(' in transform:
            translate = transform[transform.find('translate(') + 10:-1]
            translate = translate[0:translate.find(')')]
            x, y = translate.split(',')
            x = float(x) / pxToMM
            y = float(y) / pxToMM

        rotate = 0.0
        if 'rotate(' in transform:
            rotate = transform[transform.find('rotate(') + 7:-1]
            if ',' in rotate:
                rotate, x_zero, y_zero = rotate.split(',')
                rotate = float(rotate)
                x_zero = float(x_zero) / pxToMM
                y_zero = float(y_zero) / pxToMM
                #Rotate along nonzero rotation axis
                hyp = math.sqrt(x_zero*x_zero + y_zero*y_zero)
                angle = -1.0 * math.atan2(-1.0 * y_zero, -1.0 * x_zero)

                angle -= math.radians(rotate)
                y_offset = math.sin(angle) * hyp
                x_offset = math.cos(angle) * hyp

                x = x_zero + x_offset
                y = y_zero - y_offset
                
            rotate = float(rotate) * -1


        self.symbol = tag['name']
                
        if tag.has_attr('layer'):
            self.layer = tag['layer']

        if tag.has_attr('tedit'):
            self.tedit = tag['tedit']

        if tag.has_attr('property'):
            proplist = tag['property'].split()
            for prop in proplist:
                k, v = prop.split(":")
                self.property.append([str(base64.b64decode(k), "utf-8"), str(base64.b64decode(v), "utf-8")])

        if tag.has_attr('tstamp'):
            self.tstamp = tag['tstamp']

        at = ['at', str(x), str(y), str(rotate)]
        self.at = at
        
        if tag.has_attr('descr'):
            self.descr = tag['descr']

        if tag.has_attr('tags'):
            self.tags = tag['tags']

        if tag.has_attr('path'):
            self.path = tag['path']

        if tag.has_attr('attr'):
            self.attr = tag['attr']
            
        for text in tag.find_all('text'):
            t = Text()
            t.From_SVG(text, rotate)
            self.fp_text.append(t)

        if tag.has_attr('model'):
            modeltag = tag['model']
            model = []
            model.append(modeltag[0:modeltag.find(';')])
            modeltag = modeltag[modeltag.find(';') + 1:]
            offset = ['xyz'] + modeltag[0:modeltag.find(';')].split(',')
            modeltag = modeltag[modeltag.find(';') + 1:]
            scale = ['xyz'] + modeltag[0:modeltag.find(';')].split(',')
            modeltag = modeltag[modeltag.find(';') + 1:]
            modelrotate = ['xyz'] + modeltag[0:modeltag.find(';')].split(',')
            model.append(['offset', offset])
            model.append(['scale', scale])
            model.append(['rotate', modelrotate])
            self.model = model

        for tagpath in tag.find_all('path'):
            # if path.has_attr('type') == True and path['type'] == 'zone':
            #     self.zone.append(Zone.From_Svg(path))
            # print(tag)
            if tagpath.has_attr('type') == True and tagpath['type'] == 'fp_poly':
                poly = Poly()
                poly.From_SVG(tagpath)
                self.fp_poly.insert(0, poly)
            elif tagpath.has_attr('type') == True and tagpath['type'] == 'fp_line':
                paths = parse_path(tagpath['d'])

                for path in paths:
                    line = Line()
                    line.From_SVG(tagpath, path)
                    self.fp_line.insert(0, line)
            elif tagpath.has_attr('type') == True and tagpath['type'] == 'fp_arc':
                paths = parse_path(tagpath['d'])

                for path in paths:
                    arc = Arc()
                    arc.From_SVG(tagpath, path)
                    self.fp_arc.insert(0, arc)
                    
            elif tagpath.has_attr('type') == True and tagpath['type'] == 'fp_curve':
                curve = Curve()
                curve.From_SVG(path)
                self.fp_curve.insert(0, curve)
            # else:
                # segment, gr_line, gr_arc, gr_curve = self.Parse_Segment(path)
                # segments = segments + segment
                # gr_line[0][0] = 'fp_line'
                # gr_lines += gr_line
                # gr_arcs += gr_arc
                # gr_curves += gr_curve
        for tagpath in tag.find_all('rect'):
            if tagpath.has_attr('type') == True and tagpath['type'] == 'pad':
                pad = Pad()
                pad.From_SVG(tagpath, rotate)
                self.pad.append(pad)

        for tagpath in tag.find_all('circle'):
            if tagpath.has_attr('type') == True and tagpath['type'] == 'pad':
                pad = Pad()
                pad.From_SVG(tagpath, rotate)
                self.pad.append(pad)
            elif tagpath.has_attr('type') == True and tagpath['type'] == 'fp_circle':
                circle = Circle()
                circle.From_SVG(tagpath)
                self.fp_circle.append(circle)

        for tagpath in tag.find_all('ellipse'):
            if tagpath.has_attr('type') == True and tagpath['type'] == 'pad':
                pad = Pad()
                pad.From_SVG(tagpath, rotate)
                self.pad.append(pad)
