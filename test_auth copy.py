from helper.function import generate_userId,generate_device_id
from helper.crypto_password import encrypt_password,verify_password,open_key,e_password
from helper.files import load_data,save_data,get_auth_file
from helper.query import check_username,check_email,get_login_username,get_password,data_users,change_password_md,r_device,r_device_admin
import sys
from helper.responses import bad_request,success_request
import json
from flask import Flask,request
from datetime import datetime
from decorators import add_log,admin_required

now = datetime.now() # current date and time

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>IOT BACKEND</p>"


def user_register(user : dict):
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
    auths["authentication"].append({"id": user_id,"username": username,"email":email,"password":password_list,"device":device_list})
    save_data("resources/auth.json",auths)
    return success_request(message="Successfully Registered",code=201,data=None)

def user_login(user : dict):
    auths = get_auth_file()
    username = user['username']
    password = user['password']
    check = check_username(username,auths)
    if check:
        get_data = get_login_username(username,auths,"password")
        key_secret = open_key()
        # verify = verify_password(key_secret,password,get_data[''])
        password_active = get_password(get_data,True)
        if password_active == None:
            return bad_request("Your password is inactive",400)
        verify = verify_password(key_secret,password,password_active['password'])
        if verify == False:
            return bad_request("Your password is incorrect",400)
        get_result = data_users(username,auths,['id',"email","username","device"])
        users = get_result
        return success_request("Successfully Login",200,users)
    else:
        return bad_request("User is not found",400)

def user_change_password(user : dict):
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
    change_password_md(username,e_pass,auths)
    date_time = now.strftime("%m-%d-%Y %H:%M:%S")
    print("date and time:",date_time)
    get_result = data_users(username,auths,['id',"email","username","device"])
    users = get_result
    return success_request("Change Password Succesfully",200,users)



def register_device(user : dict, device : dict):
    auths = get_auth_file()
    device_id = generate_device_id()
    username = user['username']
    email = user['email']
    c_username = check_username(username,auths)
    if c_username:
        return bad_request("User Already Exists",400)
    c_email = check_email(email,auths)
    if c_email:
        return bad_request("Email Already Exists",400)
    device_process = r_device(user,device,auths)
    if device_process is None:
        return bad_request("Role Not Acceptable",400)        
    return success_request(message="Successfully Registered",code=201,data=device_process)
    

# ====================== CONTROLLER ADMIN ====================#
def c_register_device(user,device : dict):
    date_time = now.strftime("%m-%d-%Y %H:%M:%S")
    device_id = generate_device_id()
    device['id'] = device_id
    device['live_date']=date_time
    device['live_end']=date_time
    device['created_date']=date_time
    device['last_updated']=date_time
    device['created_by'] = user['username']
    print(device)
    device_process = r_device_admin(device)
    return success_request(message="Successfully Registered",code=201,data=device_process)
    
#=================================== ROUTES ===========================#

@app.route('/change_password',methods=['POST'])
@add_log()
def create_change_password():
    users = json.loads(request.data)
    if users.get("username") is None:
        return bad_request("Username Field Must Filled",400)
    if users.get("password") is None:
        return bad_request("Password Field Must Filled",400)
    if users.get("email") is None:
        return bad_request("Email Field Must Filled",400)
    x = {}
    x['username'] =users['username']
    x['password'] =users['password']
    x['email'] =users['email']
    l_user = user_change_password(x)
    return l_user


@app.route('/login',methods=['POST'])
@add_log()
def create_login():
    users = json.loads(request.data)
    if users.get("username") is None:
        return bad_request("Username Field Must Filled",400)
    if users.get("password") is None:
        return bad_request("Password Field Must Filled",400)
    x = {}
    x['username'] =users['username']
    x['password'] =users['password']
    l_user = user_login(x)
    return l_user

@app.route('/register',methods=['POST'])
@add_log()
def create_register():
    users = json.loads(request.data)
    if users.get("username") is None:
        return bad_request("Username Field Must Filled",400)
    if users.get("password") is None:
        return bad_request("Password Field Must Filled",400)
    if users.get("email") is None:
        return bad_request("Email Field Must Filled",400)
    x = {}
    x['username'] =users['username']
    x['password'] =users['password']
    x['email'] =users['email']
    l_user = user_register(x)
    return l_user

@app.route('/register_device',methods=['POST'])
@add_log()
def create_register_device():
    username = request.args['username']
    email = request.args['email']
    y = request.get_json()
    x = {}    
    x['username'] =username
    x['email'] =email
    l_device = register_device(x,y)
    return l_device

@app.route('/admin_register_device',methods=['POST'])
@admin_required
@add_log()
def create_register_device_admin(current_user):
    y = request.get_json()
    user = current_user
    l_device = c_register_device(user,y)
    return l_device

if __name__ == '__main__':
   app = Flask(__name__)
    # username = str(sys.argv[1])
    # password = str(sys.argv[2])
    # a = {}
    # a = {"username":username,"password":password}
    # change_password_user(a)
    