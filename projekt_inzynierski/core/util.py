import base64
import datetime
import hashlib
import hmac
import os
import time
from types import NoneType

from projekt_inzynierski.core.config import config_instance
from projekt_inzynierski.core.database import DatabaseAccess

def hash_password(password: bytes, hash_salt: bytes) -> bytes:
    return hashlib.scrypt(password, salt=hash_salt, n=2**17, r=8, p=1, dklen=32, maxmem=256 * 1024 * 1024)

def check_password(login: str, password: str, db: DatabaseAccess) -> bool:
    k, salt = db.get_password_hash_and_salt(login)
    if not k or not salt:
        return False
    h = hash_password(bytes(password, 'utf-16'), salt)
    return hmac.compare_digest(k, h)

def new_user(login: str, password: str, perms: int, db: DatabaseAccess, alias=None) -> bool:
    salt = os.urandom(16)
    k = hash_password(bytes(password, 'utf-16'), salt)
    if k:
        return db.create_user(login, k, salt, perms, alias if alias else login)
    return False

def generate_token(login: str, db: DatabaseAccess) -> bytes | NoneType:
    user_id = db.get_user_id(login)
    if not user_id:
        return None
    token = os.urandom(32)
    stamp = int(time.time()) + config_instance["token_duration"]

    if db.put_token_raw(user_id, token, stamp):
        return base64.encodebytes(token)
    return None

def user_id_by_token(token: bytes, db: DatabaseAccess) -> int | NoneType:
    user_id, expiration = db.get_user_and_expiration(token)
    if not user_id or not expiration or expiration <= int(time.time()):
        return None
    return user_id

def user_id_by_token_refresh(token: bytes, db: DatabaseAccess) -> int | NoneType:
    user_id, expiration = db.get_user_and_expiration(token)
    if not user_id or not expiration or expiration <= int(time.time()):
        return None
    db.put_token(user_id, token, int(time.time()) + config_instance["token_duration"])
    return user_id

def user_info(user_id: int, db: DatabaseAccess) -> dict | NoneType:
    data = db.get_user_data(user_id)
    return data

def clear_token(token: bytes, db: DatabaseAccess):
    db.remove_token(token)

