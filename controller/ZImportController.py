from flask import current_app,request
import pandas
from helper.files import save_file_temps,delete_files,save_data_upload,load_data_uploads,\
    check_File,save_data
from datetime import datetime
from helper.enum import LevelRole
from werkzeug.utils import secure_filename
from helper.responses import bad_request,success_request
from helper.function import generate_auth_id,generate_product_id,generate_store_id
from helper.zOutletQuery import insert as outletInsert,checkExist as outletCheckExist
from helper.zUserQuery import checkExist as userExistCheck,insert as userInsert
from helper.zDeviceQuery import change as deviceChange
from .ZAuthController import user_to_authRegisterImport
from helper.crypto_password import e_password
from helper.zProductQuery import insert as productInsert,checkExist as productCheckExist

superadmin = [LevelRole.SuperAdmin.value]
adminTeam = [LevelRole.SuperAdmin.value,LevelRole.adminTeam.value]
supportTeam = [LevelRole.SuperAdmin.value,LevelRole.adminTeam.value,LevelRole.supportTeam.value]
admin = [LevelRole.Admin.value]
clientStaff = [LevelRole.Manager.value,LevelRole.Staff.value,LevelRole.Supervisor.value]
ALLOWED_EXTENSIONS = ['xlsx']
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# IMPORT OUTLET
def add_importStore(company_id,current_user):
    date_time = datetime.now().strftime('%Y%m%d%H%M%S')
    if 'file' not in request.files:
        return bad_request(f"Tidak ada File",400)
    file = request.files['file']
    if file.filename == '':
        bad_request("No Selected File",400)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        custom_fileName = company_id+"outlet"+date_time
        save_file_temps(file,filename,custom_fileName)
        data = pandas.read_excel("uploads_temp/"+custom_fileName+".xlsx")
        json_string_columns = data.to_json()
        json_string_columns2 = data.to_json(orient='records')
        print(json_string_columns)
        print(json_string_columns2)
        result = {}
        setToList = []
        for index, row in data.iterrows():
            raw = {}
            raw['store_id'] = row['store_id'] if 'store_id' in row else None
            raw['store_name'] = row['store_name'] if 'store_name' in row else None
            raw['store_email'] = row['store_email'] if 'store_email' in row else None
            raw['store_address'] = row['store_address'] if 'store_address' in row else None
            raw['activate'] = True
            raw['deleted'] = False
            setToList.append(raw)
        save_data_upload(custom_fileName+".json",setToList)
        result['file_xls'] = custom_fileName+".xlsx"
        result['file_json'] = custom_fileName+".json"
        result['data'] = setToList
        return success_request("Successfully",200,result)
        # success = delete_files("uploads_temp/",custom_fileName+".xlsx")
        # if success:
        #     return success_request(f"Successfully Save File {custom_fileName}",200,F)
        # else:
        #     return bad_request(f"Gagal Delete {custom_fileName}",400)
    else:
        return bad_request("Format not Allowed, Only xlsx format",400)
        
# IMPORT USER
def add_importUser(company_id,current_user):
    date_time = datetime.now().strftime('%Y%m%d%H%M%S')
    if 'file' not in request.files:
        return bad_request(f"Tidak ada File",400)
    file = request.files['file']
    if file.filename == '':
        bad_request("No Selected File",400)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        custom_fileName = company_id+"user"+date_time
        save_file_temps(file,filename,custom_fileName)
        data = pandas.read_excel("uploads_temp/"+custom_fileName+".xlsx")
        json_string_columns = data.to_json()
        json_string_columns2 = data.to_json(orient='records')
        result = {}
        setToList = []
        for index, row in data.iterrows():
            raw = {}
            if "company_id" not in row:
                continue
            raw['company_id'] = str(row['employee_id']) if 'employee_id' in row else None
            raw['employee_id'] = str(row['employee_id']) if 'employee_id' in row else None
            raw['employee_name'] = row['employee_name'] if 'employee_name' in row else None
            raw['employee_email'] = row['employee_email'] if 'employee_email' in row else None
            raw['username'] = row['username'] if 'username' in row else None
            raw['email'] = row['email'] if 'email' in row else None
            raw['password'] = e_password(row['password']) if 'password' in row else e_password("12345!")
            raw['role'] = row['role'] if 'role' in row else "staff"
            raw['access_login'] = True if row['access_login'] == 1 else False
            raw['activate'] = False
            raw['deleted'] = False
            raw["loggedIn"] = False
            raw['id'] = generate_auth_id()
            raw['created_date'] = date_time
            raw['last_updated'] = date_time
            setToList.append(raw)
        save_data_upload(custom_fileName+".json",setToList)
        result['file_xls'] = custom_fileName+".xlsx"
        result['file_json'] = custom_fileName+".json"
        result['data'] = setToList
        return success_request("Successfully",200,result)
        # success = delete_files("uploads_temp/",custom_fileName+".xlsx")
        # if success:
        #     return success_request(f"Successfully Save File {custom_fileName}",200,F)
        # else:
        #     return bad_request(f"Gagal Delete {custom_fileName}",400)
    else:
        return bad_request ("Format not Allowed, Only xlsx format",400)

