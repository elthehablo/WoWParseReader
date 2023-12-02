import numpy as np

import parseExtractor

class Importer:
    '''
    class that allows the importing of parsed txt files
    '''
    
    def __init__(self, filename):
        self.filename = filename
        self.filecontents = []
        
    def import_parse(self) -> None:
        '''
        imports a parse and stores into into a string array using newline as a delimiter as a delimiter, also returns a separate arraylist with the filename and other info in it
        '''
        with open(self.filename) as file:
            full_data = file.read()
            
        line_list = full_data.split('\n')
        self.filecontents = line_list
        
        
        
        
        
        
        
        
        