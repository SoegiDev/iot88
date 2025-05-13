from datetime import datetime
from helper.function import generate_device_id,generate_token
from helper.iot_query import iot_get_by_id,iot_get_token,iot_push_notif,iot_change,iot_get_by_user
from helper.responses import bad_request,success_request
def d_identity_token(current_app,key : str):
    get_ = iot_get_token(key,['id','key'])
    if get_ is None:
        message = f"Data Not Found"
        return bad_request(message=message,code=404)
    if key is None:
        message = f"Your Request Rejected cause Forbidden {key}"
        return bad_request(message=message,code=401)
    message = f"Successfully Get Data {key}"
    get_['role'] = "device_IOT"
    token = generate_token(get_,current_app)
    return success_request(message=message,code=200,data=token)
    

def d_device_get_by_id(id : str):
    if id is not None:
        get_ = iot_get_by_id(id,None)
        message = f"Successfully Get Device {id}"
        return success_request(message=message,code=200,data=get_)
    get_ = iot_get_by_id(id,None)
    message = "Successfully Get All Device"
    print(f"Device {get_}")
    return success_request(message=message,code=200,data=get_)

def d_device_get_by_user(user: dict, deviceId: None):
    get_ = iot_get_by_user(user,deviceId,None)
    message = f"Successfully Get Device"
    if get_ is None:
        message = "Data Not Found"
        return success_request(message=message,code=404,data=get_)
    return success_request(message=message,code=200,data=get_)

def d_push_active(current_user):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    results = iot_change(current_user,date_time)
    return success_request(message="Successfully Push",code=200,data=results)

def d_push_notif(device_notif,current_user):
    push_id = generate_device_id()
    print(f"Id device {current_user}")
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    device_notif['id'] = push_id
    device_notif['device_id'] = current_user['id']
    device_notif['created_time'] = date_time
    results = iot_push_notif(device_notif)
    return success_request(message="Successfully Push",code=200,data=results)

def d_change(iotDevice : dict):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    get_ = iot_get_by_id(iotDevice['id'],None)
    if get_ is None:
        return bad_request("Not Found or Forbidden For Data Owned",403)
    updated = iot_change(iotDevice,date_time)
    return success_request(message="Successfully Changed",code=200,data=updated)