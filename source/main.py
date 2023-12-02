from importer import Importer
from parseExtractor import ParseExtractor
from spellcast import SpellCastCalculator
import json

def main():
        #path = "source/to_read_files/"+input("enter filename (<filename>.txt): ")
        path = "source/to_read_files/felsworn.txt" # for testing
        imported = Importer(path)
        
        imported.import_parse()
        
        all_spells = ParseExtractor.extract_all_spells_for_entry(17339, imported.filecontents)
        
        spell_cast_calculator = SpellCastCalculator(all_spells)
        
        spell_cast_calculator.compute_timers()
        
        final_timers = spell_cast_calculator.compute_final_times()
        #jsons
        print("all timers:")
        timers_json = json.dumps(spell_cast_calculator.calculated_spell_times, indent=8)
        print(timers_json)
        
        print("")
        print("calculated spell timers:")
        calculated_timers_json = json.dumps(final_timers, indent = 8)
        print(calculated_timers_json)
        return
    
if __name__ == "__main__":
    main()