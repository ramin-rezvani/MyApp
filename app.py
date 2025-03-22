from flask import Flask, render_template, request, redirect, url_for, flash, abort, session
from extensions import db,app
import secrets
import os
from flask_login import LoginManager,login_user,logout_user,current_user,logout_user,login_required
from controller import authentication,main,userPanel,adminpanel
from models import User


app.secret_key = secrets.token_hex(32)


uplode_dir= os.path.curdir + '/static/uploads/'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'shop.db')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
#google recaptcha config
app.config['RECAPTCHA_PUBLIC_KEY']='6LeTG-4qAAAAAFeKMuo0SJHrXkJepmHtLD5MqFvi'#public key
app.config['RECAPTCHA_PRIVATE_KEY']='6LeTG-4qAAAAAAcnjWJqkTgmygBE74rPH3LW94OY'#private key

db.init_app(app)

loginmanager=LoginManager(app)
loginmanager.login_view='Login'

#return info user
@loginmanager.user_loader
def user_loader(User_id):
    return User.query.get(User_id)


#main Route
app.add_url_rule('/',main,main.Main)
app.add_url_rule('/<string:slug>','Single',main.Single)
#authentication Route

app.add_url_rule("/signup","SignUp",authentication.SignUp,methods=['get','post'])
app.add_url_rule("/login","Login",authentication.Login,methods=['get','post'])
app.add_url_rule("/logout","Logout",authentication.Logout,methods=['post'])


#user Route
app.add_url_rule("/panel/info","Information",userPanel.Information)
app.add_url_rule("/panel","Panel",userPanel.Panel)
app.add_url_rule("/panel/changepassword","ChangePassword",userPanel.ChangePassword,methods=['get','post'])
app.add_url_rule("/panel/editprofile","EditProfile",userPanel.EditProfile,methods=['get','post'])
app.add_url_rule("/panel/upload","UploadAvatar",userPanel.UploadAvatar,methods=['get','post'])


#ADMIN ROUTE
app.add_url_rule("/admin","index",adminpanel.index)
app.add_url_rule("/admin/info", "AdminInformation", adminpanel.AdminInformation)
#app.add_url_rule("/panel", "Panel", self.Panel, methods=['GET'])
app.add_url_rule("/admin/changepassword","AdminChangePassword",adminpanel.AdminChangePassword,methods=['get','post'])
app.add_url_rule("/admin/editprofile","AdminEditProfile",adminpanel.AdminEditProfile,methods=['get','post'])
app.add_url_rule("/admin/upload","AdminUploadAvatar",adminpanel.AdminUploadAvatar,methods=['get','post'])
app.add_url_rule("/admin/user","GetUserList",adminpanel.GetUserList,methods=['GET','POST'])
app.add_url_rule("/admin/newuser","AddNewUser",adminpanel.AddNewUser,methods=['GET','POST'])

#course route
app.add_url_rule("/admin/episode/new","AddNewEpisode",adminpanel.AddNewEpisode,methods=['Get','POST'])
app.add_url_rule("/admin/course/new","AddNewCourse",adminpanel.AddNewCourse,methods=['Get','POST'])
app.add_url_rule("/admin/course","GetCourseList",adminpanel.GetCourseList,methods=['Get','POST'])
app.add_url_rule("/admin/episode","GetEpisode",adminpanel.GetEpisode,methods=['Get','POST'])
app.add_url_rule("/admin/episode/edit/<int:course_id>'","EditEpisode",adminpanel.EditEpisode,methods=['Get','POST'])



with app.app_context():
 db.create_all()
 print('Database connection established....')

if __name__ == '__main__':
    app.run(debug=True)