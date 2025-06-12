#!/usr/bin/env python3

import time
import sys
from argparse import ArgumentParser

import Globals
from crypto import crypto
from interactive import session
from interactive import parser

def main():
    argparser = ArgumentParser(
        prog="napass",
    )
    
    subparser = argparser.add_subparsers(dest="command", required=True)
    subparser.add_parser("init", help="Initialize a new vault")
    login_parser = subparser.add_parser("login", help="Log in into vault")
    login_parser.add_argument("file", help="Path to encrypted TOML file")

    args = argparser.parse_args()

    match args.command:
        case "init":
            vault_name = parser.safe_input("[1] Vault name: ")

            if not vault_name:
                print("(!) You must enter vault name", file=sys.stderr)
                parser.safe_sleep(.89)
                sys.exit(1)

            vault_pwd = parser.safe_input("[2] Password: ", hidden=True)
                
            if not vault_pwd:
                print("(!) You must enter vault password", file=sys.stderr)
                parser.safe_sleep(.89)
                sys.exit(1)
            
            enc_filename = vault_name + ".enc"

            Globals.SET("enc_filename", enc_filename)
            Globals.SET("vault_password", vault_pwd)

            print("(*) Creating a new vault '%s'" % vault_name)
            time.sleep(2.5)
            
            data, metadata = {}, {}
            session.start_session(data, metadata)

        case "login":
            enc_file = args.file
            Globals.SET("enc_filename", enc_file)
            
            # TODO: Add name for vaults, stored in prefix to key
            vault_pwd = parser.safe_input("Password: ", hidden=True)

            if vault_pwd:
                print("(*) Decrypting...")
                parser.safe_sleep(.89)

                data, metadata = crypto.decrypt_toml(vault_pwd, enc_file)

                if not data and not metadata:
                    print("(^!^) Wrong vault password")
                    sys.exit(1)
                else:
                    Globals.SET("vault_password", vault_pwd)
                    session.start_session(data, metadata)

        case _:
            pass



if __name__ == "__main__":
    main()