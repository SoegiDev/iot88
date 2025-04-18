# Check Admin True or False
from helper.files import load_data,save_data
from flask import request
from helper.responses import bad_request,success_request
from helper.query import get_login_username,check_super,check_owner,check_admin
from functools import wraps
from helper.files import get_auth_file

def super_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        username = None
        current_user = None
        # ensure the jwt-token is passed with the headers
        if 'x-username' in request.headers:
            username = request.headers['x-username']
        if not username: # throw error if no token provided
            return bad_request("A valid username authorize is missing!", 401)
        try:
            if check_super(username) is False:
                return bad_request("Username Only Super Admin Access", 403)
            else:
                auths = get_auth_file()
                current_user = get_login_username(username,auths,"admin",None)
        except:
            return bad_request("Invalid Authorize!", 401)
         # Return the user information attached to the token
        kwargs['current_user'] = current_user
        return f(*args, **kwargs)
    return decorator

def admin_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        username = None
        current_user = None
        # ensure the jwt-token is passed with the headers
        if 'x-username' in request.headers:
            username = request.headers['x-username']
        if not username: # throw error if no token provided
            return bad_request("A valid username authorize is missing!", 401)
        try:
            if check_admin(username) is False:
                return bad_request("Username Only Admin Access", 403)
            else:
                auths = get_auth_file()
                current_user = get_login_username(username,auths,"admin",None)
        except:
            return bad_request("Invalid Authorize!", 401)
         # Return the user information attached to the token
        kwargs['current_user'] = current_user
        return f(*args, **kwargs)
    return decorator


def owner_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        username = None
        current_user = None
        # ensure the jwt-token is passed with the headers
        if 'x-username' in request.headers:
            username = request.headers['x-username']
        if not username: # throw error if no token provided
            return bad_request("A valid username authorize is missing!", 401)
        try:
            if check_owner(username) is False:
                return bad_request("Username Only User Access", 403)
            else:
                auths = get_auth_file()
                current_user = get_login_username(username,auths,"user",None)
        except:
            return bad_request("Invalid Authorize!", 401)
         # Return the user information attached to the token
        kwargs['current_user'] = current_user
        return f(*args, **kwargs)
    return decorator