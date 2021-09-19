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
        #input = input[1:]
        
        body = json.dumps(input)
        
        svg = '<' + tag + '>'
        svg += body
        svg += '</' + tag + '>'

        return svg


    def From_SVG(self, svg):
        print("a")
