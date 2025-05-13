from flask import Flask, request,current_app
from flask_cors import CORS
from decorators import add_log
from helper.responses import bad_request
from controller.privateController import c_login
from flask import Blueprint

auth_bp = Blueprint('auth_bp', __name__)
    
@auth_bp.route('/login', methods=['POST'])
@add_log()
def auth_login():
    postData = request.get_json()
    resultData = c_login(postData)
    return resultData