from typing import List, Dict, Any
from re import search


class CManGOS:
    @staticmethod
    def parse_cmangos_loot_to_list_dict(text_file_to_parse: List[str]):
        dict_list = {}
        current_word = ""
        for character in text_file_to_parse[1][1:]:
            if character == "|":
                dict_list = dict_list | {current_word: []}
                current_word = ""
            elif character != " ":
                current_word += character
        dict_list_keys = list(dict_list.keys())
        for line in text_file_to_parse[3:]:
            header_counter = 0
            current_word = ""
            for idx, character in enumerate(line[1:]):
                if idx == len(line[1:]) - 1:
                    continue
                if character == "|":
                    dict_list[dict_list_keys[header_counter]].append(current_word)
                    header_counter += 1
                    current_word = ""
                elif character != " ":
                    if character == "'":
                        current_word += "\\'"
                    else:
                        current_word += character
                else:
                    if search(r"[A-z]", line[1:][idx-1]):
                        if search(r"[A-z]", line[1:][idx+1]):
                           current_word += character 
        return dict_list
    
    @staticmethod
    def dict_list_to_ref_loot_insert(dict_list_to_inspect, name_to_give: str, item: int, item_name: str):
        f = open(f"{name_to_give}.sql", "w")
        entries = dict_list_to_inspect.get("entry", [0])
        entry_string = f"({', '.join(entries)})"
        delete_line = f"DELETE FROM `creature_loot_template` WHERE `Entry` IN {entry_string};"
        insert_preamble = "INSERT INTO `creature_loot_template` (`Entry`, `Item`, `Reference`, `Chance`, `QuestRequired`, `LootMode`, `GroupId`, `MinCount`, `MaxCount`, `Comment`) VALUES"
        print(delete_line)
        print(insert_preamble)
        f.write(f"{delete_line}\n")
        f.write(f"{insert_preamble}\n")
        point_id = 1
        
        keys = list(dict_list_to_inspect.keys())
        
        for i in range(len(dict_list_to_inspect[keys[0]])):
            print_line = f"({dict_list_to_inspect['entry'][i]}, {item}, 0, {dict_list_to_inspect['ChanceOrQuestChance'][i]}, 0, 1, 0, 1, 1, '{dict_list_to_inspect['LootId'][i]} - {item_name}')"
            print_line = f"{print_line};" if i == len(dict_list_to_inspect[keys[0]]) - 1 else f"{print_line},"
            print(print_line)
            f.write(f"{print_line}\n")

        f.close()
                        
    
    

    