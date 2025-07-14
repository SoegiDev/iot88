from flask import request
from flask_cors import CORS
from decorators import add_log,token_required
from controller.ZProductController import product_create,product_list_search,product_show,product_change
from flask import Blueprint

zProductBp = Blueprint('zProductBp', __name__)

@zProductBp.route('/create', methods=['POST'])
@token_required
@add_log()
def productCreate(current_user):
    postData = request.get_json()
    resultData = product_create(postData,current_user)
    return resultData

@zProductBp.route('/list_search', methods=['POST'])
@token_required
@add_log()
def productList_search(current_user):
    query = request.args.get('q')
    page = request.args.get('p')
    jsonData = request.get_json()
    store_id = jsonData['store_id'] if "store_id" in jsonData else None
    company_id = jsonData['company_id'] if "company_id" in jsonData else None
    post_data = {"query":query,"page":page,"company_id":company_id,"store_id":store_id}
    content = product_list_search(post_data,current_user)
    return content

@zProductBp.route('/show', methods=['POST'])
@token_required
@add_log()
def productShow(current_user):
    jsonData = request.get_json()
    resultData = product_show(jsonData,current_user)
    return resultData

@zProductBp.route('/change', methods=['POST'])
@token_required
@add_log()
def productChange(current_user):
    jsonData = request.get_json()
    resultData = product_change(jsonData,current_user)
    return resultData

@zProductBp.route('/activate', methods=['POST'])
@token_required
@add_log()
def productActivate(current_user):
    jsonData = request.get_json()
    resultData = product_change(jsonData,current_user)
    return resultData

@zProductBp.route('/delete', methods=['POST'])
@token_required
@add_log()
def productDelete(current_user):
    jsonData = request.get_json()
    resultData = product_change(jsonData,current_user)
    return resultData