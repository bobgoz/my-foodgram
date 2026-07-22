from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def hash_password(password: str):
    """ Хеширование пароля """
    return password_hash.hash(password)