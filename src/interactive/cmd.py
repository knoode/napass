# interactive/cmd.py

import toml

from crypto import crypto
from interactive import parser
import Globals

def help():
    print("Available commands:")
    print("  add entry <entry>")
    print("  add field <entry.field>")
    print("  add field x <entry.field>")
    print("  reveal all")
    print("  remove entry <entry>")
    print("  reveal field <entry.field>")
    print("  remove field <entry.field>")
    print("  grab <entry.field>")
    print("  save")
    print("  exit")

def reveal_all(data: dict, metadata: dict) -> str:
    if data and metadata:
        return toml.dumps(
            parser.unwrap_metadata(data, metadata)
        )
    else:
        return ""

def reveal_entry(data: dict, metadata: dict, entry: str) -> str:
    if data and metadata and entry:
        unwrap_data = parser.unwrap_metadata(data, metadata)

        return toml.dumps(
            unwrap_data.get(entry)
        )
    else:
        return ""

def reveal_field(data: dict, metadata: dict, entry: str, field: str) -> str:
    unwrap_data = parser.unwrap_metadata(data, metadata)

    return grab(
        unwrap_data, entry, field
    )

def add_entry(data: dict, metadata: dict, entry: str) -> str:
    if entry:
        data[entry] = {}
        metadata[entry] = {}
        return entry
    else:
        return ""

def add_field(data: dict, entry: str, field: str, text: str) -> str:
    if entry and field and text:
        data[entry][field] = text
        return text
    else:
        return ""

def remove_entry(data: dict, entry: str) -> str:
    if data and entry:
        del data[entry]
        return entry
    else:
        return ""

def remove_field(data: dict, entry: str, field: str) -> str:
    if data and entry and field:
        del data[entry][field]
        return field
    else:
        return ""

def grab(data: dict, entry: str, field: str) -> str:
    if data and entry and field:
        return data[entry][field]
    else:
        return ""

def save(data: dict, metadata: dict):
    enc_filename = Globals.GET("enc_filename")
    password = Globals.GET("vault_password")

    crypto.encrypt_toml(data, metadata, password, enc_filename)