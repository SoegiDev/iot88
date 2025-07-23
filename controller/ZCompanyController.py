from flask import current_app
from helper.files import check_File,save_data,check_dir
from datetime import datetime
from helper.enum import LevelRole
from helper.responses import bad_request,success_request
from helper.function import generate_token,generate_company_id,pagination
from helper.zCompanyQuery import checkExist as comExistCheck,insert as comInsert,\
    queryListUsingSearch as comListSearch,change as comChange
from .ZSetupController import setup_create
from itertools import islice

superadmin = [LevelRole.SuperAdmin.value]
adminTeam = [LevelRole.SuperAdmin.value,LevelRole.adminTeam.value]
supportTeam = [LevelRole.SuperAdmin.value,LevelRole.adminTeam.value,LevelRole.supportTeam.value]
admin = [LevelRole.SuperAdmin.value,LevelRole.adminTeam.value,LevelRole.Admin.value]
clientAdmin = [LevelRole.Admin.value]

# REGISTER
def company_create(data: dict,current_user):
    filenames_create = "zcompany.json"
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    company_id = generate_company_id()
    if check_File(filenames_create) is False:
        saveItem = filenames_create
        data2 = {}
        data2["zcom"] = []
        save_data(saveItem,data2)
    if check_File(filenames_create) is True:
        check = comExistCheck(data)
        if check is not None:
            message = "Your Company Name or ID is Already exist in System"
            return success_request(message,200,check)
        data['id'] = company_id
        data['deleted'] = False
        data['activate'] = False
        data['created_date'] = date_time
        data['last_updated'] = date_time
        comInsert(data)
        return setup_create(data,current_user)
    #return success_request("Successfully",200,None)

def company_list_search (post_data: dict, current_user):
    per_page = 10
    if check_File("zcompany.json") is False:
        total_data = 0
        page = 0 
        getPage = pagination(page,total_data,per_page)
        result = {"data":[],"pagination":getPage}
        return success_request("Succesfully Get Data",200,result)
    getCompany = comListSearch(post_data)
    total_data = 0 if getCompany is None else len(getCompany)
    page = 0 if post_data['page'] is None else post_data['page'] 
    getPage = pagination(page,total_data,per_page)
    if not getCompany:
        result = {"data":[],"pagination":getPage}
        return success_request("Succesfully Get Data",200,result)
    if getPage['start'] < 0:
        result = {"data":[],"pagination":getPage}
        return success_request("Succesfully Get Data",200,result)

    filtered_data = [item for item in islice(getCompany, getPage['start'], getPage['stop'])]
    result = {"data":filtered_data,"pagination":getPage}
    return success_request("Succesfully Get Data",200,result)

def company_show(post: dict,current_user):
    getCompany = comExistCheck(post)
    company = getCompany[0]
    return success_request("Data Updated",200,data=company)

def company_change(post: dict,current_user):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    post['updated_by'] = current_user['username']
    comChange(post['id'],post,date_time)
    return success_request("Data Updated",200,data=None)

def company_activate(post: dict,current_user):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    post['updated_by'] = current_user['username']
    comChange(post['id'],post,date_time)
    return success_request("Data Updated",200,data=None)

def company_delete(post: dict,current_user):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    post['updated_by'] = current_user['username']
    comChange(post['id'],post,date_time)
    return success_request("Data Updated",200,data=None)