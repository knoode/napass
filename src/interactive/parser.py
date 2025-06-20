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
