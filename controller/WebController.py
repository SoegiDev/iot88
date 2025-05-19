from helper.function import generate_userId,generate_device_id,generate_key
from helper.responses import bad_request,success_request
from helper.esl_query import esl_register,esl_get_by_id,esl_get_by_user,esl_change
from helper.iot_query import iot_register,iot_get_by_id,iot_change_sensor
from helper.product_query import product_get_by_id,product_change

from helper.user_query import user_get_by_username
from datetime import datetime
expireTime = 720

#==================== ESL =======================#

def get_profile(current_user):
    check = user_get_by_username(current_user,None)
    if check:
        return success_request("Successfully Get Profile",200,check)
    else:
        return bad_request("User is not found",400)

def push_change_sensor(device : dict,sensor : dict):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    get_ = iot_get_by_id(device['id'],None)
    if get_ is None:
        return bad_request("Not Found or Forbidden For Data Owned",403)
    updated = iot_change_sensor(device,sensor,date_time)
    return success_request(message="Successfully Changed",code=200,data=updated)


def web_product_byid(id : str):
    if id is not None:
        get_ = product_get_by_id(id,None)
        message = f"Successfully Get PRODUCT {id}"
        return success_request(message=message,code=200,data=get_)
    get_ = product_get_by_id(None,None)
    message = "Successfully Get All PRODUCT"
    return success_request(message=message,code=200,data=get_)

def web_product_update(esl : dict):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    get_ = product_get_by_id(esl['id'],None)
    if get_ is None:
        return bad_request("Not Found or Forbidden For Data Owned",403)
    updated = product_change(esl,date_time)
    return success_request(message="Successfully Changed",code=200,data=updated)

def web_esl_byid(id : str):
    if id is not None:
        get_ = esl_get_by_id(id,None)
        message = f"Successfully Get Device {id}"
        return success_request(message=message,code=200,data=get_)
    get_ = esl_get_by_id(None,None)
    message = "Successfully Get All Device"
    return success_request(message=message,code=200,data=get_)

def web_get_byUser(user: dict, deviceId: None):
    get_ = esl_get_by_user(user,deviceId,None)
    message = f"Successfully Get Device"
    if get_ is None:
        message = "Data Not Found"
        return success_request(message=message,code=404,data=get_)
    return success_request(message=message,code=200,data=get_)

def web_esl_update(esl : dict):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    get_ = esl_get_by_id(esl['id'],None)
    if get_ is None:
        return bad_request("Not Found or Forbidden For Data Owned",403)
    updated = esl_change(esl,date_time)
    return success_request(message="Successfully Changed",code=200,data=updated)