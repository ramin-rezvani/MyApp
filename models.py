from extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask_login import UserMixin



class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(50))
    email= db.Column(db.String(150))
    password= db.Column(db.String)
    avatar=db.Column(db.String,default='/img/avatar.png')
    admin= db.Column(db.Boolean ,default=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    
    
    def __init__(self, name, email,password) -> None:
      self.name = name
      self.email = email
      self.password =generate_password_hash(password)
      