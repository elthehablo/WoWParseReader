from importer import Importer
from parseExtractor import ParseExtractor
from spellcast import SpellCastCalculator
from cmangosstuff import CManGOS
import json

def main():
        path = "source/to_read_files/"+input("enter filename (<filename>.txt): ")
        #path = "source/to_read_files/potion.txt" # for testing
        imported = Importer(path)
        
        npc_entry = int(input("enter entry id: "))
        
        imported.import_parse()
              
        choice = input("what action do you want? [spells/wander/waypoints/cmangostabletoinsert] ")
        
        match choice:
                case "spells":
                        all_spells = ParseExtractor.extract_all_spells_for_entry(npc_entry, imported.filecontents)
                        
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
                case "wander":
                        spawn_locations = ParseExtractor.find_spawn_location_by_entry(npc_entry, imported.filecontents)
                        avg_wander_movement = ParseExtractor.find_average_wander_distance(npc_entry, imported.filecontents, spawn_locations[0])
                        print("average wander movements:")
                        wander_movements = json.dumps(avg_wander_movement, indent = 8)
                        print(wander_movements)
                        return
                case "waypoints":
                        waypoints = ParseExtractor.gather_all_waypoints(npc_entry, imported.filecontents)
                        name = input("Enter name for waypoint comment: ")
                        ParseExtractor.print_waypoints_as_sql_insert(npc_entry, name, waypoints)
                        return
                case "cmangostabletoinsert":
                        table_of_data = CManGOS.parse_cmangos_loot_to_list_dict(imported.filecontents)
                        delete_heroics = True if input("Delete heroic entries? [y/n]") == "y" else False
                        if delete_heroics:
                                table_of_data = CManGOS.collect_and_delete_heroic_entries(table_of_data)
                        item_name = input(f"Name of item corresponding to id {npc_entry}: ")
                        CManGOS.dict_list_to_ref_loot_insert(table_of_data, item_name, npc_entry, item_name)
                        return
                case _:
                        return
    
if __name__ == "__main__":
    main()