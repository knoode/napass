# interactive/session.py

import pyperclip
import readline
import os
import sys

from interactive import cmd
from interactive import parser

art = """

 ▄▀▀▄ ▀▄  ▄▀▀█▄   ▄▀▀▄▀▀▀▄  ▄▀▀█▄   ▄▀▀▀▀▄  ▄▀▀▀▀▄ 
█  █ █ █ ▐ ▄▀ ▀▄ █   █   █ ▐ ▄▀ ▀▄ █ █   ▐ █ █   ▐ 
▐  █  ▀█   █▄▄▄█ ▐  █▀▀▀▀    █▄▄▄█    ▀▄      ▀▄   
  █   █   ▄▀   █    █       ▄▀   █ ▀▄   █  ▀▄   █  
▄▀   █   █   ▄▀   ▄▀       █   ▄▀   █▀▀▀    █▀▀▀   
█    ▐   ▐   ▐   █         ▐   ▐    ▐       ▐      
▐                ▐                                 

"""

def start_session(data: dict):
    # Clear the screen
    if sys.platform == "linux":
        os.system("clear")
    elif sys.platform == "windows":
        os.system("cls")
    
    print(art)
    print("Vault session started")
    print("To quit press Ctrl+D or type 'exit'")
    print()

    session_loop(data)
    
    data.clear()

    print("Exit.")

def session_loop(data: dict):
    running = True

    while running:
        try:
            command = input("napass # ")
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            print()
            continue
        
        if command:
            running = execute_command(command, data)

def execute_command(command: str, data: dict) -> bool:
    running = True

    parts = command.split()
    action = parts[0]

    if action == "help":
        cmd.help()

    elif action == "grab":
        if len(parts) == 2:
            arg = parts[1]
            entry, field = parser.sep_pair(arg)

            if entry and field:
                if entry in data.keys():
                    if field in data[entry].keys():
                        secret = cmd.grab(data, entry, field)
                        pyperclip.copy(secret)
                        print("Copied to clipboard!")
                    else:
                        print("grab: No such field '%s'" % field)
                else:
                    print("grab: No such entry '%s'" % entry)
            else:
                print("grab: Format must be 'entry.field' and only alphabetic symbols")
        else:
            print("grab: Takes 1 argument")
    
    elif action == "add":
        if len(parts) == 3:
            add_type = parts[1]

            if add_type == "entry":
                new_entry = parts[2]

                if parser.match_single(new_entry):
                    if new_entry not in data.keys():
                        cmd.add_entry(data, new_entry)
                        print("Added entry '%s'" % new_entry)
                    else:
                        print("add entry: Entry '%s' already exists" % new_entry)
                else:
                    print("add entry: Format must include only alphabetic symbols")
                    
            elif add_type == "field":
                arg = parts[2]
                entry, new_field = parser.sep_pair(arg)

                if entry and new_field:
                    if entry in data.keys():
                        if new_field not in data[entry].keys():
                            text = input("Text: ")
                            cmd.add_field(data, entry, new_field, text)
                            print("Added field '%s'" % new_field)
                        else:
                            print("add field: Field '%s' already exists" % new_field)
                    else:
                        print("add field: No such entry '%s'" % entry)
                else:
                    print("add field: Format must be 'entry.field' and only alphabetic symbols")
            else:
                print("add: Use 'add entry', or 'add field'")
        else:
            print("add: Takes 2 arguments")
    
    elif action == "save":
        if data:
            cmd.save(data)
            print("Vault saved!")
        else:
            print("save: Vault is empty")

    elif action == "reveal":
        if len(parts) >= 2:
            reveal_type = parts[1]

            if reveal_type == "all":
                toml_data = cmd.reveal_all(data)
                print(toml_data if toml_data else "()")

            elif reveal_type == "entry":
                if len(parts) == 3:
                    entry = parts[2]
                    toml_data = cmd.reveal_entry(data, entry)
                    print(toml_data if toml_data else "()")
                else:
                    print("reveal entry: Entry argument not specified")

            elif reveal_type == "field":
                if len(parts) == 3:
                    arg = parts[2]
                    entry, field = parser.sep_pair(arg)

                    if entry and field:
                        if entry in data.keys():
                            if field in data[entry].keys():
                                text = cmd.reveal_field(data, entry, field)
                                print(text if text else "()")
                            else:
                                print("reveal field: No such field '%s'" % field)
                        else:
                            print("reveal field: No such entry '%s'" % entry)
                    else:
                        print("reveal field: Format must be 'entry.field' and only alphabetic symbols")
                else:
                    print("reveal field: Takes at least 1 argument")
            
            else:
                print("reveal: Use 'reveal all' or 'reveal entry' or 'reveal field'")
        else:
            print("reveal: Takes at least 1 argument")

    elif action == "exit":
        running = False
    
    else:
        print("'%s' is not a valid command" % action)
    
    return running