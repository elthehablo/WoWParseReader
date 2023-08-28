import numpy as np

import parseExtractor

class Importer:
    '''
    class that allows the importing of parsed txt files
    '''
    
    def __init__(self, filename):
        self.filename = filename
        
    def import_parse(self):
        '''
        imports a parse and stores into into a string array using newline as a delimiter as a delimiter, also returns a separate arraylist with the filename and other info in it
        '''
        metaData = np.array([self.filename])
        
        fullData = open(self.filename, 'r')
        
        fullData.readlines()
        
        fullData.close()
        
        print(fullData)
        
        fullData = np.array(fullData)
        print(type(fullData[0]))
        
        size = np.size(fullData)
        
        version = parseExtractor.ParseExtractor.extract_version(fullData)
        
        metaData = np.append(metaData, np.array([size, version]))
        
        return metaData, fullData
        
        
        
        
        
        
        
        
        