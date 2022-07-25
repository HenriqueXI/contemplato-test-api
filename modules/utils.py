""" Utils """
from cryptography.fernet import Fernet


key = Fernet.generate_key()
fernet = Fernet(key)


def encripty(password):
    """ Encripty password """
    enc_password = fernet.encrypt(password.encode())

    return enc_password

def decrypt(password):
    """ decrypt password """
    dec_password = fernet.decrypt(password).decode()

    return dec_password
