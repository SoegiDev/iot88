from flask import request
from flask_cors import CORS
from decorators import add_log,token_required
from controller.ZCompanyController import company_create,company_list_search,\
    company_show,company_change,company_activate,company_delete
from flask import Blueprint

zCompBp = Blueprint('zComBp', __name__)

@zCompBp.route('/create', methods=['POST'])
@token_required
@add_log()
def comCreate(current_user):
    postData = request.get_json()
    resultData = company_create(postData,current_user)
    return resultData

@zCompBp.route('/list_search', methods=['POST'])
@token_required
@add_log()
def comListSearch(current_user):
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
    resultData = company_list_search(post_data,current_user)
    return resultData

@zCompBp.route('/show', methods=['POST'])
@token_required
@add_log()
def comShow(current_user):
    jsonData = request.get_json()
    resultData = company_show(jsonData,current_user)
    return resultData

@zCompBp.route('/change', methods=['POST'])
@token_required
@add_log()
def comChange(current_user):
    jsonData = request.get_json()
    resultData = company_change(jsonData,current_user)
    return resultData

@zCompBp.route('/activate', methods=['POST'])
@token_required
@add_log()
def comActivate(current_user):
    jsonData = request.get_json()
    resultData = company_activate(jsonData,current_user)
    return resultData

@zCompBp.route('/delete', methods=['POST'])
@token_required
@add_log()
def comDelete(current_user):
    jsonData = request.get_json()
    resultData = company_delete(jsonData,current_user)
    return resultData