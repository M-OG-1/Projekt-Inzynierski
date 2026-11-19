"""
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org/>
"""
import base64
import os
import random
from sqlite3 import *
from types import NoneType

"""
    TABLES:
        USERS - [id, login, alias, pass_hash, hash_salt, perms, creation_time] 
            perms:
                0 - unverified user
                1 - verified user
                2 - administrator
        TOKENS - [id, user_id, value, expiration_time] # value nie może być jako base64 bo where wtedy nie działa
        
        TODO:
            - listy ukończonych modułów i zadań
            - zgody RODO
"""

class DatabaseAccess:
    def __init__(self, path: str):
        self.connection = connect(path, check_same_thread=False)
        self.db = self.connection.cursor()
        self._prepare_tables()

    def _commit(self):
        self.connection.commit()

    def close(self):
        self._commit()
        self.connection.close()
        del self

    def _prepare_tables(self):
        self.db.execute("SELECT COUNT(name) FROM sqlite_master WHERE type='table' AND name='Users'")
        if self.db.fetchone()[0] != 1:
            self.db.execute("CREATE TABLE Users(id INTEGER PRIMARY KEY, login TEXT NOT NULL UNIQUE, alias TEXT NOT NULL, pass_hash BLOB NOT NULL, hash_salt BLOB NOT NULL, perms INT, creation_time INT DEFAULT (unixepoch()))")
            self.first_init = True
        else:
            self.first_init = False

        self.db.execute("SELECT COUNT(name) FROM sqlite_master WHERE type='table' AND name='Tokens'")
        if self.db.fetchone()[0] != 1:
            self.db.execute(
                "CREATE TABLE Tokens(id INTEGER PRIMARY KEY, user_id INT UNIQUE ON CONFLICT REPLACE, value TEXT NOT NULL, expiration_time INT NOT NULL, FOREIGN KEY(user_id) REFERENCES Users(id))")

        self._commit()




    def put_token_raw(self, user_id: int, token: bytes, expiration_stamp: int) -> bool:
        try:
            self.db.execute("REPLACE INTO Tokens(user_id, value, expiration_time) values(?, ?, ?)", (user_id, token, expiration_stamp,))
            self._commit()
        except Exception:
            return False
        return True

    def remove_token_raw(self, token: bytes) -> bool:
        try:
            self.db.execute("DELETE FROM Tokens WHERE value = ?", (token,))
            self._commit()
        except Exception:
            return False
        return True

    def get_user_and_expiration_raw(self, token: bytes) -> tuple[bytes, int] | tuple[None, None]:
        self.db.execute("SELECT user_id, expiration_time FROM Tokens WHERE value = ?", (token, ))
        f = self.db.fetchone()
        if f:
            return f[0], f[1]
        return None, None



    def put_token(self, user_id: int, token: bytes, expiration_stamp: int) -> bool:
        return self.put_token_raw(user_id, base64.decodebytes(token), expiration_stamp)

    def remove_token(self, token: bytes) -> bool:
        return self.remove_token_raw(base64.decodebytes(token))

    def get_user_and_expiration(self, token: bytes) -> tuple[bytes, int] | tuple[None, None]:
        return self.get_user_and_expiration_raw(base64.decodebytes(token))



    def create_user(self, login: str, pass_hash: bytes, hash_salt: bytes, perms: int, alias: str) -> bool:
        try:
            self.db.execute("INSERT INTO Users(login, pass_hash, hash_salt, perms, alias) VALUES(?, ?, ?, ?, ?)", (login, base64.encodebytes(pass_hash), base64.encodebytes(hash_salt), perms, alias,))
            self._commit()
        except IntegrityError:
            return False
        return True

    def get_password_hash_and_salt(self, login: str) -> tuple[bytes, bytes] | tuple[None, None]:
        self.db.execute("SELECT pass_hash, hash_salt FROM Users WHERE login = ?", (login, ))
        f = self.db.fetchone()
        if f:
            return base64.decodebytes(f[0]), base64.decodebytes(f[1])
        return None, None

    def get_user_id(self, login: str) -> int | NoneType:
        self.db.execute("SELECT id FROM Users WHERE login = ?", (login,))
        f = self.db.fetchone()
        if f:
            return f[0]
        return None

    def get_user_data(self, user_id: int) -> dict | NoneType:
        self.db.execute("SELECT login, alias, perms, creation_time from Users WHERE id = ?", (user_id,))
        f = self.db.fetchone()
        if f:
            return {"id": user_id, "login": f[0], "alias": f[1], "perms": f[2], "creation_time": f[3]}
        return None