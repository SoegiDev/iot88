from flask import Flask, request,current_app,render_template
from flask_cors import CORS
from zauth_api import zAuthBp
from controller.ZInitialController import init_auth as initialSuper
from zuser_api import zUserBp
from zcompany_api import zCompBp
from zdash_api import zDashBp
from zoutlet_api import zOutletBp
from zproduct_api import zProductBp
from zsetup_api import zSetupBp
from zimport_api import zImportBp
from zdevice_api import zDevicebp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'KEEP_IT_A_SECRET'
CORS(app, resources={ r'/*': {'origins': "*"}}, supports_credentials=True)

app.register_blueprint(zAuthBp,url_prefix='/auth')
app.register_blueprint(zUserBp,url_prefix='/user')
app.register_blueprint(zOutletBp,url_prefix='/outlet')
app.register_blueprint(zCompBp,url_prefix='/company')
app.register_blueprint(zDashBp,url_prefix='/dashboard')
app.register_blueprint(zProductBp,url_prefix='/product')
app.register_blueprint(zSetupBp,url_prefix='/setup')
app.register_blueprint(zImportBp,url_prefix='/import')
app.register_blueprint(zDevicebp,url_prefix='/device')


@app.route("/")
def hello_world():
    return "<p>IOT BACKEND</p>"

@app.route("/sleep")
def sleep_mode():
    return "<p>SLEEP MODE</p>"

@app.route("/sleepmode")
def sleep_modeOn():
    return "<p>SLEEP MODE ONE</p>"

@app.route("/initial")
def initial_super():
    post_data = {}
    post_data['username'] = "admin_super"
    post_data['password'] = "admin123!"
    post_data['email'] = "admin_super@admin.com"
    post_data['role'] = "superadmin"
    initial_data = initialSuper(post_data)
    return initial_data

@app.route('/template/versi1')
def home():
    return render_template('index.html')