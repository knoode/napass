# interactive/parser.py

import re

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

