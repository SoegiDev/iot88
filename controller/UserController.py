from helper.function import generate_userId,generate_device_id
from datetime import datetime
from decorators import owner_required
from helper.crypto_password import verify_password,open_key,e_password
from helper.responses import bad_request,success_request
from helper.query import check_username,get_login_username,get_password,check_email,change_password,get_device,change_device_by_user,register_device_by_user,change_user,change_device_sensor_by_user
from helper.files import load_data,save_data,get_auth_file,get_device_file
now = datetime.now() # current date and time

def c_register(user: dict):
    date_time = now.strftime("%m-%d-%Y %H:%M:%S")
    auths = get_auth_file()
    user_id = generate_userId()
    username = user['username']
    password = user['password']
    email = user['email']
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
    auths["authentication"].append({"id": user_id,"username": username,"email":email,"role":"user","loggedIn":False,"last_updated":datetime,"password":password_list,"device":device_list})
    save_data("resources/auth.json",auths)
    return success_request(message="Successfully Registered",code=201,data=None)


def c_login(user: dict):
    date_time = now.strftime("%m-%d-%Y %H:%M:%S")
    auths = get_auth_file()
    username = user['username']
    password = user['password']
    check = check_username(username,auths)
    if check:
        get_data = get_login_username(username,auths,"user",["username","email","id","role","password","device","get_data","last_updated"])
        if get_data is None:
            return bad_request("Forbidden",403)
        key_secret = open_key()
        # verify = verify_password(key_secret,password,get_data[''])
        password_active = get_password(get_data,True)
        if password_active == None:
            return bad_request("Your password is inactive",400)
        verify = verify_password(key_secret,password,password_active['password'])
        if verify == False:
            return bad_request("Your password is incorrect",400)
        get_data['loggedIn'] = True
        change_user(get_data,date_time,None,auths)
        get_data = get_login_username(username,auths,"user",["username","email","id","role","password","device","get_data","last_updated"])
        if get_data is None:
            return bad_request("Forbidden",403)
        return success_request("Successfully Login",200,get_data)
    else:
        return bad_request("User is not found",400)
    
@owner_required
def c_change_password(user : dict,current_user):
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
    get_data = get_login_username(username,auths,"user",["username","email","id","role","password"])
    if get_data is None:
        return bad_request("Forbidden",403)
    return success_request("Change Password Succesfully",200,get_data)

@owner_required
def c_register_device(device : dict,current_user):
    auths = get_auth_file()
    devices = get_device_file()
    date_time = now.strftime("%m-%d-%Y %H:%M:%S")
    get_ = get_device(device['device_id'],devices,current_user,None)
    if get_ is None:
        return bad_request("Not Found or Forbidden For Data Owned",403)
    register_device_by_user(auths,device,get_,date_time,current_user)
    get_ = get_device(device['device_id'],devices,current_user,None)
    change_device_by_user(current_user,get_,date_time,devices)
    get_data = get_login_username(current_user['username'],auths,"user",["username","email","id","role","password","device"])
    if get_data is None:
        return bad_request("Forbidden",403)
    return success_request(message="Successfully Registered",code=200,data=get_data)
    
@owner_required
def c_change_device(device : dict,current_user):
    date_time = now.strftime("%m-%d-%Y %H:%M:%S")
    devices = get_device_file()
    get_ = get_device(device['id'],devices,current_user,None)
    if get_ is None:
        return bad_request("Not Found or Forbidden For Data Owned",403)
    updated = change_device_by_user(current_user,device,date_time,devices)
    return success_request(message="Successfully Changed",code=200,data=updated)

@owner_required
def c_change_device_sensor(device : dict,sensor : dict,current_user):
    date_time = now.strftime("%m-%d-%Y %H:%M:%S")
    devices = get_device_file()
    get_ = get_device(device['id'],devices,current_user,None)
    if get_ is None:
        return bad_request("Not Found or Forbidden For Data Owned",403)
    updated = change_device_sensor_by_user(current_user,device,sensor,date_time,devices)
    return success_request(message="Successfully Changed",code=200,data=updated)

@owner_required
def c_get_device(id : str,current_user):
    devices = get_device_file()
    get_ = get_device(id,devices,current_user,None)
    message = "Successfully Get All Device"
    if get_ is None:
        return success_request(message="No data",code=404,data=get_)
    if id is not None:
        message = f"Successfully Get Device {id}"
    return success_request(message=message,code=200,data=get_)