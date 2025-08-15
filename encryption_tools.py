
from cryptography.fernet import Fernet

KEY = Fernet.generate_key()
CIPHER = Fernet(KEY)

def encrypt(data):
    return CIPHER.encrypt(data.encode()).decode()

def decrypt(data):
    return CIPHER.decrypt(data.encode()).decode()
