# crypto/crypto.py

import os
import base64
import toml
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from typing import Tuple

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

    data_dump = toml.dumps(data)
    metadata_dump = toml.dumps(metadata)

    encrypted = fernet.encrypt(
        data_dump.encode() + b"\x00" + metadata_dump.encode()
    )

    with open(output_file, "wb") as f:
        f.write(salt + encrypted)

def decrypt_toml(password: str, input_file: str) -> Tuple[dict, dict]:
    with open(input_file, "rb") as f:
        text = f.read()
    
    salt = text[:16]
    encrypted = text[16:]

    key = generate_key(password, salt)
    fernet = Fernet(key)

    try:
        decrypted = fernet.decrypt(encrypted).split(b"\x00")

        if len(decrypted) == 2:
            data = toml.loads(decrypted[0].decode())
            metadata = toml.loads(decrypted[1].decode())

            return (data, metadata)
        else:
            return {}, {}

    except InvalidToken:
        return {}, {}
