from flask import request
from flask_cors import CORS
from decorators import add_log,token_required
from controller.ZOutletController import outlet_create,outlet_list_search,outlet_show,outlet_change
from flask import Blueprint

zOutletBp = Blueprint('zOutletBp', __name__)

@zOutletBp.route('/create', methods=['POST'])
@token_required
@add_log()
def outletCreate(current_user):
    postData = request.get_json()
    resultData = outlet_create(postData,current_user)
    return resultData

@zOutletBp.route('/list_search', methods=['POST'])
@token_required
@add_log()
def outletList_search(current_user):
    query = request.args.get('q')
    page = request.args.get('p')
    jsonData = request.get_json()
    store_id = jsonData['store_id'] if "store_id" in jsonData else None
    company_id = jsonData['company_id'] if "company_id" in jsonData else None
    post_data = {"query":query,"page":page,"company_id":company_id,"store_id":store_id}
    content = outlet_list_search(post_data,current_user)
    return content

@zOutletBp.route('/show', methods=['POST'])
@token_required
@add_log()
def outletShow(current_user):
    jsonData = request.get_json()
    resultData = outlet_show(jsonData,current_user)
    return resultData

@zOutletBp.route('/change', methods=['POST'])
@token_required
@add_log()
def outletChange(current_user):
    jsonData = request.get_json()
    resultData = outlet_change(jsonData,current_user)
    return resultData

@zOutletBp.route('/activate', methods=['POST'])
@token_required
@add_log()
def outletActivate(current_user):
    jsonData = request.get_json()
    resultData = outlet_change(jsonData,current_user)
    return resultData

@zOutletBp.route('/delete', methods=['POST'])
@token_required
@add_log()
def outletDelete(current_user):
    jsonData = request.get_json()
    resultData = outlet_change(jsonData,current_user)
    return resultData