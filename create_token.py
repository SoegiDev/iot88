from flask import request,current_app
from helper.responses import bad_request
from controller.IOTController import d_identity_token
from controller.ESLController import e_identity_token
from flask import Blueprint

createToken_bp = Blueprint('createtoken_bp', __name__)

@createToken_bp.route("/create_token",methods=['POST'])
def create_token():
    post = request.get_json()
    type = post['type']
    if(type == "device_IOT"):
        key = post['key']
        getData = d_identity_token(current_app,key)
        return getData
    if(type == "device_ESL"):
        key = post['key']
        getData = e_identity_token(current_app,key)
        return getData
    else:
        return bad_request("Your request Rejected",400)