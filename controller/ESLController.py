from datetime import datetime
from helper.function import generate_device_id,generate_token
from helper.esl_query import esl_get_token,esl_get_by_id,esl_change,esl_push_notif,esl_get_by_user
from helper.responses import bad_request,success_request
def e_identity_token(current_app,key : str):
    get_ = esl_get_token(key,['id','key'])
    if get_ is None:
        message = f"Data Not Found"
        return bad_request(message=message,code=404)
    if key is None:
        message = f"Your Request Rejected cause Forbidden {key}"
        return bad_request(message=message,code=401)
    get_['role'] = "device_ESL"
    message = f"Successfully Get Data {key}"
    token = generate_token(get_,current_app)
    return success_request(message=message,code=200,data=token)
    

def e_device_get(id : str):
    if id is not None:
        get_ = esl_get_by_id(id,None)
        message = f"Successfully Get Device {id}"
        return success_request(message=message,code=200,data=get_)
    get_ = esl_get(id,None)
    message = "Successfully Get All Device"
    return success_request(message=message,code=200,data=get_)

def e_device_getByUser(user: dict, deviceId: None):
    get_ = esl_get_by_user(user,deviceId,None)
    message = f"Successfully Get Device"
    if get_ is None:
        message = "Data Not Found"
        return success_request(message=message,code=404,data=get_)
    return success_request(message=message,code=200,data=get_)

def e_push_active(current_user):
    print(f"Push Active {current_user}")
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    results = esl_change(current_user,date_time)
    return success_request(message="Successfully Push",code=200,data=results)

def e_push_notif(device_notif,current_user):
    push_id = generate_device_id()
    print(f"Id device {current_user}")
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    device_notif['id'] = push_id
    device_notif['device_id'] = current_user['id']
    device_notif['created_time'] = date_time
    results = esl_push_notif(device_notif)
    return success_request(message="Successfully Push",code=200,data=results)

def e_change(esl : dict):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    get_ = esl_get_by_id(esl['id'],None)
    if get_ is None:
        return bad_request("Not Found or Forbidden For Data Owned",403)
    updated = esl_change(esl,date_time)
    return success_request(message="Successfully Changed",code=200,data=updated)