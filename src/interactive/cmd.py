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
        decoded_data = parser.decode_str_update(data)
        return toml.dumps(
            parser.unwrap_metadata(decoded_data, metadata)
        )
    else:
        return ""

def reveal_entry(data: dict, metadata: dict, entry: str) -> str:
    if data and metadata and entry:
        decoded_data = parser.decode_str_update(data)
        unwrap_data = parser.unwrap_metadata(decoded_data, metadata)

        return toml.dumps(
            unwrap_data.get(entry)
        )
    else:
        return ""

def reveal_field(data: dict, metadata: dict, entry: str, field: str) -> str:
    if data and metadata and entry and field:
        decoded_data = parser.decode_str_update(data)
        return parser.unwrap_metadata(decoded_data, metadata).get(entry).get(field)
    else:
        return ""

def add_entry(data: dict, metadata: dict, entry: str) -> str:
    if entry:
        data[entry] = {}
        metadata[entry] = {}
        return entry
    else:
        return ""

def add_field(data: dict, metadata: dict, entry: str, field: str, text: str, hidden: bool = False) -> str:
    if entry and field and text:
        data[entry][field] = text.encode()
        metadata[entry][field] = { "hidden": hidden }
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

def grab(data: dict, entry: list[int], field: str) -> str:
    if data and entry and field:
        return parser.decode_to_str(data.get(entry).get(field))
    else:
        return ""

def save(data: dict, metadata: dict):
    enc_filename = Globals.GET("enc_filename")
    password = Globals.GET("vault_password")

    crypto.encrypt_toml(data, metadata, password, enc_filename)