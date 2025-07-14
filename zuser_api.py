from flask import request
from flask_cors import CORS
from decorators import add_log,token_required
from controller.ZUserController import user_create,user_change,\
    user_list_search,user_activate,user_delete,user_show,user_addCompany,user_addstore
from controller.ZAuthController import user_to_authRegister
from flask import Blueprint

zUserBp = Blueprint('zUserBp', __name__)

@zUserBp.route('/create', methods=['POST'])
@token_required
@add_log()
def uAdd(current_user):
    postData = request.get_json()
    resultData = user_create(postData,current_user)
    return resultData

@zUserBp.route('/show', methods=['POST'])
@token_required
@add_log()
def ushow(current_user):
    postData = request.get_json()
    resultData = user_show(postData,current_user)
    return resultData

@zUserBp.route('/change', methods=['POST'])
@token_required
@add_log()
def uchange(current_user):
    postData = request.get_json()
    resultData = user_change(postData,current_user)
    return resultData

@zUserBp.route('/activate', methods=['POST'])
@token_required
@add_log()
def uactivate(current_user):
    postData = request.get_json()
    resultData = user_activate(postData,current_user)
    return resultData

@zUserBp.route('/delete', methods=['POST'])
@token_required
@add_log()
def udelete(current_user):
    postData = request.get_json()
    resultData = user_delete(postData,current_user)
    return resultData

@zUserBp.route('/list_search', methods=['POST'])
@token_required
@add_log()
def ulist_search(current_user):
    query = request.args.get('q')
    page = request.args.get('p')
    jsonData = request.get_json()
    company_id = None
    if len(jsonData) > 0:
        print("Json ada")
        company_id = jsonData['company_id'] if "company_id" in jsonData else None
    else:
        print("Json Tidak ada")
    post_data = {"query":query,"page":page,"company_id":company_id}
    resultData = user_list_search(post_data,current_user)
    return resultData

@zUserBp.route('/export-to-auth', methods=['POST'])
@token_required
@add_log()
def uexporttoauth(current_user):
    postData = request.get_json()
    resultData = user_to_authRegister(postData,current_user)
    return resultData

@zUserBp.route('/add_company', methods=['POST'])
@token_required
@add_log()
def uaddcompany(current_user):
    postData = request.get_json()
    resultData = user_addCompany(postData,current_user)
    return resultData

@zUserBp.route('/add_store', methods=['POST'])
@token_required
@add_log()
def uaddstore(current_user):
    postData = request.get_json()
    resultData = user_addstore(postData,current_user)
    return resultData
