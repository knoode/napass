#!/usr/bin/env python3

import time
import sys
from argparse import ArgumentParser
from getpass import getpass

import Globals
from crypto import crypto
from interactive import session

def main():
    parser = ArgumentParser(
        prog="napass",
    )
    
    subparser = parser.add_subparsers(dest="command", required=True)
    init_parser = subparser.add_parser("init", help="Initialize a new vault")
    login_parser = subparser.add_parser("login", help="Log in into vault")
    login_parser.add_argument("file", help="Path to encrypted TOML file")

    # TODO: Add -d flag

    args = parser.parse_args()

    match args.command:
        case "init":
            try:
                vault_name = input("(?) Vault name: ").strip()
                vault_pwd = getpass("(?) Password: ").strip()

            except (KeyboardInterrupt, EOFError):
                print()
                safe_sleep(0.89)
                sys.exit(0)

            enc_filename = vault_name + ".enc"

            Globals.SET("enc_filename", enc_filename)
            Globals.SET("password", vault_pwd)

            print("(*) Creating a new vault '%s'" % vault_name)
            time.sleep(2.5)
            
            data = {}
            session.start_session(data)

        case "login":
            enc_file = args.file
            Globals.SET("enc_filename", enc_file)
            
            # TODO: Add name for vaults, stored in prefix to key
            try:
                password = getpass("(?) Password: ")
            except (EOFError, KeyboardInterrupt):
                sys.exit(0)

            print("(*) Decrypting in progress...")
            time.sleep(2.5)

            data = crypto.decrypt_toml(password, enc_file)

            if not data:
                print("(^!^) Wrong vault password")
                sys.exit(1)
            else:
                Globals.SET("password", password)
                session.start_session(data)

        case _:
            pass

def safe_sleep(seconds: int):
    try:
        time.sleep(seconds)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()