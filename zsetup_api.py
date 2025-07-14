from flask import request
from flask_cors import CORS
from decorators import add_log,token_required
from controller.ZSetupController import setup_create,setup_change,\
    setup_list_search,setup_show
from flask import Blueprint

zSetupBp = Blueprint('zSetupBp', __name__)

@zSetupBp.route('/create', methods=['POST'])
@token_required
@add_log()
def uAdd(current_user):
    postData = request.get_json()
    resultData = setup_create(postData,current_user)
    return resultData

@zSetupBp.route('/show', methods=['POST'])
@token_required
@add_log()
def ushow(current_user):
    postData = request.get_json()
    resultData = setup_show(postData,current_user)
    return resultData

@zSetupBp.route('/change', methods=['POST'])
@token_required
@add_log()
def uchange(current_user):
    postData = request.get_json()
    resultData = setup_change(postData,current_user)
    return resultData

@zSetupBp.route('/list_search', methods=['POST'])
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
    resultData = setup_list_search(post_data,current_user)
    return resultData