import numpy as np
from re import search

class ParseExtractor:
    '''
    class with several static methods that extract different kinds of information from a parsed file
    '''
    
    @staticmethod
    def extract_version(to_parse_data: str):
        '''
        extracts version and returns it as a string
        '''
        assert(type(to_parse_data) == str), "parsed file does not have correctly typed data"
        
        version_string = search(r'Detected build: (.*?)#', to_parse_data)
        
        real_version_string = version_string.group(0)
    
        
        return real_version_string
    
    @staticmethod
    def extract_all_spells_for_entry(entry: int):
        '''
        extracts all the spells, with a creature guid and entry at the timestamp
        '''
        return
            

        
        
        
        