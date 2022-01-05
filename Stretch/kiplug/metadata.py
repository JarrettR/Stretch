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
        
        
        if type(input) == unicode:
            return ''
            
        tag = str(input[0])
        input = input[1:]
        
        body = json.dumps(input)
        svg = '<' + tag + '>'
        svg += str(body)
        svg += '</' + tag + '>'

        return svg


    def From_SVG(self, svg):
        # content = svg.svg.kicad.contents[0][0:-1]
        pcb = []

        for tag in svg.svg.kicad.children:
            if tag.name != None:
                chunk = [tag.name]
                try:
                    chunk += json.loads(tag.decode_contents())
                except:
                    assert False,"Bad metadata {}: {} - {}".format(type(tag), tag, chunk)
                    
                pcb += [chunk]
        # content = '[' + content + ' ]'
        # meta = json.loads(content)
        # print(meta)
        return pcb
