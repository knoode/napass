# crypto/crypto.py

import os
import base64
import toml
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from typing import Tuple

from interactive import parser

def generate_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=1_200_000,
    )

    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_toml(data: dict, metadata: dict, password: str, output_file: str):

    salt = os.urandom(16)
    key = generate_key(password, salt)
    fernet = Fernet(key)

    data_toml = toml.dumps(data)
    metadata_toml = toml.dumps(metadata)

    data_enc = base64.urlsafe_b64encode(fernet.encrypt(data_toml.encode()))
    metadata_enc = base64.urlsafe_b64encode(fernet.encrypt(metadata_toml.encode()))
    encrypted = data_enc + b'\x00' + metadata_enc

    with open(output_file, "wb") as f:
        f.write(salt + encrypted)
    

def decrypt_toml(password: str, input_file: str) -> Tuple[dict, dict]:
    with open(input_file, "rb") as f:
        text = f.read()
    
    salt = text[:16]
    encrypted = text[16:]

    key = generate_key(password, salt)
    fernet = Fernet(key)

    enc_parts = encrypted.split(b'\x00')

    try:
        if len(enc_parts) == 2:
            data_toml = fernet.decrypt(base64.urlsafe_b64decode(enc_parts[0])).decode()
            metadata_toml = fernet.decrypt(base64.urlsafe_b64decode(enc_parts[1])).decode()

            data, metadata = toml.loads(data_toml), toml.loads(metadata_toml)
            # print(data, metadata)
            # os.system("read")

            return (data, metadata)
        else:
            return {}, {}

    except InvalidToken:
        return {}, {}