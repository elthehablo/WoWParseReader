from typing import Dict, List, Any
from datetime import datetime

class SpellCastCalculator:
    '''
    class that allows to calculate the spelltimers for a creature
    '''
    
    def __init__(self, list_dict_spell_timer: List[Dict[str, Any]]):
        self.list_dict_spell_timer = list_dict_spell_timer
    
    def compute_timers(self):
        final_list_dict = []
        spell_entries = get_all_spell_entries(self.list_dict_spell_timer)
        timestamp_format = "%H:%M:%S.%f"
        for idx, item in enumerate(self.list_dict_spell_timer):
            if item.get('attackStartTime', ""):
                combat_start_datetime = datetime.strptime(item['attackStartTime'], timestamp_format)
                for spell_entry in spell_entries:
                    counter = idx+1
                    while self.list_dict_spell_timer[counter].get('spell_id', "") != spell_entry:
                        counter+=1
                    initial_spell_cast_timestamp = datetime.strptime(
                        self.list_dict_spell_timer[counter]['timestamp'], timestamp_format
                    )
                    timedelta = initial_spell_cast_timestamp-combat_start_datetime
                    dict = {
                        'entry': item['entry'],
                        'casterGUID': item['casterGUID'],
                        'spell_id': spell_entry,
                        'timedeltaInitialCast': timedelta.total_seconds()
                    }
                    final_list_dict.append(dict)
                    #now we want all consecutive spells
                    current_spell_cast_timestamp = initial_spell_cast_timestamp
                    counter += 1
                    castno = 1
                    while self.list_dict_spell_timer[counter].get('timestamp', ""):
                        if (self.list_dict_spell_timer[counter].get('spell_id') == spell_entry):
                            new_timestamp = datetime.strptime(
                                self.list_dict_spell_timer[counter]['timestamp'], timestamp_format
                            )
                            timedelta = new_timestamp - current_spell_cast_timestamp
                            current_spell_cast_timestamp = new_timestamp #new value to check from comes the new entry point
                            dict = {
                                'entry': item['entry'],
                                'casterGUID': item['casterGUID'],
                                'spell_id': spell_entry,
                                'timebetweenlastcast': timedelta.total_seconds(),
                                'noOfCast': str(castno)
                            }
                            final_list_dict.append(dict)
                            castno += 1
                        counter += 1
                        if counter == len(self.list_dict_spell_timer):
                            break #before we check out of bounds
        return final_list_dict

def get_all_spell_entries(dict_to_check: List[Dict[str, Any]]):
    spell_entry_list = []
    for item in dict_to_check:
        spell_id = item.get('spell_id', "")
        if spell_id and spell_id not in spell_entry_list:
            spell_entry_list.append(spell_id) 
    return spell_entry_list