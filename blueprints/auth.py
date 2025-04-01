from flask import Blueprint
from controller.auth import AuthController

bp = Blueprint('auth', __name__)
auth = AuthController()

bp.add_url_rule('/signup', 'SignUp', auth.SignUp, methods=['GET', 'POST'])
bp.add_url_rule('/login', 'Login', auth.Login, methods=['GET', 'POST'])
bp.add_url_rule('/logout', 'Logout', auth.Logout, methods=['POST'])