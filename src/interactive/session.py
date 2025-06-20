# interactive/session.py

from getpass import getpass
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

def start_session(data: dict, metadata: dict):
    # Clear the screen
    if sys.platform == "linux":
        os.system("clear")
    elif sys.platform == "windows":
        os.system("cls")
    
    print(art)
    print("Vault session started")
    print("To quit press Ctrl+D or type 'exit'")
    print()

    # print(data)
    # os.system("read")
    session_loop(data, metadata)

    data.clear()

    print("Exit.")

def session_loop(data: dict, metadata: dict):
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
            running = execute_command(command, data, metadata)

def execute_command(command: str, data: dict, metadata: dict) -> bool:
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
                        print("grab: No such field '%s.%s'" % (entry, field))
                else:
                    print("grab: No such entry '%s'" % entry)
            else:
                print("grab: Format must be 'entry.field' and only alphabetic symbols")
        else:
            print("grab: Takes 1 argument")
    
    elif action == "add":
        if len(parts) in (3, 4):
            add_type = parts[1]

            if add_type == "entry":
                new_entry = parts[2]

                if parser.match_single(new_entry):
                    if new_entry not in data.keys():
                        cmd.add_entry(data, metadata, new_entry)
                        print("Added entry '%s'" % new_entry)
                    else:
                        print("add entry: Entry '%s' already exists" % new_entry)
                else:
                    print("add entry: Format must include only alphabetic symbols")
                    
            elif add_type == "field":
                if len(parts) == 4:
                    hidden = parts[2] == "x"
                    couple = parts[3]
                else:
                    hidden = False
                    couple = parts[2]
                
                entry, new_field = parser.sep_pair(couple)

                if entry and new_field:
                    if entry in data.keys():
                        if new_field not in data[entry].keys():
                            if hidden:
                                text = parser.safe_input("Text: ", hidden=True)
                            else:
                                text = parser.safe_input("Text: ")

                            cmd.add_field(data, metadata, entry, new_field, text, hidden)

                            print("Added field '%s.%s'" % (entry, new_field))
                        else:
                            print("add field: Field '%s.%s' already exists" % (entry, new_field))
                    else:
                        print("add field: No such entry '%s'" % entry)
                else:
                    print("add field: Format must be 'entry.field' and only alphabetic symbols")
            else:
                print("add: Use 'add entry', or 'add field'")
        else:
            print("add: Takes at least 2 arguments")
    
    elif action == "remove":
        if len(parts) == 3:
            remove_type = parts[1]

            if remove_type == "entry":
                entry = parts[2]

                if parser.match_single(entry):
                    if entry in data.keys():
                        cmd.remove_entry(data, entry)
                        print("Entry '%s' removed!" % entry)
                    else:
                        print("remove entry: No such entry '%s'" % entry)
                else:
                    print("remove entry: Format must include only alphabetic symbols")
            
            elif remove_type == "field":
                entry, field = parser.sep_pair(parts[2])

                if entry and field:
                    if entry in data.keys():
                        if field in data[entry].keys():
                            cmd.remove_field(data, entry, field)
                            print("Field '%s.%s' removed!" % (entry, field))
                        else:
                            print("remove field: No such field '%s.%s'" % (entry, field))
                    else:
                        print("remove field: No such entry '%s'" % entry)
                else:
                    print("remove field: Format must be 'entry.field' and only alphabetic symbols")
        else:
            print("remove: Takes at least 2 arguments")
    
    elif action == "save":
        if data:
            cmd.save(data, metadata)
            print("Vault saved!")
        else:
            print("save: Vault is empty")

    elif action == "reveal":
        if len(parts) in (2, 3):
            reveal_type = parts[1]

            if reveal_type == "all":
                toml_data = cmd.reveal_all(data, metadata)
                print(toml_data if toml_data else "()")

            elif reveal_type == "entry":
                if len(parts) == 3:
                    entry = parts[2]
                    if entry in data.keys():
                        toml_data = cmd.reveal_entry(data, metadata, entry)
                        print(toml_data if toml_data else "()")
                    else:
                        print("reveal entry: No such entry '%s'" % entry)
                else:
                    print("reveal entry: Entry argument not specified")

            elif reveal_type == "field":
                if len(parts) == 3:
                    arg = parts[2]
                    entry, field = parser.sep_pair(arg)

                    if entry and field:
                        if entry in data.keys():
                            if field in data[entry].keys():
                                text = cmd.reveal_field(data, metadata, entry, field)
                                print(text)
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