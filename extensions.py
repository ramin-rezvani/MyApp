from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
loginmanager = LoginManager()
loginmanager.login_view = 'auth.Login'

@loginmanager.user_loader
def user_loader(user_id):
    from models import User
    return User.query.get(user_id)