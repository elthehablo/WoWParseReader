from importer import Importer
from parseExtractor import ParseExtractor

def main():
        #path = "source/to_read_files/"+input("enter filename (<filename>.txt): ")
        path = "source/to_read_files/felsworn.txt" # for testing
        imported = Importer(path)
        
        imported.import_parse()
        
        all_spells = ParseExtractor.extract_all_spells_for_entry(17339, imported.filecontents)
        
        
        print(all_spells) 
        return
    
if __name__ == "__main__":
    main()