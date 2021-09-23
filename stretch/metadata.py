import json

class Metadata(object):

    def __init__(self):
        self.tstamp = ''
        


    # Not used, no processing done
    # def From_PCB(self, pcb):
    # def To_PCB(self):

    def To_SVG(self, input):
        # This will just take whatever data and store it in an XML tag as JSON
        # Hacky, but we don't care about it other than to be able to load it back in later

       
        tag = input[0]
        # print(tag)
        input = input[1:]
        
        body = json.dumps(input)
        svg = '<' + tag + '>'
        svg += body
        svg += '</' + tag + '>'
        # print(svg)

        return svg


    def From_SVG(self, svg):
        # content = svg.svg.kicad.contents[0][0:-1]
        pcb = []

        for tag in svg.svg.kicad.children:
            chunk = [tag.name]
            chunk += tag.contents
            pcb += chunk
        # content = '[' + content + ' ]'
        # meta = json.loads(content)
        # print(meta)
        return pcb
