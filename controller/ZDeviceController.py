from datetime import datetime
from helper.function import generate_token,generate_key,pagination,generate_device_id
from helper.files import check_File,save_data,create_dir
from helper.responses import bad_request,success_request
from helper.zDeviceQuery import insert as deviceInsert,checkExist as deviceCheckExist,\
    change as deviceChange, queryListUsingSearch as devicelistSearch
from helper.zCompanyQuery import checkExist as companyCheckExist
from helper.zOutletQuery import checkExist as outletCheckExist
from helper.files import get_esl_file
from helper.enum import DirectoryFiles
from helper.enum import LevelRole
from itertools import islice
import re

superadmin = [LevelRole.SuperAdmin.value]
adminTeam = [LevelRole.SuperAdmin.value,LevelRole.adminTeam.value]
supportTeam = [LevelRole.SuperAdmin.value,LevelRole.adminTeam.value,LevelRole.supportTeam.value]
admin = [LevelRole.Admin.value]
clientStaff = [LevelRole.Manager.value,LevelRole.Staff.value,LevelRole.Supervisor.value]

# HOME
def deviceHome(post: dict,current_user):
    post = {}
    post = {"id":"Device","message":"Home"}
    return success_request("Successfully",200,post)

def device_esl_create(post: dict, current_app):
    create_dir("resources/device_esl")
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    filenames_create = "device_esl/"+"device.json"
    if check_File(filenames_create) is False:
        saveItem = filenames_create
        data2 = {}
        data2["zESL"] = []
        save_data(saveItem,data2)
    if check_File(filenames_create) is True:
        fileStore = "device.json"
        mac = post['mac_address'].replace(":", "")
        device : dict = {}
        device['id'] = mac
        check = deviceCheckExist(device,fileStore)
        print(f"HasilCheck {check}")
        if check is not None:
            return bad_request("Your Mac Address was Registered",400)
    mac = post['mac_address'].replace(":", "")
    device : dict = {}
    key = generate_key()
    ID = generate_device_id(fileStore)
    device['id'] = mac
    device['device_id'] = ID
    device['device_name'] = mac
    device['device_category'] = "esl_"+post['device_board'] if 'device_board' in post else ""
    device['device_size'] = post['device_size'] if 'device_size' in post else ""
    device['device_type'] = "esl"
    device['device_board'] = post['device_board'] if 'device_board' in post else ""
    device['device_chip'] = post['device_chip'] if 'device_chip' in post else ""
    device['device_identity'] = post['device_chip'][0:4] if 'device_chip' in post else ""
    device['device_location'] = "device_location"
    device['device_connected'] = False
    device["device_screen"] = True
    device['device_key'] = key
    device['device_version'] = "1.0.0" 
    device['base_mac_address'] = post['mac_address'] if 'mac_address' in post else "" 
    device['base_ip_address'] = post['base_ip_address'] if 'base_ip_address' in post else ""
    device['base_server'] = post['base_server'] if 'base_server' in post else ""
    device['base_endpoint'] = post['base_endpoint'] if 'base_endpoint' in post else ""
    device['base_wifi_ssid'] = post['base_wifi_ssid'] if 'base_wifi_ssid' in post else ""
    device['base_wifi_password'] = post['base_wifi_password'] if 'base_wifi_password' in post else ""
    device['base_server_connected'] = True if 'base_server_connected' in post else ""
    device['client_ip_address'] = post['client_ip_address'] if 'client_ip_address' in post else ""
    device['client_server'] = post['client_server'] if 'client_server' in post else ""
    device['client_endpoint'] = post['client_endpoint'] if 'client_endpoint' in post else ""
    device['client_wifi_ssid'] = post['client_wifi_ssid'] if 'client_wifi_ssid' in post else ""
    device['client_wifi_password'] = post['client_wifi_password'] if 'client_wifi_password' in post else ""
    device['client_owner_id'] = post['client_owner_id'] if 'client_owner_id' in post else ""
    device['client_store_id'] = post['client_store_id'] if 'client_store_id' in post else ""
    device['client_location'] = post['client_location'] if 'client_location' in post else ""
    device['client_server_connected'] = True if 'client_server_connected' in post else False
    device['deleted'] = False
    device['status'] = 0
    device['updated'] = False
    device['live_date'] = date_time
    device['live_end'] = date_time
    device['created_date'] = date_time
    device['last_updated'] = date_time
    device['created_by'] = "hardware"
    device['template'] = 1
    device["content_header1"] = "Header 1 (17)"
    device["content_header2"] = "Header 2 (17)"
    device["content_header_right"] = "code(13)"
    device["content_footer_center"] = "50000"
    device["content_footer_left"] = "10%"
    device["content_footer_strike"] = "70000"
    device["content_footer_right"] = "100gr"
    device["content_footer_center_sub"] = "2024-10-20"
    device["content_footer_right_sub"] = "Stock: 12"
    if device['id']=="":
         return bad_request("ID NOT FOUND",430)
    cToken : dict = {}
    cToken['id'] = mac
    cToken['device_key'] = key
    cToken['role'] = "device_ESL"
    token = generate_token(cToken,current_app)
    device['device_token'] = token
    esl_process = deviceInsert(device,fileStore)
    return success_request(message="Successfully Registered",code=201,data=esl_process)

