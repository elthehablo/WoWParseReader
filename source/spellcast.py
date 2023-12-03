from typing import Dict, List, Any
from datetime import datetime

class SpellCastCalculator:
    '''
    class that allows to calculate the spelltimers for a creature
    '''
    
    def __init__(self, list_dict_spell_timer: List[Dict[str, Any]]):
        self.list_dict_spell_timer = list_dict_spell_timer
        self.calculated_spell_times = []
    
    def compute_timers(self):
        '''
        computes the spellcast initial and repeat values for 
        '''
        final_list_dict = []
        spell_entries = get_all_spell_entries(self.list_dict_spell_timer)
        timestamp_format = "%H:%M:%S.%f"
        breakcondition = False #break on no repeating
        for idx, item in enumerate(self.list_dict_spell_timer):
            if item.get('attackStartTime', ""):
                combat_start_datetime = datetime.strptime(item['attackStartTime'], timestamp_format)
                for spell_entry in spell_entries:    
                    counter = idx+1
                    while self.list_dict_spell_timer[counter].get('spell_id', "") != spell_entry:
                        counter+=1
                        if counter == len(self.list_dict_spell_timer):
                            #happens when no repeat found
                            breakcondition = True
                            break
                    if breakcondition:
                        continue
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
                    cast_counter = counter + 1
                    castno = 1
                    while self.list_dict_spell_timer[cast_counter].get('timestamp', ""):
                        if (self.list_dict_spell_timer[cast_counter].get('spell_id') == spell_entry):
                            new_timestamp = datetime.strptime(
                                self.list_dict_spell_timer[cast_counter]['timestamp'], timestamp_format
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
                        cast_counter += 1
                        if cast_counter == len(self.list_dict_spell_timer):
                            break #before we check out of bounds
        self.calculated_spell_times = final_list_dict
    
    def compute_final_times(self):
        spell_entries = get_all_spell_entries(self.list_dict_spell_timer)
        guid_list = get_all_guids(self.list_dict_spell_timer)
        final_dict = {}
        current_initial_timer_list = {}
        current_repeat_timer_list = {}
        for spell_entry in spell_entries:
            final_dict = final_dict | {spell_entry: {
                'initial_min_time': "",
                'initial_avg_time': "",
                'initial_max_time': "",
                'repeat_min_time': "",
                'repeat_avg_time': "",
                'repeat_max_time': "",
            }}
            current_initial_timer_list[spell_entry] = []
            current_repeat_timer_list[spell_entry] = []
        for calc_item in self.calculated_spell_times:
            for spell_entry in spell_entries:
                
                for guid in guid_list:
                    if calc_item.get('spell_id', "") == spell_entry \
                        and calc_item.get('casterGUID', "") == guid:
                        if calc_item.get('timedeltaInitialCast', ""):
                            current_initial_timer_list[spell_entry].append(float(calc_item['timedeltaInitialCast']))
                        elif calc_item.get('timebetweenlastcast', ""):
                            current_repeat_timer_list[spell_entry].append(float(calc_item['timebetweenlastcast']))
        current_repeat_timer_list = fill_empty_repeat_lists(current_repeat_timer_list)
        for spell_entry in spell_entries:
            current_initial_min_value = min(current_initial_timer_list[spell_entry])
            current_initial_avg_value = sum(current_initial_timer_list[spell_entry])/len(current_initial_timer_list[spell_entry])
            current_initial_max_value = current_initial_min_value + 2*(current_initial_avg_value-current_initial_min_value)
            current_repeat_min_value = min(current_repeat_timer_list[spell_entry])
            current_repeat_avg_value = sum(current_repeat_timer_list[spell_entry])/len(current_repeat_timer_list[spell_entry])
            current_repeat_max_value = current_repeat_min_value + 2*(current_repeat_avg_value-current_repeat_min_value)
            final_dict[spell_entry]['initial_min_time'] = current_initial_min_value
            final_dict[spell_entry]['initial_avg_time'] = current_initial_avg_value
            final_dict[spell_entry]['initial_max_time'] = current_initial_max_value
            final_dict[spell_entry]['repeat_min_time'] = current_repeat_min_value
            final_dict[spell_entry]['repeat_avg_time'] = current_repeat_avg_value
            final_dict[spell_entry]['repeat_max_time'] = current_repeat_max_value
        return final_dict

def get_all_spell_entries(dict_to_check: List[Dict[str, Any]]):
    spell_entry_list = []
    for item in dict_to_check:
        spell_id = item.get('spell_id', "")
        if spell_id and spell_id not in spell_entry_list:
            spell_entry_list.append(spell_id) 
    return spell_entry_list

def get_all_guids(dict_to_check: List[Dict[str, Any]]):
    guid_list = []
    for item in dict_to_check:
        guid = item.get('casterGUID', "")
        if guid and guid not in guid_list:
            guid_list.append(guid)
    return guid_list

def fill_empty_repeat_lists(dict_list_to_check):
    '''
    adds a 0 to an empty repeat list so that the average calculations don't break
    '''

    for dict_item in dict_list_to_check:
        if len(dict_list_to_check[dict_item]) == 0:
            dict_list_to_check[dict_item] = [0]
    return dict_list_to_check