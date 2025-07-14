from flask import request
from flask_cors import CORS
from decorators import add_log,token_required
from controller.ZDashboardController import team_dashboard
from flask import Blueprint

zDashBp = Blueprint('zDashBp', __name__)

@zDashBp.route('/dash_team', methods=['GET'])
@token_required
@add_log()
def dashTeam(current_user):
    resultData = team_dashboard(current_user)
    return resultData
