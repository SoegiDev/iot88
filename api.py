from flask import Flask, request,current_app
from flask_cors import CORS
from auth import auth_bp
from api_esl import esl_bp
from create_token import createToken_bp
from api_iot import iot_bp
from api_web import web_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'KEEP_IT_A_SECRET'
CORS(app, resources={ r'/*': {'origins': "*"}}, supports_credentials=True)

app.register_blueprint(auth_bp,url_prefix='/api')
app.register_blueprint(esl_bp,url_prefix='/api/esl')
app.register_blueprint(iot_bp,url_prefix='/api/iot')
app.register_blueprint(web_bp,url_prefix='/api/web')
app.register_blueprint(createToken_bp,url_prefix='/api')

@app.route("/")
def hello_world():
    return "<p>IOT BACKEND</p>"