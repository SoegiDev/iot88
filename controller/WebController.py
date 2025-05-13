from helper.function import generate_userId,generate_device_id,generate_key
from helper.responses import bad_request,success_request
from helper.esl_query import esl_register
from helper.iot_query import iot_register,iot_get_by_id,iot_change_sensor

from helper.user_query import user_get_by_username
from datetime import datetime, timezone, timedelta
expireTime = 360

#==================== ESL =======================#

def create_esl(device : dict,current_user):
    print(f" ROle {current_user['role']}")
    roles = current_user['role']
    if roles not in ("admin", "superadmin"): 
        return bad_request("Forbidden!! Only Admin ",403)
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    device_id = generate_device_id()
    device['id'] = device_id
    device['key'] = generate_key()
    device['live_date']=date_time
    device['live_end']=date_time
    device['created_date']=date_time
    device['last_updated']=date_time
    device['created_by'] = current_user['username']
    esl_process = esl_register(device)
    return success_request(message="Successfully Registered",code=201,data=esl_process)

def create_iot(device : dict,current_user):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    device_id = generate_device_id()
    device['id'] = device_id
    device['key'] = generate_key()
    device['live_date']=date_time
    device['live_end']=date_time
    device['created_date']=date_time
    device['last_updated']=date_time
    device['created_by'] = current_user['username']
    device_process = iot_register(device)
    return success_request(message="Successfully Registered",code=201,data=device_process)

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