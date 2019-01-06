import os
import part_data
from string import Template

identical_parts_header = """
//*********************************************************************************************
//  IDENTICAL PARTS UNLOCKS
//	This allows identical parts to unlock for free when one is unlocked
//  
//	DO NOT EDIT THIS FILE DIRECTLY!!!
//	This file is generated from Column A of the RP-0 Official Parts Tech Tree IDENTS Sheet
//
//*********************************************************************************************
"""

output_dir = os.getenv('PB_OUTPUT_DIR', "../../../GameData/RP-0/Tree/")
identical_part_template = Template("@PART[${name}]:FOR[xxxRP0] { %identicalParts = ${identical_parts} }\n")

def generate_identical_parts(parts):
    identical_parts_map = {}
    for part in parts:
        if part['name'] is not None and len(part['name']) > 0:
            if part['mod'] != 'Engine_Config' and not part['orphan']:
                if part['identical_part_name'] is not None and len(part['identical_part_name']) > 0:
                    idp = part['identical_part_name']
                    if idp not in identical_parts_map:
                        identical_parts_map[idp] = set()
                    identical_parts_map[idp].add(part['name'])
    identical_part_configs = ""
    for part_id in sorted(list(identical_parts_map.keys()), key=lambda x:x.lower()):
        sorted_names = list(identical_parts_map[part_id])
        sorted_names.sort(key=lambda x: x.lower())
        for name in sorted_names:
            sorted_parts = list(identical_parts_map[part_id])
            sorted_parts.sort()
            identical_part_configs += identical_part_template.substitute(name=name, identical_parts=",".join(sorted_parts))
    
    text_file = open(output_dir + "identicalParts.cfg", "w", newline='\n')
    text_file.write(identical_parts_header)
    text_file.write(identical_part_configs)
    text_file.close()
        