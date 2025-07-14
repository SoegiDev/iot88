from flask import current_app,request
from helper.files import check_File,save_data,create_dir,get_listResources_files
from datetime import datetime
from helper.enum import LevelRole
from helper.responses import bad_request,success_request
from helper.function import generate_productId,pagination
from helper.zProductQuery import checkExist as productCheckExist,\
    insert as productInsert,queryListUsingSearch as productListSearch,\
        change as productChange
from helper.zOutletQuery import queryListUsingSearch as outletListSearch
        
from itertools import islice

superadmin = [LevelRole.SuperAdmin.value]
adminTeam = [LevelRole.SuperAdmin.value,LevelRole.adminTeam.value]
supportTeam = [LevelRole.SuperAdmin.value,LevelRole.adminTeam.value,LevelRole.supportTeam.value]
admin = [LevelRole.Admin.value]
clientStaff = [LevelRole.Manager.value,LevelRole.Supervisor.value,LevelRole.Staff.value]
storeAccess = ['product/activate','product/delete']
# REGISTER
def product_create(post: dict,current_user):
    create_dir("resources/product")
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if 'store' not in post:
        return bad_request("Store not Found",400)
    storeList = post['store']
    for store in storeList:
        filenames_create = "product/"+"product"+store['store_id']+".json"
        Cid = store['company_id'][-6:]
        Sid = store['store_id'][-5:]
        product_id = generate_productId(Cid,Sid)
        if check_File(filenames_create) is False:
            saveItem = filenames_create
            data2 = {}
            data2["zproduct"] = []
            save_data(saveItem,data2)
        if check_File(filenames_create) is True:
            fileStore = "product"+store['store_id']+".json"
            check = productCheckExist(post,fileStore)
            if check is not None:
                continue
            post['id'] = product_id
            post['deleted'] = False
            post['activate'] = False
            post['created_date'] = date_time
            post['last_updated'] = date_time
            post['created_by'] = current_user['username']
            if 'store' in post :
                del post['store']
            productInsert(post,fileStore)
    return success_request("Successfully",200,None)

def product_list_search (post_data: dict, current_user):
    ListProduct = []
    per_page = 10
    create_dir("resources/product")
    roleType = 0
    if current_user['role'] in supportTeam:
        roleType = 0
    if current_user['role'] in admin:
        roleType = 1
    if current_user['role'] in clientStaff:
        roleType = 2
    print(f"Role Type {roleType}")
    if roleType == 0:
        listData = get_listResources_files("product")
        if post_data['store_id'] is None:
            for x in listData:
                getProduct = productListSearch(post_data,x)
                if getProduct:
                    for item in getProduct:
                        ListProduct.append(item)
        else:     
            fileStore = "product"+post_data['store_id']+".json"
            checkFile = check_File("product/"+fileStore)
            getProduct = None
            if checkFile is False:
                getProduct = None
            else:
                getProduct = productListSearch(post_data,fileStore)
                ListProduct = getProduct
    if roleType == 1:
        if post_data['company_id'] is None:
            page = 0 if post_data['page'] is None else post_data['page'] 
            getPage = pagination(page,0,per_page)
            result = {"data":[],"pagination":getPage}
            return success_request("Company Mandatory Not Found",200,result)
        else:
            fileStore = "outlet"+post_data['company_id']+".json"
            checkFile = check_File("outlet/"+fileStore)
            getProduct = None
            if checkFile is False:
                getProduct = None
            else:
                companySearch = {}
                companySearch['query'] = None
                companySearch['company_id'] = post_data['company_id']
                getOutlet = outletListSearch(companySearch,fileStore)
                if getOutlet:
                    for out in getOutlet:
                        fileStore = "product"+out['id']+".json"
                        checkFile = check_File("product/"+fileStore)
                        if checkFile:
                            print(f"CheckFile {checkFile}")
                            out['query'] = post_data['query']
                            out['store_id'] = out['id']
                            getProduct = productListSearch(out,fileStore)
                            if getProduct:
                                for prod in getProduct:
                                    prod['store_id'] = out['id']
                                    prod['store_name'] = out['store_name']
                                    ListProduct.append(prod)

    if roleType == 2:
        if not current_user['user_account']['store']:
            page = 0 if post_data['page'] is None else post_data['page'] 
            getPage = pagination(page,0,per_page)
            result = {"data":[],"pagination":getPage}
            return success_request("Your Account Not Found Store",200,result)
        else:     
            storeList = current_user['user_account']['store']
            print(f"STOREE LIST {storeList}")
            for x in storeList:
                fileStore = "product"+x['store_id']+".json"
                checkFile = check_File("product/"+fileStore)
                if checkFile:
                    print(f"CheckFile {checkFile}")
                    x['query'] = post_data['query']
                    x['store_id'] = x['store_id']
                    getProduct = productListSearch(x,fileStore)
                    if getProduct:
                        for prod in getProduct:
                            ListProduct.append(prod)
    total_data = 0 if not ListProduct else len(ListProduct)
    page = 0 if post_data['page'] is None else post_data['page'] 
    getPage = pagination(page,total_data,per_page)
    if not ListProduct:
        result = {"data":[],"pagination":getPage}
        return success_request("Succesfully Get Data",200,result)
    if getPage['start'] < 0:
        result = {"data":[],"pagination":getPage}
        return success_request("Succesfully Get Data",200,result)
    filtered_data = [item for item in islice(ListProduct, getPage['start'], getPage['stop'])]
    result = {"data":filtered_data,"pagination":getPage}
    return success_request("Succesfully Get Data",200,result)

def product_show(post: dict,current_user):
    fileStore = "product"+post['store_id']+".json"
    getProduct = productCheckExist(post,fileStore)
    product = getProduct[0]
    return success_request("Data Updated",200,data=product)

def product_change(post: dict,current_user):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    post['updated_by'] = current_user['username']
    storeId = post['store_id']
    fileStore = "product"+storeId+".json"
    del post['store_id']
    productChange(post['id'],post,fileStore,date_time)
    return success_request("Data Updated",200,data=None)