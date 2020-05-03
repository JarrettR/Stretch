from bs4 import BeautifulSoup




class SexpressionWriter(object):
    def __init__(self, svg):


        # May or may not need to actually use an XML parser instead of HTML!
        #self.soup = BeautifulSoup(svg, 'lxml-xml')
        self.soup = BeautifulSoup(svg, 'html.parser')


    def display(self):
        
        print(self.soup.prettify())