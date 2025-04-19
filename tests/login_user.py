"""System module."""
import json
import requests
BASE_URL = "http://127.0.0.1:8080/"
def login() :
    """Doc String"""
    path = "login"
    mimetype = 'application/json'
    username = 'mistersoegi'
    password= 'pass12345!'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'username': username,
        'password': password
    }
    response = requests.post(BASE_URL+path,data=json.dumps(data), headers=headers,timeout=10)
    
    assert response.status_code == 200