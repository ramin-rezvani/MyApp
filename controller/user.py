from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models import User
from forms import ChangePasswordForm, EditProfileForm
from werkzeug.utils import secure_filename
from PIL import Image
import os

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class UserController:
    @login_required
    def Information(self):
        return render_template('user/info.html', user=current_user)

    @login_required
    def Panel(self):
        return render_template('user/panel.html', user=current_user)

    @login_required
    def ChangePassword(self):
        form = ChangePasswordForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                old_password = request.form.get('old_password')
                new_password = request.form.get('new_password')
                if check_password_hash(current_user.password, old_password):
                    current_user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
                    db.session.commit()
                    flash('Password changed successfully!', 'success')
                    return redirect(url_for('user.Panel'))
                else:
                    flash('Old password is incorrect', 'error')
                    return redirect(url_for('user.ChangePassword'))
        return render_template('user/change_password.html', form=form)

    @login_required
    def EditProfile(self):
        form = EditProfileForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                name = request.form.get('name')
                email = request.form.get('email')
                current_user.name = name
                current_user.email = email
                db.session.commit()
                flash('Profile updated successfully!', 'success')
                return redirect(url_for('user.Panel'))
        return render_template('user/edit_profile.html', form=form, user=current_user)

    @login_required
    def UploadAvatar(self):
        if request.method == 'POST':
            if 'avatar' not in request.files:
                flash('No file part', 'error')
                return redirect(request.url)
            file = request.files['avatar']
            if file.filename == '':
                flash('No selected file', 'error')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                img = Image.open(file)
                img = img.resize((100, 100))
                img.save(file_path)
                current_user.avatar = f'/uploads/{filename}'
                db.session.commit()
                flash('Avatar uploaded successfully!', 'success')
                return redirect(url_for('user.Panel'))
        return render_template('user/Avatar.html')