# IMPORT OUTLET
def add_importProduct(company_id,current_user):
    date_time = datetime.now().strftime('%Y%m%d%H%M%S')
    if 'file' not in request.files:
        return bad_request(f"Tidak ada File",400)
   
    file = request.files['file']
    if file.filename == '':
        bad_request("No Selected File",400)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        custom_fileName = company_id+"outlet"+date_time
        save_file_temps(file,filename,custom_fileName)
        data = pandas.read_excel("uploads_temp/"+custom_fileName+".xlsx")
        json_string_columns = data.to_json()
        json_string_columns2 = data.to_json(orient='records')
        print(json_string_columns)
        print(json_string_columns2)
        result = {}
        setToList = []
        for index, row in data.iterrows():
            raw = {}
            raw['location'] = {}
            raw['size'] = {}
            store = []
            if 'stores' in row:
                listStore = row['stores'].split(';')
                for k in listStore:
                   st = {}
                   st['store_id'] = k
                   st['company_id'] = company_id
                   store.append(st)
            raw['store'] = store
            raw['sku'] = str(row['sku']) if 'sku' in row else None
            raw['item_name'] = row['item_name'] if 'item_name' in row else None
            raw['item_category'] = row['item_category'] if 'item_category' in row else None
            raw['item_price'] = str(row['item_price']) if 'item_price' in row else None
            raw['item_desc'] = row['item_desc'] if 'item_desc' in row else None
            raw['item_active'] = True if row['item_active'] == 1 else False
            raw['item_disc'] = str(row['item_disc']) if 'item_disc' in row else None
            raw['item_price_disc'] = "0"
            raw['item_disc_status'] = False
            raw['item_image'] = ""
            raw['item_qris']="https://www.google.com"
            raw['item_qris_status']= False
            raw['location']['zone'] = row['zone'] if 'zone' in row else None
            raw['location']['aisle'] = row['aisle'] if 'aisle' in row else None
            raw['location']['section'] = row['section'] if 'section' in row else None
            raw['location']['position'] = row['position'] if 'position' in row else None
            raw['location']['level'] = row['level'] if 'level' in row else None
            raw['location']['rack'] = row['rack'] if 'rack' in row else None
            raw['location']['color'] = row['color'] if 'color' in row else None
            raw['size']['weight'] = row['weight'] if 'weight' in row else None
            raw['size']['height'] = row['height'] if 'height' in row else None
            raw['size']['width'] = row['width'] if 'width' in row else None
            raw['size']['dimension'] = row['dimension'] if 'dimension' in row else None
            raw['size']['color'] = row['color'] if 'color' in row else None
            raw['size']['uom'] = row['uom'] if 'uom' in row else None
            raw['activate'] = True
            raw['deleted'] = False
            setToList.append(raw)
        save_data_upload(custom_fileName+".json",setToList)
        result['file_xls'] = custom_fileName+".xlsx"
        result['file_json'] = custom_fileName+".json"
        result['data'] = setToList
        return success_request("Successfully",200,result)
        # success = delete_files("uploads_temp/",custom_fileName+".xlsx")
        # if success:
        #     return success_request(f"Successfully Save File {custom_fileName}",200,F)
        # else:
        #     return bad_request(f"Gagal Delete {custom_fileName}",400)
    else:
        return bad_request("Format not Allowed, Only xlsx format",400)
    

# IMPORT CONTENT
def add_content(company_id,current_user):
    date_time = datetime.now().strftime('%Y%m%d%H%M%S')
    years = datetime.now().strftime('%Y')
    fileStore = "device"+years+".json"
    if 'file' not in request.files:
        return bad_request(f"Tidak ada File",400)
    file = request.files['file']
    if file.filename == '':
        bad_request("No Selected File",400)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        custom_fileName = company_id+"content"+date_time
        save_file_temps(file,filename,custom_fileName)
        data = pandas.read_excel("uploads_temp/"+custom_fileName+".xlsx")
        json_string_columns = data.to_json()
        json_string_columns2 = data.to_json(orient='records')
        print(json_string_columns)
        print(json_string_columns2)
        result = {}
        setToList = []
        for index, row in data.iterrows():
            raw = {}
            raw['id'] = str(row['device']) if 'device' in row else ""
            raw['client_owner_id'] = str(row['company_id']) if 'company_id' in row else ""
            raw['client_store_id'] = str(row['store_id']) if 'store_id' in row else ""
            raw['content_header1'] = str(row['content_header1']) if 'content_header1' in row else ""
            raw['content_header2'] = str(row['content_header2']) if 'content_header2' in row else ""
            raw['content_header_right'] = str(row['content_header_right']) if 'content_header_right' in row else ""
            raw['content_footer_center'] = str(row['content_footer_center']) if 'content_footer_center' in row else ""
            raw['content_footer_left'] = str(row['content_footer_left']) if 'content_footer_left' in row else ""
            raw['content_footer_strike'] = str(row['content_footer_strike']) if 'content_footer_strike' in row else ""
            raw['content_footer_right'] = str(row['content_footer_right']) if 'content_footer_right' in row else ""
            raw['content_footer_center_sub'] = str(row['content_footer_center_sub']) if 'content_footer_center_sub' in row else ""
            raw['content_footer_right_sub'] = str(row['content_footer_right_sub']) if 'content_footer_right_sub' in row else ""
            raw['updated'] = True
            #deviceChange(str(row['device']),raw,fileStore,date_time)
            setToList.append(raw)
        save_data_upload(custom_fileName+".json",setToList)
        result['file_xls'] = custom_fileName+".xlsx"
        result['file_json'] = custom_fileName+".json"
        result['data'] = setToList
        return success_request("Successfully",200,result)
        # success = delete_files("uploads_temp/",custom_fileName+".xlsx")
        # if success:
        #     return success_request(f"Successfully Save File {custom_fileName}",200,F)
        # else:
        #     return bad_request(f"Gagal Delete {custom_fileName}",400)
    else:
        return bad_request("Format not Allowed, Only xlsx format",400)

