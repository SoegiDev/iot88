from flask import request
from flask_cors import CORS
from decorators import add_log,token_required
from controller.ZImportController import add_importStore,cancel_importData,\
    save_importStore,add_importUser,save_importUser,add_importProduct,\
        save_importProduct,add_content,update_content
from flask import Blueprint

zImportBp = Blueprint('zImportBp', __name__)

@zImportBp.route('/add_outlet', methods=['POST'])
@token_required
def storeImport(current_user):
    print(f"Request {request.form}")
    company_id = None
    if "company_id" in request.form:        
        company_id = request.form.get('company_id') 
    resultData = add_importStore(company_id,current_user)
    return resultData

@zImportBp.route('/add_user', methods=['POST'])
@token_required
def userImport(current_user):
    print(f"Request {request.form}")
    company_id = None
    if "company_id" in request.form:        
        company_id = request.form.get('company_id') 
    resultData = add_importUser(company_id,current_user)
    return resultData

@zImportBp.route('/add_product', methods=['POST'])
@token_required
def productImport(current_user):
    print(f"Request {request.form}")
    company_id = None
    if "company_id" in request.form:        
        company_id = request.form.get('company_id') 
    resultData = add_importProduct(company_id,current_user)
    return resultData

@zImportBp.route('/add_content', methods=['POST'])
@token_required
def esl_addContent(current_user):
    print(f"Request {request.form}")
    company_id = None
    if "company_id" in request.form:        
        company_id = request.form.get('company_id') 
    resultData = add_content(company_id,current_user)
    return resultData

@zImportBp.route('/save_update_content', methods=['POST'])
@token_required
def esl_update_content(current_user):
    file_xls = None
    file_json = None
    jsonData = request.get_json()
    if "company_id" in jsonData:        
        company_id = jsonData['company_id']
    if "file_xls" in jsonData:        
        file_xls = jsonData['file_xls'] 
    if "file_json" in jsonData:        
        file_json = jsonData['file_json'] 
    resultData = update_content(company_id,file_xls,file_json,current_user)
    return resultData

@zImportBp.route('/cancel_import', methods=['POST'])
@token_required
def cancel_import(current_user):
    company_id = None
    file_xls = None
    file_json = None
    jsonData = request.get_json()
    if "company_id" in jsonData:        
        company_id = jsonData['company_id']
    if "file_xls" in jsonData:        
        file_xls = jsonData['file_xls'] 
    if "file_json" in jsonData:        
        file_json = jsonData['file_json'] 
    resultData = cancel_importData(company_id,file_xls,file_json,current_user)
    return resultData

@zImportBp.route('/save_import_outlet', methods=['POST'])
@token_required
def save_import_outlet(current_user):
    file_xls = None
    file_json = None
    jsonData = request.get_json()
    if "company_id" in jsonData:        
        company_id = jsonData['company_id']
    if "file_xls" in jsonData:        
        file_xls = jsonData['file_xls'] 
    if "file_json" in jsonData:        
        file_json = jsonData['file_json'] 
    resultData = save_importStore(company_id,file_xls,file_json,current_user)
    return resultData

@zImportBp.route('/save_import_user', methods=['POST'])
@token_required
def save_import_user(current_user):
    file_xls = None
    file_json = None
    jsonData = request.get_json()
    if "company_id" in jsonData:        
        company_id = jsonData['company_id']
    if "file_xls" in jsonData:        
        file_xls = jsonData['file_xls'] 
    if "file_json" in jsonData:        
        file_json = jsonData['file_json'] 
    resultData = save_importUser(company_id,file_xls,file_json,current_user)
    return resultData

@zImportBp.route('/save_import_product', methods=['POST'])
@token_required
def save_import_product(current_user):
    file_xls = None
    file_json = None
    jsonData = request.get_json()
    if "company_id" in jsonData:        
        company_id = jsonData['company_id']
    if "file_xls" in jsonData:        
        file_xls = jsonData['file_xls'] 
    if "file_json" in jsonData:        
        file_json = jsonData['file_json'] 
    resultData = save_importProduct(company_id,file_xls,file_json,current_user)
    return resultData