def esl_get_token(post: dict,current_app):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    years = datetime.now().strftime('%Y')
    id = post['id'].replace(":", "")
    sendPost = {"id":id}
    fileStore = "device"+years+".json"
    getDevice = deviceCheckExist(sendPost,fileStore)
    if getDevice is None:
        message = f"Data Not Found"
        return bad_request(message=message,code=404)
    device = getDevice[0]
    result = {'id':device['id'],'device_key':device['device_key'],'device_token':device['device_token']}
    message = f"Successfully Get Data"
    return success_request("Successfully",code=200,data=result)

def esl_sync(post: dict, current_user):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    years = datetime.now().strftime('%Y')
    sendPost = {"id":current_user['id']}
    fileStore = "device.json"
    getDevice = deviceCheckExist(sendPost,fileStore)
    if getDevice is None:
        message = f"Data Not Found"
        return bad_request(message=message,code=404)
    get_ = getDevice[0]
    message = "Successfully Get All Device"
    data = {}
    data['base_ip_address'] = post['ip_address']
    data['client_ip_address'] = post['ip_address']
    data['device_connected'] = True
    data['client_server_connected'] = True
    deviceChange(current_user['id'],data,fileStore,date_time)
    
    list = {key: value for key, value in get_.items() if not key.startswith('content_')}
    return success_request("Successfully",code=200,data=list)


def esl_product(current_user):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    years = datetime.now().strftime('%Y')
    sendPost = {"id":current_user['id']}
    fileStore = "device.json"
    getDevice = deviceCheckExist(sendPost,fileStore)
    if getDevice is None:
        message = f"Data Not Found"
        return bad_request(message=message,code=404)
    get_ = getDevice[0]
    message = "Successfully Get All Device"
    return success_request("Successfully",code=200,data=get_)

def esl_content(current_user):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    years = datetime.now().strftime('%Y')
    sendPost = {"id":current_user['id']}
    fileStore = "device.json"
    getDevice = deviceCheckExist(sendPost,fileStore)
    if getDevice is None:
        message = f"Data Not Found"
        return bad_request(message=message,code=404)
    get_ = getDevice[0]
    message = "Successfully Get All Device"
    list = {key: value for key, value in get_.items() if key.startswith('content_')}
    list['updated'] = get_['updated']
    list['device_identity'] = get_['device_identity']
    list['content_header1'] = list['content_header1'][0:17]
    list['content_header2'] = list['content_header2'][0:17]
    list['content_header_right'] = list['content_header_right'][0:13]
    list['content_footer_center'] = list['content_footer_center'][0:7]
    list['content_footer_strike'] = list['content_footer_strike'][0:7]
    data = {}
    data['updated'] = False
    deviceChange(current_user['id'],data,fileStore,date_time)
    return success_request("Successfully",code=200,data=list)

