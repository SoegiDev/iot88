from flask import Flask, request
from decorators import add_log
from controller.AdminController import c_register_device_admin, \
    c_login_admin, c_get_device_admin, \
    c_register_admin, c_change_password_admin, \
    c_change_device_admin, c_change_device_sensor_admin
from controller.UserController import c_register, c_login, c_change_password, \
    c_register_device, c_change_device, c_change_device_sensor, c_get_device

app = Flask(__name__)


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
@add_log()
def create_change_device_admin():
    y = request.get_json()
    l_device = c_change_device_admin(y)
    return l_device


@app.route('/admin_change_sensor_device', methods=['POST'])
@add_log()
def create_change_device_sensor_admin():
    y = request.get_json()
    device = {}
    device = {"id": y['id']}
    sensor = {}
    sensor = {"name": y['name'], "description": y['description'],
              "active": y['active'], "threshold": y['threshold']}
    l_device = c_change_device_sensor_admin(device, sensor)
    return l_device


@app.route('/admin_get_device', methods=['GET'])
@add_log()
def create_get_device_admin():
    id = None
    if request.args.get("id"):
        id = request.args.get("id", "")
        id = id
    get_deviceList = c_get_device_admin(id)
    return get_deviceList


# ======================USER============================= #
@app.route('/register', methods=['POST'])
@add_log()
def create_register():
    y = request.get_json()
    login = c_register(y)
    return login


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


if __name__ == '__main__':
    app = Flask(__name__)
