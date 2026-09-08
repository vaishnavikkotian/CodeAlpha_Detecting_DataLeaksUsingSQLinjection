import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Fixed salt for demo (In production, store salt securely per user)
SALT = b'static_secure_salt_123'

def get_cipher(master_key: str) -> Fernet:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_key.encode()))
    return Fernet(key)

def encrypt_data(data: str, master_key: str) -> str:
    cipher = get_cipher(master_key)
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(token: str, master_key: str) -> str:
    cipher = get_cipher(master_key)
    return cipher.decrypt(token.encode()).decode()