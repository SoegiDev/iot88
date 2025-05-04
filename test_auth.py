from flask import Flask, request
from flask_cors import CORS
from decorators import add_log,token_required
from controller.AdminController import c_register_device_admin, \
    c_login_admin, c_get_device_admin, \
    c_register_admin, c_change_password_admin, \
    c_change_device_admin, c_change_device_sensor_admin, \
    c_register_device_sensor_admin,c_profile_admin, \
    c_push_notif_sensor,c_register_esl_admin,c_change_esl_admin,c_get_notif_admin, \
        c_get_esl_admin
from controller.UserController import c_register, c_login, c_change_password, \
    c_register_device, c_change_device, c_change_device_sensor, c_get_device

app = Flask(__name__)
app.config['SECRET_KEY'] = 'KEEP_IT_A_SECRET'
CORS(app, resources={ r'/*': {'origins': "*"}}, supports_credentials=True)
@app.route("/")
def hello_world():
    return "<p>IOT BACKEND</p>"


@app.route('/admin_register', methods=['POST'])
@add_log()
def create_admin_register():
    y = request.get_json()
    login = c_register_admin(y)
    return login


@app.route('/admin_login', methods=['POST'])
@add_log()
def create_admin_login():
    y = request.get_json()
    login = c_login_admin(y)
    return login

@app.route('/admin_get_profile', methods=['GET'])
@token_required
@add_log()
def create_admin_profile(current_user):
    profile = c_profile_admin(current_user)
    return profile


@app.route('/admin_change_password', methods=['POST'])
@add_log()
def create_admin_change_password():
    y = request.get_json()
    change = c_change_password_admin(y)
    return change


@app.route('/admin_register_device', methods=['POST'])
@add_log()
def create_register_device_admin():
    y = request.get_json()
    l_device = c_register_device_admin(y)
    return l_device


@app.route('/admin_change_device', methods=['POST'])
@token_required
@add_log()
def create_change_device_admin(current_user):
    y = request.get_json()
    l_device = c_change_device_admin(y)
    return l_device

@app.route('/admin_register_sensor_device', methods=['POST'])
@token_required
@add_log()
def create_register_device_sensor_admin(current_user):
    y = request.get_json()
    device = {}
    device = {"id": y['id']}
    sensor = {}
    sensor = {"name": y['name'], "description": y['description'],
              "active": y['active'], "threshold": y['threshold']}
    l_device = c_register_device_sensor_admin(device, sensor)
    return l_device


@app.route('/admin_change_sensor_device', methods=['POST'])
@token_required
@add_log()
def create_change_device_sensor_admin(current_user):
    y = request.get_json()
    device = {}
    device = {"id": y['id']}
    sensor = {}
    sensor = {"name": y['name'], "description": y['description'],
              "active": y['active'], "threshold": y['threshold']}
    l_device = c_change_device_sensor_admin(device, sensor)
    return l_device


@app.route('/admin_get_device', methods=['GET'])
@token_required
@add_log()
def create_get_device_admin(curent_user):
    id = None
    if request.args.get("id"):
        id = request.args.get("id", "")
        id = id
    get_deviceList = c_get_device_admin(id)
    return get_deviceList


@app.route('/admin_get_device_noauth', methods=['GET'])
@add_log()
def create_get_device_admin_noauth():
    id = None
    if request.args.get("id"):
        id = request.args.get("id", "")
        id = id
    get_deviceList = c_get_device_admin(id)
    return get_deviceList

@app.route('/admin_get_esl_noauth', methods=['GET'])
@add_log()
def create_get_esl_admin_noauth():
    id = None
    if request.args.get("id"):
        id = request.args.get("id", "")
        id = id
    get_deviceList = c_get_esl_admin(id)
    return get_deviceList

@app.route('/admin_push_sensor', methods=['POST'])
@add_log()
def create_push_sensor():
    y = request.get_json()
    get_deviceList = c_push_notif_sensor(y)
    return get_deviceList


@app.route('/admin_register_esl', methods=['POST'])
@token_required
@add_log()
def create_register_esl_admin(current_user):
    y = request.get_json()
    l_device = c_register_esl_admin(y,current_user)
    return l_device

@app.route('/admin_get_notif', methods=['GET'])
@token_required
@add_log()
def create_get_notif_admin(current_user):
    id = None
    if request.args.get("id"):
        id = request.args.get("id", "")
        id = id
    get_notif = c_get_notif_admin(id,current_user)
    return get_notif
# ======================USER============================= #
@app.route('/register', methods=['POST'])
@add_log()
def create_register():
    y = request.get_json()
    register = c_register(y)
    return register


@app.route('/login', methods=['POST'])
@add_log()
def create_login():
    y = request.get_json()
    login = c_login(y)
    return login


@app.route('/change_password', methods=['POST'])
@add_log()
def create_change_password():
    y = request.get_json()
    change = c_change_password(y)
    return change


@app.route('/register_device', methods=['POST'])
@add_log()
def create_register_device():
    y = request.get_json()
    change = c_register_device(y)
    return change


@app.route('/change_device', methods=['POST'])
@add_log()
def create_change_device():
    y = request.get_json()
    l_device = c_change_device(y)
    return l_device


@app.route('/change_sensor_device', methods=['POST'])
@add_log()
def create_change_device_sensor():
    y = request.get_json()
    device = {}
    device = {"id": y['id']}
    sensor = {}
    sensor = {"name": y['name'], "description": y['description'],
              "active": y['active'],
              "threshold": y['threshold']}
    l_device = c_change_device_sensor(device, sensor)
    return l_device


@app.route('/get_device', methods=['GET'])
@add_log()
def create_get_device():
    id = None
    if request.args.get("id"):
        id = request.args.get("id", "")
        id = id
    get_deviceList = c_get_device(id)
    return get_deviceList

@app.route('/admin_change_esl', methods=['POST'])
@token_required
@add_log()
def create_change_esl_admin(current_user):
    y = request.get_json()
    l_device = c_change_esl_admin(y)
    return l_device

if __name__ == '__main__':
    app = Flask(__name__)
