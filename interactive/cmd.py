# interactive/cmd.py

import toml

from crypto import crypto
import Globals

def help():
    print("Available commands:")
    print("  add entry <entry>")
    print("  add field <entry.field>")
    print("  reveal entry <entry>")
    print("  reveal field <entry.field>")
    print("  reveal all")
    print("  grab <entry.field>")
    print("  save")
    print("  exit")

def reveal_all(data: dict) -> str:
    if data:
        return toml.dumps(data)
    else:
        return ""

def reveal_entry(data: dict, entry: str) -> str:
    if data and entry:
        entry = data[entry]
        return toml.dumps(entry)
    else:
        return ""

def reveal_field(data: dict, entry: str, field: str) -> str:
    return \
    grab(
        data, entry, field
    )

def add_entry(data: dict, entry: str) -> str:
    if entry:
        data[entry] = {}
        return entry
    else:
        return ""

def add_field(data: dict, entry: str, field: str, text: str) -> str:
    if entry and field and text:
        data[entry][field] = text
        return text
    else:
        return ""

def grab(data: dict, entry: str, field: str) -> str:
    if data and entry and field:
        return data[entry][field]
    else:
        return ""

def save(data: dict):
    enc_filename = Globals.GET("enc_filename")
    password = Globals.GET("password")
    crypto.encrypt_toml(data, password, enc_filename)