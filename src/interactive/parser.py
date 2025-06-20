# interactive/parser.py

import sys
import re
import time
from getpass import getpass

def safe_input(text: str, hidden: bool = False) -> str:
    try:
        result = input(text) if not hidden else getpass(text)
    except (KeyboardInterrupt, EOFError):
        print("Interrupted.")
        safe_sleep(.89)
        sys.exit(1)
    
    return result

def safe_sleep(seconds: int):
    try:
        time.sleep(seconds)
    except KeyboardInterrupt:
        pass

def match_couple(arg: str) -> bool:
    r = re.compile(r"[a-zA-Z]+\.[a-zA-Z]+")
    return bool(r.match(arg))

def match_single(arg: str) -> bool:
    r = re.compile(r"[a-zA-Z]+")
    return bool(r.match(arg))

def sep_pair(arg: str) -> tuple[str, str]:
    if match_couple(arg):
        entry, field = arg.split('.')
        return (entry, field)
    else:
        return ('', '')

def unwrap_metadata(data: dict, metadata: dict) -> dict:
    result = {}

    for section, fields in data.items():
        result[section] = {}
        for field, text in fields.items():
            if text:
                if metadata.get(section).get(field).get("hidden"):
                    result[section][field] = '•' * len(text)
                else:
                    result[section][field] = text
        
    return result

def decode_to_str(field: list[int]) -> str:
    if field:
        decoded = [ chr(i) for i in field ]
        return ''.join(decoded)
    else:
        return ""

def decode_str_update(data: dict) -> dict:
    if data:
        decoded_data = {}

        for entry, field in data.items():
            decoded_data[entry] = {}

            if field:
                for k,v in field.items():
                    decoded_data[entry][k] = decode_to_str(v)
            else:
                decoded_data[entry] = {}

        return decoded_data
    else:
        return {}

def into_toml(data: dict) -> str:
    toml_string = ""

    for section, fields in data.items():
        for field, value in fields.items():
            if isinstance(value, dict):
                toml_string += "[%s.%s]\n" % (section, field)

                for k,v in value.items():
                    toml_string += f'{k} = "{v}"'
            else:
                toml_string += "[%s]\n" % section
                toml_string += f'{field} = "{value}"\n'
    
    return toml_string
