import importer

def main():
        path = "source/to_read_files/"+input("enter filename (<filename>.txt): ")
        imported = importer.Importer(path)
        
        importdata1, importdata2 = imported.import_parse()
        
        print(importdata1) 
        return
    
if __name__ == "__main__":
    main()