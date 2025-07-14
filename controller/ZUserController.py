from flask import current_app
from helper.files import check_File,save_data
from datetime import datetime
from helper.enum import LevelRole
from helper.responses import bad_request,success_request
from helper.function import generate_token,generate_userId,pagination
from helper.zUserQuery import checkExist as userExistCheck,insert as userInsert,\
    change as userChange,queryListUsingSearch as userlistSearch
from helper.zAuthQuery import checkExistUserId as authExistCheck
from helper.zCompanyQuery import checkExist as companyExistCheck
from helper.crypto_password import e_password
from itertools import islice
from .ZAuthController import user_to_authRegister,auth_activate,auth_delete,auth_change

superadmin = [LevelRole.SuperAdmin.value]
adminTeam = [LevelRole.SuperAdmin.value,LevelRole.adminTeam.value]
supportTeam = [LevelRole.SuperAdmin.value,LevelRole.adminTeam.value,LevelRole.supportTeam.value]
admin = [LevelRole.Admin.value]
clientStaff = [LevelRole.Manager.value,LevelRole.Staff.value,LevelRole.Supervisor.value]

# REGISTER
def user_create(data: dict,current_user):
    filenames_create = "zuser.json"
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user_id = generate_userId()
    if check_File(filenames_create) is False:
        saveItem = filenames_create
        data2 = {}
        data2["zuser"] = []
        save_data(saveItem,data2)
    if check_File(filenames_create) is True:
        check = userExistCheck(data)
        if check is not None:
            message = "Your Email or Username is Already exist in System"
            return bad_request(message,400)
        data['id'] = user_id
        data['employee_code'] = data['employee_code'] if 'employee_code' in data else ""
        data['employee_email'] = data['employee_email'] if 'employee_email' in data else ""
        data['send_email'] = False
        data['password'] = e_password(data['password'])
        data['role'] = data['role'] if "role" in data else "staff"
        data['access_admin'] = True if data['role']=="admin" else False
        data['access_login'] = data['access_login']
        data['access_module'] = []
        data['deleted'] = False
        data['created_date'] = date_time
        data['last_updated'] = date_time
        data['created_by'] = current_user['username']
    if data['access_login'] == False and data['role'] not in admin and current_user['role'] in admin:
        userInsert(data)
        return success_request("Successfully",200,None)
    if data['access_login'] == True and data['role'] not in admin and current_user['role'] in admin:
        userInsert(data)
        return user_to_authRegister(data,current_user)
    if data['access_login'] == True and data['role'] in admin and current_user['role'] in supportTeam:
        userInsert(data)
        return user_to_authRegister(data,current_user)
    else:
        return bad_request("Forbidden, Admin Role only Team Admin Access",400)
    

def user_change(post: dict,current_user):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    post['updated_by'] = current_user['username']
    userChange(post['id'],post,date_time)
    if 'auth_account' in post:
       return auth_change(post['auth_account'],current_user)
    return success_request("Data Updated",200,data=None)

def user_activate(post: dict,current_user):
    data={}
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "auth_account" not in post:
        return bad_request("User Not Found ",400)
    data['updated_by'] = current_user['username']
    userChange(post['id'],post,date_time)
    return auth_activate(post,current_user)

def user_delete(post: dict,current_user):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    userChange(post['id'],post,date_time)
    if "auth_account" in post:
        return auth_delete(post,current_user)
    return success_request("Data Updated",200,data=None)

def user_show(post: dict,current_user):
    getUser = userExistCheck(post)
    if getUser is None:
        return bad_request("Not Found",404)
    user = getUser[0]
    return success_request("Data Updated",200,data=user)

def user_addCompany(post: dict,current_user):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    getUser = userExistCheck(post)
    if getUser is None:
        return bad_request("Not Found",404)
    user = getUser[0]
    userChange(post['id'],post,date_time)
    return success_request("Data Updated",200,data=None)

def user_addstore(post: dict,current_user):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    getUser = userExistCheck(post)
    if getUser is None:
        return bad_request("Not Found",404)
    user = getUser[0]
    userChange(post['id'],post,date_time)
    return success_request("Data Updated",200,data=None)


def user_list_search (post_data: dict, current_user):
    per_page = 10
    if check_File("zuser.json") is False:
        total_data = 0
        page = 0 
        getPage = pagination(page,total_data,per_page)
        result = {"data":[],"pagination":getPage}
        return success_request("Succesfully Get Data",200,result)
    getUser = userlistSearch(post_data)
    total_data = 0 if getUser is None else len(getUser)
    page = 0 if post_data['page'] is None else post_data['page'] 
    getPage = pagination(page,total_data,per_page)
    if not getUser:
        result = {"data":[],"pagination":getPage}
        return success_request("Succesfully Get Data",200,result)
    if getPage['start'] < 0:
        result = {"data":[],"pagination":getPage}
        return success_request("Succesfully Get Data",200,result)
    for x in getUser:
        ath = authExistCheck(x) if getUser is not None else ""
        getc = {}
        if 'company_id' in x:
            if x['company_id'] != "":
                getc['id'] = x['company_id']
                company = companyExistCheck(getc) if getUser is not None else ""
                if company:
                    x['company'] = company[0]
                    del x['company_id']       
        if ath:
            x['auth_account'] = ath[0]
        
    filtered_data = [item for item in islice(getUser, getPage['start'], getPage['stop'])]
    result = {"data":filtered_data,"pagination":getPage}
    return success_request("Succesfully Get Data",200,result)
 