def esl_ListSearch(post_data: dict, current_user):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    years = datetime.now().strftime('%Y')
    fileStore = "device.json"
    per_page = 12
    ListData = []
    if check_File("device_esl/"+fileStore) is False:
        total_data = 0
        page = 0 
        getPage = pagination(page,total_data,per_page)
        result = {"data":[],"pagination":getPage}
        return success_request("Succesfully Get Data",200,result)
    getDevice = devicelistSearch(post_data,fileStore)
    total_data = 0 if getDevice is None else len(getDevice)
    page = 0 if post_data['page'] is None else post_data['page'] 
    getPage = pagination(page,total_data,per_page)
    if not getDevice:
        result = {"data":[],"pagination":getPage}
        return success_request("Succesfully Get Data",200,result)
    if getPage['start'] < 0:
        result = {"data":[],"pagination":getPage}
        return success_request("Succesfully Get Data",200,result)
    for x in getDevice:
        total_data = total_data +1
        data_ = x
        if x['client_owner_id'] != "":
            outletSearch = {"id":x['client_store_id']}
            companySearch = {"id":x['client_owner_id']}
            fileStore = "outlet"+x['client_owner_id']+".json"
            getOutlet = outletCheckExist(outletSearch,fileStore)
            getCompany = companyCheckExist(companySearch)
            data_["client_owner_name"] = getCompany[0]['company_name']
            data_["client_store_name"] = getOutlet[0]['store_name']
        ListData.append(data_)
    ListSearch = ListData
    total_data = 0 if ListSearch is None else len(ListSearch)
    page = 0 if post_data['page'] is None else post_data['page'] 
    getPage = pagination(page,total_data,per_page)
    if post_data['query'] != "":
        ListSearch = list(filter(
            lambda item:re.search(post_data['query'].lower(),item['client_owner_name'].lower()) or 
            re.search(post_data['query'].lower(),item['client_store_name'].lower()), ListData))
    filtered_data = [item for item in islice(ListSearch, getPage['start'], getPage['stop'])]
    result = {"data":filtered_data,"pagination":getPage}
    return success_request("Succesfully Get Data",200,result)
 
def esl_show(post: dict,current_user):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    years = datetime.now().strftime('%Y')
    fileStore = "device.json"
    getESL = deviceCheckExist(post,fileStore)
    if getESL is None:
        message = f"Data Not Found"
        return bad_request(message=message,code=404)
    data = getESL[0]
    if data['client_store_id'] != "":
        outletSearch = {"id":data['client_store_id']}
        companySearch = {"id":data['client_owner_id']}
        fileStore = "outlet"+data['client_owner_id']+".json"
        getOutlet = outletCheckExist(outletSearch,fileStore)
        getCompany = companyCheckExist(companySearch)
        data["client_owner_name"] = getCompany[0]['company_name']
        data["client_store_name"] = getOutlet[0]['store_name']
    return success_request("Data Updated",200,data=data)

def esl_change(post: dict,current_user):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    years = datetime.now().strftime('%Y')
    fileStore = "device.json"
    deviceChange(post['id'],post,fileStore,date_time)
    return success_request("Data Updated",200,data=None)
# # #RETRIEVE FROM WEB

# def esl_list(post_data: dict, current_user):
#     per_page = 10
#     list_esl = []
#     data_ = {}
#     get_data = eslList(post_data,None)
#     total_data = 0 if get_data is None else len(get_data)
#     page = 0 if post_data['page'] is None else post_data['page'] 
#     getPage = pagination(page,total_data,per_page)
#     if get_data is None:
#         result = {"data":[],"pagination":getPage}
#         return success_request("Successfully Get Data",200,result)
#     for x in get_data:
#         total_data = total_data +1
#         data_ = x
#         if x['client_owner_id'] != "":
#             data_['client_owner_name'] = get_company(x['client_owner_id'],["company_name"])['company_name']
#             data_["client_store_name"] = get_store(x['client_store_id'],["store_name"],DirectoryFiles.Stores.value,x['client_owner_id'])['store_name']
#         list_esl.append(data_)
#     if getPage['start'] < 0:
#         result = {"data":[],"pagination":getPage}
#         return success_request("Successfully Get Data",200,result)
#     filtered_data = [item for item in islice(list_esl, getPage['start'], getPage['stop'])]
#     result = {"data":filtered_data,"pagination":getPage}
#     return success_request("Successfully Get Data",200,result)

