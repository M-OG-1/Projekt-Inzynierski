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
from functools import wraps
from types import NoneType

from flask import Flask, request, redirect, session, render_template, send_file, make_response, url_for

from .config import config_instance
from .database import DatabaseAccess
from .util import check_password, new_user, generate_token, user_id_by_token_refresh, user_info, user_id_by_token, \
    clear_token

TOKEN_COOKIE_NAME = "auth_token"
TOKEN_STR_ENCODING = "ascii"

decorator_counter = 0
class AppServer(Flask):
    def __init__(self, import_name: str, root_path: str):
        super().__init__(import_name)
        self.db_path = root_path + os.sep + "data.db"
        self.db = DatabaseAccess(self.db_path)
        if self.db.first_init:
            new_user("admin", "admin", 2, self.db)

        def check_auth(perm_level):
            def _decorator(func):
                @wraps(func)
                def _wrapper():
                    if TOKEN_COOKIE_NAME in request.cookies.keys():
                        token = bytes(request.cookies[TOKEN_COOKIE_NAME].strip(), TOKEN_STR_ENCODING)
                        if config_instance["auto_refresh_tokens"]:
                            user_id = user_id_by_token_refresh(token, self.db)
                        else:
                            user_id = user_id_by_token(token, self.db)
                        if user_id:
                            if perm_level > 0:
                                info = user_info(user_id, self.db)
                                if info:
                                    if info["perms"] >= perm_level:
                                        return func(user_id, token)
                            else:
                                return func(user_id, token)
                    r = redirect(url_for("root_route"))
                    r.headers["WWW-Authenticate"] = "Bearer"
                    return r

                return _wrapper
            return _decorator

        @self.route("/")
        def root_route():
            return render_template("index.html")

        @self.route("/auth_test")
        @check_auth(0)
        def auth_test(user_id, token):
            d = user_info(user_id, self.db)
            if d:
                return render_template("auth_test_successful.html", **d), 200
            return render_template("auth_test_failed.html"), 200

        @self.route("/favicon.ico")
        def favicon():
            return send_file("favicon.ico", mimetype="image/x-icon")

        @self.route("/api/login", methods=["POST"])
        def login():
            l = request.form["login"]
            p = request.form["password"]
            s = check_password(l, p, self.db)
            if s:
                token = generate_token(l, self.db)
                if token:
                    r = redirect(url_for("home"))
                    r.set_cookie(TOKEN_COOKIE_NAME, token.decode(TOKEN_STR_ENCODING))
                    return r
            return render_template("index.html", status_message="login_fail"), 401

        @self.route("/api/logout", methods = ["GET", "POST"])
        @check_auth(0)
        def logout(user_id, token):
            clear_token(token, self.db)
            r = redirect(url_for("root_route"))
            r.set_cookie(TOKEN_COOKIE_NAME, '', expires=0)
            return r

        @self.route("/api/register", methods=["POST"])
        def register():
            l = request.form["login"]
            p = request.form["password"]
            s = False
            if "alias" in request.form.keys():
                s = new_user(l, p, 1, self.db, alias=request.form["alias"])
            else:
                s = new_user(l, p, 1, self.db)

            if s:
                return render_template("index.html", status_message = "register_success"), 201
            return render_template("index.html", status_message = "register_fail"), 200


        @self.route("/home")
        @check_auth(0)
        def home(user_id, token):
            return render_template("home.html"), 200

        @self.route("/admin")
        @check_auth(2)
        def admin_route(user_id, token):
            return render_template("admin.html"), 200

        @self.route("/api/sql")
        @check_auth(2)
        def sql(user_id, token):
            # TODO
            return render_template("admin.html"), 200
