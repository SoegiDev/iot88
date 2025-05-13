from functools import wraps
import jwt
from flask import request
from flask import current_app
from helper.responses import bad_request
from helper.iot_query import iot_get_by_id
from helper.esl_query import esl_get_by_id
from helper.user_query import user_get_by_id

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
       # token = request.cookies.get('jwt_token')
        token = request.headers.get('x-access-token')
        if not token:
            # abort(bad_request("Invalid Authorize!", 401))
            return bad_request("Token is Invalid Authorize!", 401)
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            # get_data = None
            if(data['role']=="device_IOT"):            
                get_data = iot_get_by_id(data['id'],None)
                get_data['role'] = "device_IOT"
            if(data['role']=="device_ESL"):            
                get_data = esl_get_by_id(data['id'],None)
                get_data['role'] = "device_ESL"
            if(data['role']=="user"): 
                get_data = user_get_by_id(data,None)
            if(data['role']=="admin"): 
                get_data = user_get_by_id(data,None)
        except jwt.ExpiredSignatureError:
            #abort(bad_request("Invalid Authorize!", 401))
            return bad_request("Token is Expired!", 401)
        except jwt.InvalidTokenError:
            return bad_request("Invalid token!", 401)

        return f(get_data, *args, **kwargs)

    return decorated