from functools import wraps
import jwt
from flask import request,abort
from flask import current_app
from helper.responses import bad_request,success_request
from helper.files import get_auth_file
from helper.query import get_login_username

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
       # token = request.cookies.get('jwt_token')
        token = request.headers.get('x-access-token')
        if not token:
            # abort(bad_request("Invalid Authorize!", 401))
            return bad_request("Token is Invalid Authorize!", 401)
        try:
            auths = get_auth_file()
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            get_data = get_login_username(data['username'],auths,data['role'],
                                          ["username","email","id","role","password","last_updated"])
        except jwt.ExpiredSignatureError:
            #abort(bad_request("Invalid Authorize!", 401))
            return bad_request("Token is Expired!", 401)
        except jwt.InvalidTokenError:
            return bad_request("Invalid token!", 401)

        return f(get_data, *args, **kwargs)

    return decorated