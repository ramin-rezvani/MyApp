from extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from sqlalchemy import Column,Integer,String,Text,DateTime,ForeignKey,event
from slugify import slugify



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String) 
    avatar=db.Column(db.String,default='/uploads/avatar.png')
    admin= db.Column(db.Boolean ,default=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    
    
    def __init__(self, name, email,password) -> None:
      self.name = name
      self.email = email
      self.password= password
      
class Course(db.Model):
  __tablename__='courses'
  id=Column(Integer,primary_key=True)
  title=Column(String)
  slug=Column(String)
  price=Column(String,default=0)
  content=Column(Text)
  image=Column(String,default='/uploads/avatar.png')
  CommentCount=Column(Integer,default=0)
  students=Column(String)
  category_id=Column(Integer,ForeignKey('categories.id'))
  ViewCount=Column(Integer,default=0)
  time=Column(String,default='00:00:00')
  user_id=Column(Integer,ForeignKey('user.id'))
  date_created=db.Column(db.DateTime, default=datetime.now)
  updated_post=Column(db.DateTime,default=datetime.now,onupdate=datetime.now)
  
  def getWriter(self , id):
     return User.query.get(id).name
  
  @staticmethod
  def generate_slug(target,value,oldvalue,initiator):
   if value and(not target.slug and value != oldvalue):
      target.slug=slugify(value)
      
db.event.listen(Course.title,'set',Course.generate_slug)
      
      
class Episode(db.Model):
   __tabelname__='episode'
   id=Column(Integer,primary_key=True)
   course_id=Column(Integer,ForeignKey('courses.id'),nullable=False)
   title=Column(String) 
   type=Column(String) 
   time=Column(String) 
   videoUrl=Column(String)
   body=Column(Text)
   number=Column(Integer)
   viewCount=Column(Integer,default=0)     
   date_created=Column(DateTime, default=datetime.now())
   date_updated=Column(DateTime,default=datetime.now(),onupdate=datetime.now())
   
   def getCourse(self):
      return Course.query.filter_by(id=self.course_id).one()
   
class Category(db.Model):
   __tablename__ = 'categories'
   id = Column(Integer,primary_key=True)
   name = Column(String)
   
class Bascket(db.Model):
   id= Column(Integer,primary_key=True)
   course_id = Column(Integer,ForeignKey('courses.id'),nullable=True)
   user_id = Column(Integer,ForeignKey('user.id'),nullable=True)
    
   def GetCourse(self):
      return Course.query.filter_by(id=self.course_id).first()