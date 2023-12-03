from typing import Dict, List, Any
from re import search
import math

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
    
    @staticmethod
    def find_spawn_location_by_entry(entry: int, content_to_parse: List[str]) -> List[float]:
        possible_spawn_locations = []
        for idx, line in enumerate(content_to_parse):
            if search(r'Object Guid: Full: (.*?)Creature', line):
                entry_check = search(r'Entry: (.*?)Low:', line)
                if entry_check:
                    true_entry = int(entry_check.group(0).split(' ')[1])
                    if true_entry == entry:
                        coords_posis = idx+25
                        orientation_posis = idx+26
                        coords_line = content_to_parse[coords_posis]
                        orientation_line = content_to_parse[orientation_posis]
                        coords = search(r'X: (-?\d+\.\d+) Y: (-?\d+\.\d+) Z: (-?\d+\.\d+)', coords_line)
                        orientation = search(r'Orientation: (-?\d+\.\d+)', orientation_line)
                        coords_orientation_list = []
                        if coords:
                            grouped_list = coords.group(0).split(' ')
                            for i in range(len(grouped_list)):
                                if i%2 != 0:
                                    coords_orientation_list.append(float(grouped_list[i]))
                        else:
                            coords_orientation_list = [0.0, 0.0, 0.0]
                        if orientation:
                            grouped_list = orientation.group(0).split(' ')
                            coords_orientation_list.append(float(grouped_list[1]))
                        else:
                            coords_orientation_list.append(0.0)
                        possible_spawn_locations.append(coords_orientation_list)
        return possible_spawn_locations
    
    @staticmethod
    def find_average_wander_distance(entry: int, content_to_parse: List[str], spawn_location: List[float]) -> Dict[str, Any]:
        '''
        finds the wander details of a creature, such as:
        - max wandering distance
        - average wandering distance
        - amount of movement updates
        '''
        x_distance_list = []
        y_distance_list = []
        movement_updates = 0
        for idx, line in enumerate(content_to_parse):
            if search(r'ServerToClient: SMSG_ON_MONSTER_MOVE', line):
                entry_check = search(r'Entry: (.*?)Low:', content_to_parse[idx+1])
                if entry_check:
                    true_entry = int(entry_check.group(0).split(' ')[1])
                    if true_entry == entry:
                        coords = search(r'X: (-?\d+\.\d+) Y: (-?\d+\.\d+) Z: (-?\d+\.\d+)', content_to_parse[idx+2])
                        current_coords_list = []
                        if coords:
                            grouped_list = coords.group(0).split(' ')
                            for i in range(len(grouped_list)):
                                if i%2 != 0:
                                    current_coords_list.append(float(grouped_list[i]))
                        x_dist = abs(spawn_location[0]-current_coords_list[0])
                        y_dist = abs(spawn_location[1]-current_coords_list[1])
                        x_distance_list.append(x_dist)
                        y_distance_list.append(y_dist)
                        movement_updates += 1
        avg_x = sum(x_distance_list)/len(x_distance_list)
        avg_y = sum(y_distance_list)/len(y_distance_list)
        max_x = max(x_distance_list)
        max_y = max(y_distance_list)
        max_distance_from_spawn = math.sqrt(math.pow(max_x, 2)+math.pow(max_y, 2))
        dict_to_return = {
            'spawn_location': f"X: {spawn_location[0]} Y: {spawn_location[1]} Z: {spawn_location[2]} O: {spawn_location[3]}",
            'avg_x_wander': avg_x,
            'avg_y_wander': avg_y,
            'max_x_wander': max_x,
            'max_y_wander': max_y,
            'max_distance_from_spawn': max_distance_from_spawn,
            'no_recorded_movement_updates': movement_updates
        }
        return dict_to_return
    
    @staticmethod
    def gather_all_waypoints(entry: int, content_to_parse: List[str]):
        true_waypoints = []
        additional_waypoints = []
        for idx, line in enumerate(content_to_parse):
            if search(r'ServerToClient: SMSG_ON_MONSTER_MOVE', line):
                entry_check = search(r'Entry: (.*?)Low:', content_to_parse[idx+1])
                if entry_check:
                    true_entry = int(entry_check.group(0).split(' ')[1])
                    if true_entry == entry:
                        from_search_line = idx
                        while not search(r' Points:', content_to_parse[from_search_line]):
                            from_search_line += 1
                        coords = search(r'X: (-?\d+\.\d+) Y: (-?\d+\.\d+) Z: (-?\d+\.\d+)', content_to_parse[from_search_line])
                        current_coords_list = []
                        if coords:
                            grouped_list = coords.group(0).split(' ')
                            for i in range(len(grouped_list)):
                                if i%2 != 0:
                                    current_coords_list.append(float(grouped_list[i]))
                        if current_coords_list not in true_waypoints:
                            true_waypoints.append(current_coords_list)
                        additional_waypoint_counter = from_search_line+1
                        while search(r' WayPoints:', content_to_parse[additional_waypoint_counter]):
                            coords = search(r'X: (-?\d+\.\d+) Y: (-?\d+\.\d+) Z: (-?\d+\.\d+)', content_to_parse[additional_waypoint_counter])
                            current_coords_list = []
                            if coords:
                                grouped_list = coords.group(0).split(' ')
                                for i in range(len(grouped_list)):
                                    if i%2 != 0:
                                        current_coords_list.append(float(grouped_list[i]))
                            if current_coords_list not in additional_waypoints:
                                additional_waypoints.append(current_coords_list)
                            additional_waypoint_counter += 1
        return true_waypoints
    
    @staticmethod
    def print_waypoints_as_sql_insert(entry: int, name: str, waypoint_list: List[float]) -> None:
        f = open(f"{name}.sql", "w")
        wp_entry = entry*100
        delete_line = f"DELETE FROM `waypoints` WHERE `entry` = {wp_entry};"
        insert_preamble = "INSERT INTO `waypoints` (`entry`, `pointid`, `position_x`, `position_y`, `position_z`, `orientation`, `delay`, `point_comment`) VALUES"
        print(delete_line)
        print(insert_preamble)
        f.write(f"{delete_line}\n")
        f.write(f"{insert_preamble}\n")
        point_id = 1
        
        cleaned_waypoint_list = [sub_list for sub_list in waypoint_list if sub_list != []]
        
        for waypoint in cleaned_waypoint_list:
            if waypoint:
                print_line = f"({wp_entry}, {point_id}, {waypoint[0]}, {waypoint[1]}, {waypoint[2]}, NULL, 0, '{name}')"
                print_line = f"{print_line};" if point_id == len(cleaned_waypoint_list) else f"{print_line}," 
                print(print_line)
                f.write(f"{print_line}\n")
                point_id += 1
        f.close()
        
                        
        
        
        

def check_for_entry(data_to_check: List[str], current_id: int):
    return search(r'Entry: (.*?)Low:', data_to_check[current_id+1])
        
        
        