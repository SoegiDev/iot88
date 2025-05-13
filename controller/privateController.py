
from helper.crypto_password import verify_password,open_key,e_password
from helper.responses import bad_request,success_request
from helper.user_query import user_get_by_username,user_get_password
from helper.crypto_password import verify_password
from helper.function import generate_token
from flask import request,current_app

def c_login(user: dict):
    check = user_get_by_username(user,["username","email","id","role","password"])
    if check:
        key_secret = open_key()
        password_active = user_get_password(check,True)
        if password_active == None:
            return bad_request("Your password is inactive",400)
        verify = verify_password(key_secret,user['password'],password_active['password'])
        if verify == False:
            return bad_request("Your password is incorrect",400)
        token = generate_token(check,current_app)
        return success_request("Successfully Login",200,token)
    else:
        return bad_request("User is not found",400)