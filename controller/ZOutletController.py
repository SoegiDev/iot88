from flask import current_app,request
from helper.files import check_File,save_data,create_dir,get_listResources_files
from datetime import datetime
from helper.enum import LevelRole
from helper.responses import bad_request,success_request
from helper.function import generate_storeId,pagination
from helper.zOutletQuery import checkExist as outletCheckExist,\
    insert as outletInsert, queryListUsingSearch as outletListSearch,\
        change as outletChange
from itertools import islice

superadmin = [LevelRole.SuperAdmin.value]
adminTeam = [LevelRole.SuperAdmin.value,LevelRole.adminTeam.value]
supportTeam = [LevelRole.SuperAdmin.value,LevelRole.adminTeam.value,LevelRole.supportTeam.value]
admin = [LevelRole.Admin.value]
clientStaff = [LevelRole.Manager.value,LevelRole.Staff.value,LevelRole.Supervisor.value]

storeAccess = ['outlet/activate','outlet/delete']
# REGISTER
def outlet_create(post: dict,current_user):
    create_dir("resources/outlet")
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "company_id" not in post:
        return bad_request("Company mandatory not Found ",400)
    filenames_create = "outlet/"+"outlet"+post['company_id']+".json"
    Cid = post['company_id'][-12:]
    outlet_id = generate_storeId(Cid)
   
    if check_File(filenames_create) is False:
        saveItem = filenames_create
        data2 = {}
        data2["zoutlet"] = []
        save_data(saveItem,data2)
    if check_File(filenames_create) is True:
        fileStore = "outlet"+post['company_id']+".json"
        check = outletCheckExist(post,fileStore)
        if check is not None:
            message = "Your Company Name or ID is Already exist in System"
            return success_request(message,200,None)
        post['id'] = outlet_id
        post['deleted'] = False
        post['activate'] = False
        post['created_date'] = date_time
        post['last_updated'] = date_time
        post['created_by'] = current_user['username']
        outletInsert(post,fileStore)
    return success_request("Successfully",200,None)

def outlet_list_search (post_data: dict, current_user):
    ListOutlet = []
    per_page = 10
    create_dir("resources/outlet")
    roleType = 0
    if current_user['role'] in adminTeam:
        roleType = 0
    if current_user['role'] in admin:
        roleType = 1
    if current_user['role'] in clientStaff:
        roleType = 2
    print(f"Type ROle {roleType}")
    if roleType == 0:
        listData = get_listResources_files("outlet")
        if post_data['company_id'] is None:
            for x in listData:
                getOutlet = outletListSearch(post_data,x)
                print(f"List Outlet {getOutlet}")
                print(f"Type {type(getOutlet)}")
                if getOutlet:
                    for toko in getOutlet:
                        ListOutlet.append(toko)
        else:     
            fileStore = "outlet"+post_data['company_id']+".json"
            checkFile = check_File("outlet/"+fileStore)
            getOutlet = None
            if checkFile is False:
                print(f"CHeck file {checkFile}")
                getOutlet = None
            else:
                getOutlet = outletListSearch(post_data,fileStore)
                ListOutlet = getOutlet
    if roleType == 1:
        if post_data['company_id'] is None:
            page = 0 if post_data['page'] is None else post_data['page'] 
            getPage = pagination(page,0,per_page)
            result = {"data":[],"pagination":getPage}
            return success_request("Company Mandatory Not Found",200,result)
        else:     
            fileStore = "outlet"+post_data['company_id']+".json"
            checkFile = check_File("outlet/"+fileStore)
            getOutlet = None
            if checkFile is False:
                print(f"CHeck file {checkFile}")
                getOutlet = None
            else:
                getOutlet = outletListSearch(post_data,fileStore)
                ListOutlet = getOutlet
    if roleType == 2:
        if not current_user['user_account']['store']:
            page = 0 if post_data['page'] is None else post_data['page'] 
            getPage = pagination(page,0,per_page)
            result = {"data":[],"pagination":getPage}
            return success_request("Your Account Not Found Store",200,result)
        else:     
            storeList = current_user['user_account']['store']
            print(f"store List {storeList} ")
            for x in storeList:
                postSearch = {"id":x['store_id']}
                fileStore = "outlet"+x['company_id']+".json"
                getOutlet = outletCheckExist(postSearch,fileStore)
                if getOutlet:
                    for toko in getOutlet:
                        ListOutlet.append(toko)
                        
    total_data = 0 if not ListOutlet else len(ListOutlet)
    page = 0 if post_data['page'] is None else post_data['page'] 
    getPage = pagination(page,total_data,per_page)
    if not ListOutlet:
        result = {"data":[],"pagination":getPage}
        return success_request("Succesfully Get Data",200,result)
    if getPage['start'] < 0:
        result = {"data":[],"pagination":getPage}
        return success_request("Succesfully Get Data",200,result)
    filtered_data = [item for item in islice(ListOutlet, getPage['start'], getPage['stop'])]
    result = {"data":filtered_data,"pagination":getPage}
    return success_request("Succesfully Get Data",200,result)

def outlet_show(post: dict,current_user):
    rule = request.url_rule
    fileStore = "outlet"+post['company_id']+".json"
    getOutlet = outletCheckExist(post,fileStore)
    outlet = getOutlet[0]
    return success_request("Data Updated",200,data=outlet)

def outlet_change(post: dict,current_user):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    post['updated_by'] = current_user['username']
    fileStore = "outlet"+post['company_id']+".json"
    outletChange(post['id'],post,fileStore,date_time)
    return success_request("Data Updated",200,data=None)