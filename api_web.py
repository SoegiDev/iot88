from flask import Flask, request,current_app
from flask_cors import CORS
from decorators import add_log,token_required
from helper.responses import bad_request
from controller.WebController import create_esl,get_profile,push_change_sensor
from flask import Blueprint

web_bp = Blueprint('web_bp', __name__)
    
@web_bp.route('/esl_register', methods=['POST'])
@token_required
@add_log()
def esl_register(current_user):
    y = request.get_json()
    l_device = create_esl(y,current_user)
    return l_device

@web_bp.route('/get_profile', methods=['GET'])
@token_required
@add_log()
def user_get_profile(current_user):
    profile = get_profile(current_user)
    return profile

@web_bp.route('/iot_change_sensor', methods=['POST'])
@token_required
@add_log()
def create_change_device_sensor(current_user):
    y = request.get_json()
    device = {}
    device = {"id": y['id']}
    sensor = {}
    sensor = {"name": y['name'], "description": y['description'],
              "active": y['active'],
              "threshold": y['threshold']}
    l_device = push_change_sensor(device, sensor)
    return l_device