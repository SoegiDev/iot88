from functools import wraps
from flask import g, request, redirect, url_for

def tes_log(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        results_function = f(*args,**kwargs)
        print(f"TEST LOG {results_function}")
        return f(*args, **kwargs)
    return decorated_function