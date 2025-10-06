from helper.files import check_File,save_data
from datetime import datetime
from helper.enum import LevelRole
from helper.responses import success_request
from helper.function import generate_auth_id
from helper.zAuthQuery import checkExist as authExistCheck,insert as authInsert,\
    change as authChange,queryListUsingSearch as authListSearch
from helper.crypto_password import verify_password,open_key,e_password
from itertools import islice

superadmin = [LevelRole.SuperAdmin.value]
adminTeam = [LevelRole.SuperAdmin.value,LevelRole.adminTeam.value]
supportTeam = [LevelRole.SuperAdmin.value,LevelRole.adminTeam.value,LevelRole.supportTeam.value]
admin = [LevelRole.SuperAdmin.value,LevelRole.adminTeam.value,LevelRole.Admin.value]
clientAdmin = [LevelRole.Admin.value]

# REGISTER
def init_auth(data: dict):
    filenames_create = "zauth.json"
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    auth_id = generate_auth_id()
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
        data['activate'] = True
        data['access_login'] = True
        data['password'] = e_password(data['password'])
        data['created_date'] = date_time
        data['last_updated'] = date_time
        print(data)
        authInsert(data)
    return success_request("Successfully",200,None)