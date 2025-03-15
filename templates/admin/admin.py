from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import app, db  # وارد کردن app و db از extensions
from models import User
from forms import ChangePasswordForm, EditProfileForm
from werkzeug.utils import secure_filename
from PIL import Image


class AdminController:
 def __init__(self):
    self.register_routes()
 def register_routes(self):
    # تعریف مسیرها با استفاده از add_url_rule
    app.add_url_rule("/admin", "index", self.index, methods=['GET'])
    #app.add_url_rule("/panel/info", "Information", self.Information, methods=['GET'])
    #app.add_url_rule("/panel", "Panel", self.Panel, methods=['GET'])
    #app.add_url_rule("/panel/changepassword", "ChangePassword", self.ChangePassword, methods=['GET', 'POST'])
    #app.add_url_rule("/panel/editprofile", "EditProfile", self.EditProfile, methods=['GET', 'POST'])
    #app.add_url_rule("/panel/upload", "UploadAvatar", self.UploadAvatar, methods=['GET', 'POST'])

 @login_required
 def index(self):
    if not current_user.admin:
        return redirect(url_for('panel'))
    return render_template('/admin/index.html')