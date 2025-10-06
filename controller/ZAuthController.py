from flask import current_app
from helper.files import check_File,save_data
from datetime import datetime
from helper.enum import LevelRole
from helper.responses import bad_request,success_request
from helper.function import generate_token,pagination,generate_auth_id
from helper.zAuthQuery import checkExist as authExistCheck,insert as authInsert,\
    change as authChange,queryListUsingSearch as authListSearch
from helper.zUserQuery import change as userChange,checkExist as userExistCheck
from helper.zCompanyQuery import checkExist as companyRow
from helper.crypto_password import verify_password,open_key,e_password
from itertools import islice

superadmin = [LevelRole.SuperAdmin.value]
adminTeam = [LevelRole.SuperAdmin.value,LevelRole.adminTeam.value]
supportTeam = [LevelRole.SuperAdmin.value,LevelRole.adminTeam.value,LevelRole.supportTeam.value]
admin = [LevelRole.SuperAdmin.value,LevelRole.adminTeam.value,LevelRole.Admin.value]
clientAdmin = [LevelRole.Admin.value]

# REGISTER
def auth_register(data: dict):
    filenames_create = "zauth.json"
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    auth_id = generate_auth_id()
    print(auth_id)
    print(check_File(filenames_create))
    if check_File(filenames_create) is False:
        saveItem = filenames_create
        data2 = {}
        data2["zauth"] = []
        save_data(saveItem,data2)
    if check_File(filenames_create) is True:
        check = len(authExistCheck(data))
        if check > 0:
            message = "Your Email or Username is Already exist in System"
            return success_request(message,200,check)
        data['id'] = auth_id
        data["loggedIn"] = False
        data['deleted'] = False
        data['activate'] = False
        data['access_login'] = True
        data['password'] = e_password(data['password'])
        data['created_date'] = date_time
        data['last_updated'] = date_time
        print(data)
        authInsert(data)
    return success_request("Successfully",200,None)

#LOGIN
def auth_login(post: dict):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    getUser = authExistCheck(post)
    if getUser:
        auth = getUser[0]
        key_secret = open_key()
        if auth['activate'] == False:
            return bad_request("Your account must Activate",400)
        verify = verify_password(key_secret,post['password'],auth['password'])
        if verify == False:
            return bad_request("Your password is incorrect",400)
        if auth['access_login'] == False:
            return bad_request("Your password is incorrect",400)
        token = generate_token(auth,current_app)
        updateData = {}
        updateData['updated_by'] = auth['username']
        updateData['loggedIn'] = True
        authChange(auth['id'],updateData,date_time)
        if "user_id" in auth:    
            userChange(auth['user_id'],updateData,date_time)
        return success_request("Successfully Login",200,data={"token":token,"data":auth})
    else:
        return bad_request("User is not found",400)

#cHANGE PASSWORD
def auth_change_password(data : dict,current_user):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    getUser = authExistCheck(data)
    if not getUser:
        return bad_request("User is not found",400)
    user = getUser[0]
    e_pass = e_password(data['password'])
    data['password'] = e_pass
    data['updated_by'] = current_user['username']
    authChange(user['id'],data,date_time)
    return success_request("Change Password Succesfully",200,data=None)

#SHOW
def auth_show(post : dict,current_user):
    getUser = authExistCheck(post)
    if not getUser:
        return bad_request("User is not found",400)
    user = getUser[0]
    return success_request("Change Password Succesfully",200,data=user)

#AUTH CHANGE
def auth_change(post : dict,current_user):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    post['updated_by'] = current_user['username']
    authChange(post['id'],post,date_time)
    return success_request("Data Updated",200,data=None)

#cHANGE ACTIVATE
def auth_activate(post : dict,current_user):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = {}
    getUser = []
    if "auth_account" in post:
        getUser = authExistCheck(post['auth_account'])
    if "auth_account" not in post:
        getUser = authExistCheck(post)
    if not getUser:
        return bad_request("User is not found",400)
    user = getUser[0]
    data['activate'] = True
    data['updated_by'] = current_user['username']
    authChange(user['id'],data,date_time)
    return success_request("Activated User Successfully",200,data=None)

def auth_delete(post : dict,current_user):
    data = {}
    getUser = []
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "auth_account" in post:
        getUser = authExistCheck(post['auth_account'])
    if "auth_account" not in post:
        getUser = authExistCheck(post)
    if not getUser:
        return bad_request("User is not found",400)
    user = getUser[0]
    data['deleted'] = post['deleted']
    data['updated_by'] = current_user['username']
    authChange(user['id'],data,date_time)
    return success_request("Data Updated",200,data=None)

