# Globals.py

Globals = {
    "enc_filename": "",
    "vault_password": "",
}

def GET(g: str) -> str:
    if g in Globals.keys():
        return Globals[g]
    else:
        return ""

def SET(g: str, v: str):
    if g in Globals.keys():
        Globals[g] = v