# def esl_list_for_add(post_data: dict, current_user):
#     per_page = 10
#     list_esl = []
#     data_ = {}
#     get_data = eslListForAdd(post_data,None)
#     print(f"Get Data {get_data}")
#     total_data = 0 if get_data is None else len(get_data)
#     page = 0 if post_data['page'] is None else post_data['page'] 
#     getPage = pagination(page,total_data,per_page)
#     if get_data is None:
#         result = {"data":[],"pagination":getPage}
#         return success_request("Successfully Get Data",200,result)
#     for x in get_data:
#         total_data = total_data +1
#         data_ = x
#         if x['client_owner_id'] != "":
#             data_['client_owner_name'] = get_company(x['client_owner_id'],["company_name"])['company_name']
#             data_["client_store_name"] = get_store(x['client_store_id'],["store_name"],DirectoryFiles.Stores.value,x['client_owner_id'])['store_name']
#         list_esl.append(data_)
#     if getPage['start'] < 0:
#         result = {"data":[],"pagination":getPage}
#         return success_request("Successfully Get Data",200,result)
#     filtered_data = [item for item in islice(list_esl, getPage['start'], getPage['stop'])]
#     result = {"data":filtered_data,"pagination":getPage}
#     return success_request("Successfully Get Data",200,result)

# def esl_listbycompany(post_data: dict, current_user):
#     per_page = 10
#     list_esl = []
#     data_ = {}
#     print(f" Data Store {post_data['store_id']}")
#     get_data = eslByCompany(post_data,post_data['company_id'],post_data['store_id'],None)
#     total_data = 0 if get_data is None else len(get_data)
#     page = 0 if post_data['page'] is None else post_data['page']
#     getPage = pagination(page,total_data,per_page) 
#     if get_data is None:
#         result = {"data":[],"pagination":getPage}
#         return success_request("Successfully Get Data",200,result)
#     for x in get_data:
#         total_data = total_data +1
#         data_ = x
#         if x['client_owner_id'] != "":
#             data_['client_owner_name'] = get_company(x['client_owner_id'],["company_name"])['company_name']
#             data_["client_store_name"] = get_store(x['client_store_id'],["store_name"],DirectoryFiles.Stores.value,x['client_owner_id'])['store_name']
#         list_esl.append(data_)
#     if getPage['start'] < 0:
#         result = {"data":[],"pagination":getPage}
#         return success_request("Successfully Get Data",200,result)
#     filtered_data = [item for item in islice(list_esl, getPage['start'], getPage['stop'])]
#     result = {"data":filtered_data,"pagination":getPage}
#     return success_request("Successfully Get Data",200,result)

# def esl_row(post_data: dict , current_user):
#     list_esl = []
#     data_ = {}
#     total_data = 0
#     get_ = eslRow(post_data['id'],None)
#     if get_ is None:
#         return bad_request("Data Not Found",400)
#     else:
#         if id is not None:
#             if get_['client_owner_id'] == "":
#                 get_['client_owner_name'] = ""    
#                 get_["client_store_name"] = ""    
#             else:
#                 get_['client_owner_name'] = get_company(get_['client_owner_id'],["company_name"])['company_name']
#                 get_["client_store_name"] = get_store(get_['client_store_id'],["store_name"],DirectoryFiles.Stores.value,get_['client_owner_id'])['store_name']
#             message = "Successfully Get Data"
#             return success_request(message=message,code=200,data=get_)
#         else:
#             message = "Successfully Get Data"
#             for x in get_:
#                 total_data = total_data +1
#                 data_ = x
#                 if x['client_owner_id'] != "":
#                     data_['client_owner_name'] = get_company(x['client_owner_id'],["company_name"])['company_name']
#                     data_["client_store_name"] = get_store(x['client_store_id'],["store_name"],DirectoryFiles.Stores.value,x['client_owner_id'])['store_name']
#                 else:
#                     data_['client_owner_name'] = ""
#                     data_['client_store_name'] = ""
#                 list_esl.append(data_)
#             return success_request(message=message,code=200,data=list_esl)

# def esl_change(data : dict,current_user):
#     date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     get_ = eslRow(data['id'],None)
#     data['updated_by'] = current_user['username']
#     if get_ is None:
#         return bad_request("Not Found or Forbidden For Data Owned",403)
#     updated = eslChange(data['id'],data,date_time)
#     return success_request(message="Successfully Changed",code=200,data=updated)