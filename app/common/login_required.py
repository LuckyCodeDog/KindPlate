from functools import wraps
from flask import redirect, url_for, session


def redirect_to_login():
    return redirect(url_for("login"))


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("is_authenticated") :
            return func(*args, **kwargs)
        return redirect_to_login()
    return wrapper


def admin_login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("role") == "admin":
            return func(*args, **kwargs)
        return redirect_to_login()
    return wrapper


def trainer_login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("role") == "trainer":
            return func(*args, **kwargs)
        return redirect_to_login()
    return wrapper


def member_login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("role") == "member":
            return func(*args, **kwargs)
        return redirect_to_login()
    return wrapper
