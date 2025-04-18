from cryptography.fernet import Fernet
import os
from cryptography.hazmat.primitives import hashes

def generate_key():
    key = Fernet.generate_key()
    key_pass = key.decode("utf-8")
    return key_pass

def create_key():
    key = Fernet.generate_key()
    key_pass = key.decode("utf-8")
    f = open("resources/key2.txt", "w")
    f.write(key_pass)
    f.close()
    return key_pass

def open_key():
    f = open("resources/key.txt", "r")
    key_pass = f.read()
    return key_pass

def encrypt_password(key: str, sentences : str):
    secret_key = str.encode(key)
    b_sentences = str.encode(sentences)
    cipher_suite = Fernet(secret_key)
    cipher_text = cipher_suite.encrypt(b_sentences)
    return cipher_text

def decrypt_password(key: str, encrypt : str):
    try:    
        secret_key = str.encode(key)
        cipher_suited = Fernet(secret_key)
        plain_text = cipher_suited.decrypt(encrypt)
        return plain_text.decode()
    except Exception as error:
            print('eRROR: ' + repr(error))
            errors = f"Error {repr(error)}"
            return errors
        
def verify_password(key: str, sentences : str, encrypt_password):
    try:
        b_encrypt = str.encode(encrypt_password)
        chipper_text = decrypt_password(key,b_encrypt)
        if chipper_text == sentences:
            return True
        else:
            return False
    except Exception as error:
            print('eRROR: ' + repr(error))
            errors = f"Error {repr(error)}"
            return errors
        
def e_password(password : str):
    key_secret = open_key()
    e_pass = encrypt_password(key_secret,password)
    password_encryption = e_pass.decode("utf-8")
    return password_encryption