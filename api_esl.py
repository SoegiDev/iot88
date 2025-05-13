from flask import request
from decorators import add_log
from helper.responses import bad_request
from flask import Blueprint
from controller.ESLController import e_change,e_device_get,e_device_getByUser,e_identity_token,e_push_notif,e_push_active
from decorators import add_log,token_required

esl_bp = Blueprint('esl_bp', __name__)
    

@esl_bp.route("/get", methods=['GET'])
@token_required
@add_log()
def esl_get(current_user):
    id = None
    get_device = None
    if request.args.get("id"):
        id = request.args.get("id", "")
        id = id
    if current_user['role'] == "device_ESL":    
        get_device = e_device_get(current_user['id'])
        return get_device
    if current_user['role'] == "admin" or current_user['role']=="superadmin":
        get_device = e_device_get(id)
        return get_device
    if current_user['role'] == "user":
        get_device = e_device_getByUser(current_user,id)
        return get_device
    else:
        return bad_request("Your request Rejected",400)
    
@esl_bp.route("/push_active", methods=['GET'])
@token_required
@add_log()
def esl_push_active(current_user):
    returnValue = e_push_active(current_user)
    return returnValue


@esl_bp.route("/push_notify", methods=['POST'])
@token_required
@add_log()
def esl_push_notify(current_user):
    if(current_user['role'] != "device_ESL"):
        return bad_request("Your Request Rejected",401)
    dataPush = request.get_json()
    returnValue = e_push_notif(dataPush,current_user)
    return returnValue

@esl_bp.route('/change_esl', methods=['POST'])
@token_required
@add_log()
def esl_change_device(current_user):
    y = request.get_json()
    updated = e_change(y)
    return updated