# REGISTER
def user_to_authRegister(post: dict,current_user):
    data = {}
    if post['role'] == "admin":
        if current_user['role'] not in supportTeam:
            return bad_request("Forbidden Access For Change Role Admin, Admin Team Only",403)
    filenames_create = "zauth.json"
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    auth_id = generate_auth_id()
    if check_File(filenames_create) is False:
        saveItem = filenames_create
        data2 = {}
        data2["zauth"] = []
        save_data(saveItem,data2)
    if check_File(filenames_create) is True:
        check = authExistCheck(data)
        if check:
            message = "Your Email or Username is Already exist in System"
            return success_request(message,200,check)
        if "id" in post:
            data["user_id"] = post['id']
        data['username'] = post['username']
        data['email'] = post['email']
        data['role'] = post['role']
        data['id'] = auth_id
        data["loggedIn"] = False
        data['deleted'] = False
        data['activate'] = False
        data['access_login'] = post['access_login']
        data['password'] = post['password']
        data['created_date'] = date_time
        data['last_updated'] = date_time
        authInsert(data)
        print(f"USER POST {post}")
        user = userExistCheck(post)
        print(f"USER {user}")
        userData = {}
        userData['auth_account'] = data
        userChange(post['id'],userData,date_time)
    return success_request("Successfully",200,None)

def user_to_authRegisterImport(post: dict,current_user):
    data = {}
    if post['role'] == "admin":
        if current_user['role'] not in supportTeam:
            return bad_request("Forbidden Access For Change Role Admin, Admin Team Only",403)
    filenames_create = "zauth.json"
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    auth_id = generate_auth_id()
    if check_File(filenames_create) is False:
        saveItem = filenames_create
        data2 = {}
        data2["zauth"] = []
        save_data(saveItem,data2)
    if check_File(filenames_create) is True:
        check = authExistCheck(data)
        if check:
            message = "Your Email or Username is Already exist in System"
            return success_request(message,200,check)
        if "id" in post:
            data["user_id"] = post['id']
        data['username'] = post['username']
        data['email'] = post['email']
        data['role'] = post['role']
        data['id'] = auth_id
        data["loggedIn"] = False
        data['deleted'] = False
        data['activate'] = False
        data['access_login'] = post['access_login']
        data['password'] = post['password']
        data['created_date'] = date_time
        data['last_updated'] = date_time
        authInsert(data)
        searchuser ={"id":data['user_id']}
        user = userExistCheck(searchuser)
        userData = user[0]
        userData['auth_account'] = data
        userChange(data['user_id'],userData,date_time)
    return True

def auth_list_search (post_data: dict, current_user):
    per_page = 10
    getUser = authListSearch(post_data)
    total_data = 0 if getUser is None else len(getUser)
    page = 0 if post_data['page'] is None else post_data['page'] 
    getPage = pagination(page,total_data,per_page)
    if not getUser:
        result = {"data":[],"pagination":getPage}
        return success_request("Succesfully Get Data",200,result)
    if getPage['start'] < 0:
        result = {"data":[],"pagination":getPage}
        return success_request("Succesfully Get Data",200,result)
   
    filtered_data = [item for item in islice(getUser, getPage['start'], getPage['stop'])]
    result = {"data":filtered_data,"pagination":getPage}
    return success_request("Succesfully Get Data",200,result)

#GET PROFILE
def auth_profile(current_user):
    user_result = {}
    if "user_account" in current_user:
        user_result = current_user['user_account']
        if "company_id" in current_user["user_account"]:
            getCompany = {"id":user_result['company_id']}
            company = companyRow(getCompany)
            if company:
                user_result['company'] = company[0]
                del user_result['company_id']         
        if "store" not in user_result:
            user_result['store'] = []
        return success_request("Successfully Login",200,current_user)
    else:
        return success_request("Successfully Login",200,current_user) 
    
# GET PROFILE FOR TOKEN
def auth_profile_token(auth):
    postUser = {}
    getUser = None
    if "user_id" in auth:
        postUser['id'] = auth['user_id'] 
        getUser = userExistCheck(postUser)
    if getUser:
        print("ADA USER")
        user = getUser[0]
        if "company_id" not in user:
            user['company'] = {}
        if "store" not in user:
            user['store'] = []
        del user["auth_account"]
        auth['user_account'] = user
        return auth
    else:
        return auth
