from flask import request,current_app
from decorators import add_log
from helper.responses import bad_request
from flask import Blueprint
from decorators import add_log,token_required
from controller.ZDeviceController import deviceHome,device_esl_create,esl_get_token,\
    esl_sync,esl_ListSearch,esl_product,esl_content,esl_show,esl_change

zDevicebp = Blueprint('zDevicebp', __name__)

@zDevicebp.route('/home', methods=['GET'])
@add_log()
def d_home():
    result = deviceHome()
    return result

@zDevicebp.route('/esl/register', methods=['POST'])
@add_log()
def esl_register():
    post = request.get_json()
    result = device_esl_create(post,current_app)
    return result

@zDevicebp.route('/esl/token', methods=['POST'])
@add_log()
def esl_token():
    post = request.get_json()
    result = esl_get_token(post,current_app)
    return result

@zDevicebp.route('/esl/sync', methods=['POST'])
@token_required
@add_log()
def esl_post_sync(current_user):
    post = request.get_json()
    result = esl_sync(post,current_user)
    return result

@zDevicebp.route('/esl/product', methods=['GET'])
@token_required
@add_log()
def esl_get_product(current_user):
    result = esl_product(current_user)
    return result

@zDevicebp.route('/esl/content', methods=['GET'])
@token_required
@add_log()
def esl_get_content(current_user):
    result = esl_content(current_user)
    return result

@zDevicebp.route('/esl/show', methods=['POST'])
@token_required
@add_log()
def eslShow(current_user):
    jsonData = request.get_json()
    resultData = esl_show(jsonData,current_user)
    return resultData

@zDevicebp.route('/esl/change', methods=['POST'])
@token_required
@add_log()
def eslChange(current_user):
    jsonData = request.get_json()
    resultData = esl_change(jsonData,current_user)
    return resultData

@zDevicebp.route('/esl/list_search', methods=['POST'])
@token_required
@add_log()
def esl_list_search(current_user):
    query = request.args.get('q')
    page = request.args.get('p')
    jsonData = request.get_json()
    store_id = jsonData['store_id'] if "store_id" in jsonData else None
    company_id = jsonData['company_id'] if "company_id" in jsonData else None
    post_data = {"query":query,"page":page,"client_owner_id":company_id,"client_store_id":store_id}
    content = esl_ListSearch(post_data,current_user)
    return content