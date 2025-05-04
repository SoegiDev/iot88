from helper.function import generate_userId,generate_device_id,generate_key
from datetime import datetime
from decorators import add_log,admin_required,super_required
from helper.crypto_password import verify_password,open_key,e_password
from helper.responses import bad_request,success_request
from helper.query import register_device_by_admin,check_username,get_login_username, \
    get_password,check_email,change_password,get_device,change_device_by_admin, \
        get_device_admin,change_device_sensor_by_admin,register_device_sensor_by_admin, \
            register_push_notif,register_esl_by_admin,get_esl,change_esl_by_admin, \
                get_notif_device
from helper.files import load_data,save_data,get_auth_file,get_device_file,get_device_notif , \
    get_esl_file
import jwt
from flask import request,current_app
from datetime import datetime, timezone, timedelta
expireTime = 360
@super_required
def c_register_admin(user: dict,current_user):
    auths = get_auth_file()
    user_id = generate_userId()
    username = user['username']
    password = user['password']
    email = user['email']
    role = user['role']
    c_username = check_username(username,auths)
    if c_username:
        return bad_request("User Already Exists",400)
    c_email = check_email(email,auths)
    if c_email:
        return bad_request("Email Already Exists",400)
    email_list = []
    email_list.append({"email":email,"primary":True})
    password_list = []
    password_list.append({"password":e_password(password),"primary":True})
    device_list = []
    auths["authentication"].append({"id": user_id,"username": username,"email":email,"role":role,"password":password_list,"device":device_list})
    save_data("resources/auth.json",auths)
    return success_request(message="Successfully Registered",code=201,data=None)


def c_login_admin(user: dict):
    auths = get_auth_file()
    username = user['username']
    password = user['password']
    check = check_username(username,auths)
    if check:
        get_data = get_login_username(username,auths,"admin",["username","email","id","role","password"])
        if get_data is None:
            return bad_request("Forbidden",403)
        key_secret = open_key()
        password_active = get_password(get_data,True)
        if password_active == None:
            return bad_request("Your password is inactive",400)
        verify = verify_password(key_secret,password,password_active['password'])
        if verify == False:
            return bad_request("Your password is incorrect",400)
        token = jwt.encode({
            'username': username,'role': get_data['role'],
            'exp': datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(minutes=expireTime),
            'expDate': str(datetime.now() + timedelta(minutes=expireTime))
            
        }, current_app.config['SECRET_KEY'], algorithm='HS256')
        get_data['token'] = token
        return success_request("Successfully Login",200,get_data)
    else:
        return bad_request("User is not found",400)
    
@admin_required
def c_change_password_admin(user : dict,current_user):
    auths = get_auth_file()
    username = user['username']
    password = user['password']
    email = user['email']
    c_username = check_username(username,auths)
    if c_username == False:
        return bad_request("User is not found",400)
    c_email = check_email(email,auths)
    if c_email == False:
        return bad_request("Email is not found",400)
    e_pass = e_password(password)
    change_password(username,e_pass,auths)
    get_data = get_login_username(username,auths,"admin",["username","email","id","role","password"])
    if get_data is None:
        return bad_request("Forbidden",403)
    return success_request("Change Password Succesfully",200,get_data)

@admin_required
def c_register_device_admin(device : dict,current_user):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    device_id = generate_device_id()
    device['id'] = device_id
    device['key'] = generate_key()
    device['live_date']=date_time
    device['live_end']=date_time
    device['created_date']=date_time
    device['last_updated']=date_time
    device['created_by'] = current_user['username']
    device_process = register_device_by_admin(device)
    return success_request(message="Successfully Registered",code=201,data=device_process)

@admin_required
def c_change_device_admin(device : dict,current_user):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    devices = get_device_file()
    get_ = get_device(device['id'],devices,current_user,None)
    if get_ is None:
        return bad_request("Not Found or Forbidden For Data Owned",403)
    updated = change_device_by_admin(device,date_time,devices)
    return success_request(message="Successfully Changed",code=200,data=updated)

@admin_required
def c_register_device_sensor_admin(device : dict,sensor : dict,current_user):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    devices = get_device_file()
    get_ = get_device(device['id'],devices,current_user,None)
    if get_ is None:
        return bad_request("Not Found or Forbidden For Data Owned",403)
    updated = register_device_sensor_by_admin(device,sensor,date_time,devices)
    return success_request(message="Successfully Changed",code=200,data=updated)

@admin_required
def c_change_device_sensor_admin(device : dict,sensor : dict,current_user):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    devices = get_device_file()
    get_ = get_device(device['id'],devices,current_user,None)
    if get_ is None:
        return bad_request("Not Found or Forbidden For Data Owned",403)
    updated = change_device_sensor_by_admin(device,sensor,date_time,devices)
    return success_request(message="Successfully Changed",code=200,data=updated)

    
@admin_required
def c_get_device_admin(id : str,current_user):
    devices = get_device_file()
    get_ = get_device_admin(id,devices,current_user,None)
    message = "Successfully Get All Device"
    if id is not None:
        message = f"Successfully Get Device {id}"
    return success_request(message=message,code=200,data=get_)

@admin_required
def c_get_esl_admin(id : str,current_user):
    devices = get_esl_file()
    get_ = get_esl(id,devices,current_user,None)
    message = "Successfully Get All ESL"
    if id is not None:
        message = f"Successfully Get ESL {id}"
    return success_request(message=message,code=200,data=get_)

def c_profile_admin(current_user):
    auths = get_auth_file()
    username = current_user['username']
    check = check_username(username,auths)
    if check:
        get_data = get_login_username(username,auths,"admin",["username","email","id","role","password"])
        return success_request("Successfully Get Profile",200,get_data)
    else:
        return bad_request("User is not found",400)
    
def c_push_notif_sensor(sensor : dict):
    device_notif = get_device_notif()
    push_id = generate_device_id()
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sensor['device_id'] = sensor['id']
    sensor['id'] = push_id
    sensor['created_time'] = date_time
    updated = register_push_notif(device_notif,sensor)
    return success_request(message="Successfully Push",code=200,data=updated)

def c_register_esl_admin(device : dict,current_user):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    device_id = generate_device_id()
    device['id'] = device_id
    device['key'] = generate_key()
    device['live_date']=date_time
    device['live_end']=date_time
    device['created_date']=date_time
    device['last_updated']=date_time
    device['created_by'] = current_user['username']
    esl_process = register_esl_by_admin(device)
    return success_request(message="Successfully Registered",code=201,data=esl_process)

@admin_required
def c_change_esl_admin(device : dict,current_user):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    devices = get_esl_file()
    get_ = get_esl(device['id'],devices,current_user,None)
    if get_ is None:
        return bad_request("Not Found or Forbidden For Data Owned",403)
    updated = change_esl_by_admin(device,date_time,devices)
    return success_request(message="Successfully Changed",code=200,data=updated)

def c_get_notif_admin(id : str,current_user):
    notif = get_device_notif()
    get_ = get_notif_device(id,notif,current_user,None)
    message = "Successfully Get All Notif"
    if id is not None:
        message = f"Successfully Get Notif {id}"
    return success_request(message=message,code=200,data=get_)