import numpy as np

class ParseExtractor:
    '''
    class with several static methods that extract different kinds of information from a parsed file
    '''
    
    @staticmethod
    def extract_version(toParseData):
        '''
        extracts version and returns it as a string
        '''
        assert(type(toParseData) == str), "parsed file does not have correctly typed data"
        
        N = np.size(toParseData)
        
        lineVersion = 0
        
        for i in range(N):
            if("# Detected build" in toParseData[i]):
                lineVersion = i
                break
        
        if(lineVersion == 0):
            print("error: version not found")
            return
        
        versionString = ""
        
        limit = 1000 #sets initial limit at an unreachable position
        
        for i in range(np.size(toParseData[lineVersion])):
            if (i > limit):
                versionString += toParseData[lineVersion][i] #if i is beyond the limit, which is at the initial V, it adds it
            if (toParseData[lineVersion][i] == "V"):
                versionString += "V"
                limit = i
        
        return versionString
            

        
        
        
        