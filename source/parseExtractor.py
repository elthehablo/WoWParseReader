from typing import Dict, List, Any
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
    def extract_all_spells_for_entry(entry: int, content_to_parse: List[str]) -> List[Dict[str, Any]]:
        '''
        extracts all the spells, with a creature guid and entry at the timestamp
        '''
        spell_data_list = []
        count = 0
        for idx, line in enumerate(content_to_parse):
            if search(r'ServerToClient: SMSG_ATTACK_START', line):
                creature_entry_extracted = check_for_entry(content_to_parse, idx)
                if creature_entry_extracted:
                    timestamp = search(r'Time: (\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}\.\d+)', line).group(0)
                    caster_guid_extracted = search(r'Full: (.*?)Creature', content_to_parse[idx+1])
                    timestamp_final = timestamp.split(' ')[2]
                    caster_guid_final = caster_guid_extracted.group(0).split(' ')[1]
                    attack_start_dict = {
                        'entry': str(entry),
                        'casterGUID': caster_guid_final,
                        'attackStartTime': timestamp_final
                    }
                    spell_data_list.append(attack_start_dict)
            elif search(r'ServerToClient: SMSG_SPELL_START', line):
                creature_entry_extracted = check_for_entry(content_to_parse, idx)
                if creature_entry_extracted:
                    timestamp = search(r'Time: (\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}\.\d+)', line).group(0)
                    entry_check = int(creature_entry_extracted.group(0).split(' ')[1])
                    if entry_check == entry:
                        caster_guid_extracted = search(r'Full: (.*?)Creature', content_to_parse[idx+1])
                        spell_id_extracted = search(r'SpellID: (.*?) \(', content_to_parse[idx+5])
                        timestamp_final = timestamp.split(' ')[2]
                        caster_guid_final = caster_guid_extracted.group(0).split(' ')[1]
                        spell_id_final = spell_id_extracted.group(0).split(' ')[1]
                        dict_to_put_in_list = {
                            'entry': str(entry),
                            'casterGUID': caster_guid_final,
                            'timestamp': timestamp_final,
                            'spell_id': spell_id_final,
                            'count': str(count)
                        }
                        spell_data_list.append(dict_to_put_in_list)
                        count += 1
        return spell_data_list

def check_for_entry(data_to_check: List[str], current_id: int):
    return search(r'Entry: (.*?)Low:', data_to_check[current_id+1])
        
        
        