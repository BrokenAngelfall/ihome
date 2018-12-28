import random
from functools import wraps

from flask import session, render_template, redirect


def random_str():
    str1 = ''
    str2 = 'wdasjinmfdcsasokMl12983rfekwndscm,'
    for i in range(4):
        str1 += random.choice(str2)
    return str1


def login_check(func):
    @wraps(func)
    def login_(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:
            return redirect('/user/login/')
    return login_