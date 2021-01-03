from flask_login import UserMixin
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import datetime

from files.setup import app

db = SQLAlchemy(app)
#TIER ONE DATABASE
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    #information
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phoneNumber = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    lists = db.relationship("List", backref="user", lazy=True)
    days = db.relationship("Day", backref="user", lazy=True)
    posts = db.relationship("Post", backref="user", lazy=True)
    subposts = db.relationship("SubPost", backref="user", lazy=True)

    #return
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class List(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  uuid = db.Column(db.String(50), unique=True)
  name = db.Column(db.String(500), nullable=False)
  goalType = db.Column(db.String(10), nullable=True)
  checked = db.Column(db.Boolean, nullable=True, default=False)
  checkedDay = db.Column(db.Date, nullable=True)

  user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

  def __repr__(self):
    return f"User('{self.name}', '{self.goalType}')"

class Day(db.Model):
  id = db.Column(db.Integer, primary_key=True)

  day = db.Column(db.Date, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)

  uuid = db.Column(db.String(50), unique=True)
  title = db.Column(db.String(500), nullable=False)
  post = db.Column(db.String, nullable=False)
  goalType = db.Column(db.String(10), nullable=False)

  user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

  subposts = db.relationship("SubPost", backref="post", lazy=True)

  def __repr__(self):
        return f"Post('{self.title}', '{self.goalType}')"
class SubPost(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  subpost = db.Column(db.String(1000), nullable=False)
  username = db.Column(db.String(20), nullable=False)

  user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
  post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)

db.create_all()