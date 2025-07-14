from flask import request
from flask_cors import CORS
from decorators import add_log,token_required
from controller.ZAuthController import auth_register,auth_login,\
    auth_change_password,auth_list_search,auth_profile,auth_change,\
        auth_show
from flask import Blueprint

zAuthBp = Blueprint('zAuthBp', __name__)

@zAuthBp.route('/register', methods=['POST'])
@add_log()
def aRegister():
    postData = request.get_json()
    resultData = auth_register(postData)
    return resultData

@zAuthBp.route('/login', methods=['POST'])
@add_log()
def alogin():
    postData = request.get_json()
    resultData = auth_login(postData)
    return resultData

@zAuthBp.route('/show', methods=['POST'])
@token_required
@add_log()
def ashow(current_user):
    postData = request.get_json()
    resultData = auth_show(postData,current_user)
    return resultData

@zAuthBp.route('/change_password', methods=['POST'])
@token_required
@add_log()
def achange_password(current_user):
    postData = request.get_json()
    resultData = auth_change_password(postData,current_user)
    return resultData

@zAuthBp.route('/change', methods=['POST'])
@token_required
@add_log()
def achange(current_user):
    postData = request.get_json()
    resultData = auth_change(postData,current_user)
    return resultData

@zAuthBp.route('/list_search', methods=['POST'])
@token_required
@add_log()
def alist_search(current_user):
    query = request.args.get('q')
    page = request.args.get('p')
    jsonData = request.get_json()
    company_id = None
    company_id = jsonData['company_id'] if "company_id" in jsonData else None
    post_data = {"query":query,"page":page,"company_id":company_id}
    resultData = auth_list_search(post_data,current_user)
    return resultData

@zAuthBp.route('/profile', methods=['GET'])
@token_required
#@add_log()
def aprofile(current_user):
    resultData = auth_profile(current_user)
    return resultData