# UPDATE CONTENT
def update_content(company_id,file_xls,file_json,current_user):
    getListUpload = load_data_uploads(file_json)
    if company_id is None:
        return bad_request("Company mandatory not Found ",400)
    process_data = 0
    total_data = len(getListUpload)
    years = datetime.now().strftime('%Y')
    fileStore = "device"+years+".json"
    for io in getListUpload:
        process_data += 1
        date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        deviceChange(str(io['id']),io,fileStore,date_time)
    if process_data == total_data:
        delete_files("uploads_temp/",file_xls)
        return success_request("Successfully",200,None)



# SAVE OUTLET
def save_importStore(company_id,file_xls,file_json,current_user):
    getListUpload = load_data_uploads(file_json)
    if company_id is None:
        return bad_request("Company mandatory not Found ",400)
    filenames_create = "outlet/"+"outlet"+company_id+".json"
    if check_File(filenames_create) is False:
        saveItem = filenames_create
        data2 = {}
        data2["zoutlet"] = []
        save_data(saveItem,data2)
    process_data = 0
    total_data = len(getListUpload)
    for io in getListUpload:
        process_data += 1
        post = {}
        date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        fileStore = "outlet"+company_id+".json"
        check = outletCheckExist(io,fileStore)
        if check :
            continue
        Cid = company_id[-12:]
        outlet_id = generate_store_id(fileStore)
        post['company_id'] = company_id
        post['store_id'] = io['store_name']
        post['store_name'] = io['store_name'] 
        post['store_email'] = io['store_email'] if io['store_email'] is not None else "email@store.com"
        post['store_address'] = io['store_address']
        post['id'] = outlet_id
        post['deleted'] = False
        post['activate'] = False
        post['created_date'] = date_time
        post['last_updated'] = date_time
        post['created_by'] = current_user['username']
        outletInsert(post,fileStore)
    if process_data == total_data:
        delete_files("uploads_temp/",file_xls)
        return success_request("Successfully",200,None)
    
# SAVE USER
def save_importUser(company_id,file_xls,file_json,current_user):
    getListUpload = load_data_uploads(file_json)
    if company_id is None:
        return bad_request("Company mandatory not Found ",400)
    process_data = 0
    total_data = len(getListUpload)
    for io in getListUpload:
        process_data += 1
        date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        check = userExistCheck(io)
        if check:
            continue
        io['company_id'] = company_id
        io['created_date'] = date_time
        io['last_updated'] = date_time
        userInsert(io)
        user_to_authRegisterImport(io,current_user)
    if process_data == total_data:
        delete_files("uploads_temp/",file_xls)
        return success_request("Successfully",200,None)

# SAVE Product
def save_importProduct(company_id,file_xls,file_json,current_user):
    getListUpload = load_data_uploads(file_json)
    if company_id is None:
        return bad_request("Company mandatory not Found ",400)

    total_data = len(getListUpload)
    process_data = 0
    for post in getListUpload:
        process_data += 1
        if 'store' not in post:
            continue
        storeList = post['store']
        for store in storeList:
            date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            filenames_create = "product/"+"product"+store['store_id']+".json"
            Cid = store['company_id'][-6:]
            Sid = store['store_id'][-5:]
            product_id = generate_product_id(filenames_create)
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
    if process_data == total_data:
        delete_files("uploads_temp/",file_xls)
        return success_request("Successfully",200,None)
    
        
# IMPORT OUTLET
def cancel_importData(company_id,file_xls,file_json,current_user):
    date_time = datetime.now().strftime('%Y%m%d%H%M%S')
    if file_xls is not None:
        success = delete_files("uploads_temp/",file_xls)
        success_2 = delete_files("uploads/",file_json)
        if success and success_2:
            return success_request(f"Successfully Cancel Import",200,None)
        else:
                return bad_request(f"Gagal Delete {file_xls}",400)
    else:
        return bad_request("File Not Found",400)
            
            
