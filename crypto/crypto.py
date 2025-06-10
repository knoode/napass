# crypto/crypto.py

import os
import base64
import toml
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken

def generate_key(password: str, salt: bytes) -> bytes:

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=1_200_000,
    )

    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_toml(data: dict, password: str, output_file: str):

    salt = os.urandom(16)
    key = generate_key(password, salt)
    fernet = Fernet(key)

    toml_string = toml.dumps(data)
    encrypted = fernet.encrypt(toml_string.encode())

    with open(output_file, "wb") as f:
        f.write(salt + encrypted)

def decrypt_toml(password: str, input_file: str) -> dict:

    with open(input_file, "rb") as f:
        data = f.read()
    
    salt = data[:16]
    encrypted = data[16:]

    key = generate_key(password, salt)
    fernet = Fernet(key)

    try:
        decrypted = fernet.decrypt(encrypted)
    except InvalidToken:
        return {}

    return toml.loads(decrypted.decode())