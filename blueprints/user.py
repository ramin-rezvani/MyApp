from flask import Blueprint
from controller.user import UserController

bp = Blueprint('user', __name__, url_prefix='/panel')
user = UserController()

bp.add_url_rule('/info', 'Information', user.Information, methods=['GET'])
bp.add_url_rule('', 'Panel', user.Panel, methods=['GET'])
bp.add_url_rule('/changepassword', 'ChangePassword', user.ChangePassword, methods=['GET', 'POST'])
bp.add_url_rule('/editprofile', 'EditProfile', user.EditProfile, methods=['GET', 'POST'])
bp.add_url_rule('/upload', 'UploadAvatar', user.UploadAvatar, methods=['GET', 'POST'])