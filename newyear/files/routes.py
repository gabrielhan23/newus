from flask import render_template, url_for, flash, redirect, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from flask_socketio import socketio, join_room, leave_room
from datetime import datetime
import uuid, json

from files.setup import *
from files.databases import *
from files.forms import *
from files.functions import *

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
      return redirect(url_for("list"))
    form = LoginForm()
    if form.validate_on_submit():
      user = User.query.filter_by(email=form.email.data).first()
      if user and bcrypt.check_password_hash(user.password, form.password.data):
        login_user(user)
        flash("You have been logged in", "success")
        return redirect(url_for("list"))
    return render_template("login.html", form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
      return redirect(url_for("list"))
    form = RegistrationForm()
    if form.validate_on_submit():
      hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
      user = User(username=form.username.data, email=form.email.data, password=hashed_password, phoneNumber=form.phoneNumber.data)
      db.session.add(user)
      db.session.commit()
      
      login_user(user)
      flash("You have successfuly made an account.", "success")
      return redirect(url_for("list"))
    return render_template("signup.html", form=form)

@app.route('/list', methods=['GET', 'POST'])
@login_required
def list():
    listItems = List.query.filter_by(user=current_user).all()
    print(listItems)
    preUUID = uuid.uuid4()
    today = datetime.datetime.now().strftime("%d")
    # today = datetime.datetime(2020, 1, 1).strftime("%d")
    for listItem in listItems:
      print(listItem.checkedDay)
      if listItem.checkedDay and listItem.checkedDay.strftime("%d")>today:
        print(listItem.checked)
        print(listItem.checkedDay)
        listItem.checked = False
        listItem.checkedDay = None
    return render_template("list.html", goalList=goalList, listItems=listItems, preUUID=preUUID)

@app.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendar():

    days = current_user.days
    
    return render_template("calendar.html", days=days)

@app.route('/charity', methods=['GET', 'POST'])
@login_required
def charity():
    return render_template("charity.html")

@app.route('/post/<topic>', methods=['GET', 'POST'])
@login_required
def post(topic):
    posts = Post.query.filter_by(goalType=topic).all()
    print(posts)
    return render_template("post.html", posts=posts)

@app.route('/chat/<uuid>', methods=['GET', 'POST'])
@login_required
def chat(uuid):
    post = Post.query.filter_by(uuid=uuid).first()
    subposts = post.subposts
    return render_template("chat.html", post=post, subposts=subposts)

def sendModivation():
  users = User.query.all()
  for user in users:
    phoneNumber = user.phoneNumber
    message = getModivation()
    client.send_message({
      'from': '16073072184',
      'to': phoneNumber,
      'text': message,
    })

scheduler.add_job(func=sendModivation, trigger="interval", hours=12)
# scheduler.add_job(func=sendModivation, trigger="interval", seconds=10)
scheduler.start()

@socketio.on('begin_chat')
def begin_chat(data):
  print(data['room'])
  join_room(data['room'])


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
