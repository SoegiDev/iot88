from flask import request
from decorators import add_log
from helper.responses import bad_request
from flask import Blueprint
from decorators import add_log,token_required
from controller.IOTController import d_change,d_device_get_by_id,d_device_get_by_user,d_push_active,d_push_notif
iot_bp = Blueprint('iot_bp', __name__)
    
@iot_bp.route("/get", methods=['GET'])
@token_required
@add_log()
def iot_get(current_user):
    id = None
    get_device = None
    if request.args.get("id"):
        id = request.args.get("id", "")
        id = id
    if current_user['role'] == "device_IOT":    
        get_device = d_device_get_by_id(current_user['id'])
        return get_device
    if current_user['role'] == "admin" or current_user['role'] == "superadmin":
        get_device = d_device_get_by_id(id)
        return get_device
    if current_user['role'] == "user":
        get_device = d_device_get_by_user(current_user,id)
        return get_device
    else:
        return bad_request("Your request Rejected",400)

@iot_bp.route("/push_active", methods=['GET'])
@token_required
@add_log()
def iot_push_active(current_user):
    returnValue = d_push_active(current_user)
    return returnValue


@iot_bp.route("/push_notify", methods=['POST'])
@token_required
@add_log()
def iot_push_notify(current_user):
    if(current_user['role'] != "device_IOT"):
        return bad_request("Your Request Rejected",401)
    dataPush = request.get_json()
    returnValue = d_push_notif(dataPush,current_user)
    return returnValue

@iot_bp.route('/change_iot', methods=['POST'])
@token_required
@add_log()
def iot_change_device(current_user):
    y = request.get_json()
    updated = d_change(y)
    return updated