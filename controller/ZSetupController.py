from flask import current_app
from helper.files import check_File,save_data
from datetime import datetime
from helper.enum import LevelRole
from helper.responses import bad_request,success_request
from helper.function import generate_token,generate_userId,pagination
from helper.zSetupQuery import checkExist as setupExistQuery,insert as setupInsert,\
    queryListUsingSearch as setupListSearch,change as setupChange
from itertools import islice

superadmin = [LevelRole.SuperAdmin.value]
adminTeam = [LevelRole.SuperAdmin.value,LevelRole.adminTeam.value]
supportTeam = [LevelRole.SuperAdmin.value,LevelRole.adminTeam.value,LevelRole.supportTeam.value]
admin = [LevelRole.SuperAdmin.value,LevelRole.adminTeam.value,LevelRole.Admin.value]
clientAdmin = [LevelRole.Admin.value,LevelRole.Manager.value]

# REGISTER
def setup_create(data: dict,current_user):
    filenames_create = "zsetup.json"
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user_id = generate_userId()
    if check_File(filenames_create) is False:
        saveItem = filenames_create
        data2 = {}
        data2["zset"] = []
        save_data(saveItem,data2)
    if check_File(filenames_create) is True:
        check = setupExistQuery(data)
        if check is not None:
            message = "Your Company Name or ID is Already exist in System"
            return success_request(message,200,check)
        data['id'] = user_id
        data['deleted'] = False
        data['activate'] = False
        data['created_date'] = date_time
        data['last_updated'] = date_time
        setupInsert(data)
    return success_request("Successfully",200,None)

def setup_list_search (post_data: dict, current_user):
    per_page = 10
    getCompany = setupListSearch(post_data)
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

def setup_show(post: dict,current_user):
    getCompany = setupExistQuery(post)
    company = getCompany[0] 
    return success_request("Data Updated",200,data=company)

def setup_change(post: dict,current_user):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    post['updated_by'] = current_user['username']
    setupChange(post['id'],post,date_time)
    return success_request("Data Updated",200,data=None)