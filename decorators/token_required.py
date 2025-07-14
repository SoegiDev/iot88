from functools import wraps
import jwt
from flask import request
from flask import current_app
from datetime import datetime
from helper.responses import bad_request
from helper.zAuthQuery import checkExist as authCheck
from helper.zDeviceQuery import checkExist as deviceCheck
from controller.ZAuthController import auth_profile_token

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
            if(data['role']=="device_ESL"):
                years = datetime.now().strftime('%Y')
                filenames_create = "device"+years+".json"
                postdata = {}
                postdata['id'] = data['id']
                getData = deviceCheck(postdata,filenames_create)
                get_data = getData[0] if getData is not None else None
            else:
                getUser = authCheck(data)[0] if authCheck(data) is not None else None
                get_data = auth_profile_token(getUser) if getUser is not None else None
           # print(f"from token {get_data}")
        except jwt.ExpiredSignatureError:
            #abort(bad_request("Invalid Authorize!", 401))
            return bad_request("Token is Expired!", 401)
        except jwt.InvalidTokenError:
            return bad_request("Invalid token!", 401)

        return f(get_data, *args, **kwargs)

    return decorated