from flask import render_template, url_for, flash, redirect, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from flask_socketio import socketio, join_room, leave_room
from datetime import datetime
import uuid, json

from files.setup import *
from files.databases import *
from files.forms import *
from files.functions import *

@app.route('/listadd', methods=['POST'])
def listAdd():
  uuidStr = str(uuid.uuid4())
  # updating
  if request.form.get("new") == "false":
    listElement = List.query.filter_by(uuid=request.form.get("uuid")).first()
    if listElement.user_id == current_user.id and checkGoalList(request.form.get("goalType")):
      print(request.form.get("name"))
      listElement.name = request.form.get("name")
      listElement.goalType = request.form.get("goalType")
      if request.form.get("checked") == "true":
        listElement.checked = True
        listElement.checkedDay = datetime.datetime.now()
        dayMake = True
        for listElement in current_user.lists:
          if listElement.checked == False:
            dayMake = False
        if dayMake:
          day = Day(day=datetime.datetime.now(), user_id=current_user.id)
          db.session.add(day)
      db.session.commit()
      return jsonify("success")
  # new ones
  else:
    if request.form.get("goalType") == "None":
      listElement = List(name=request.form.get("name"), user_id=current_user.id, uuid=request.form.get("uuid"))
    elif request.form.get("goalType") != "None" and checkGoalList(request.form.get("goalType")):
      listElement = List(name=request.form.get("name"), goalType=request.form.get("goalType"), uuid=request.form.get("uuid"), user_id=current_user.id)
    else:
      print("creating failure")
      return jsonify("")
    db.session.add(listElement)
    db.session.commit()
    return jsonify(uuidStr)
  print("updating failure")
  return jsonify("")


@app.route('/addpost', methods=['POST'])
def addpost():
  if checkExists([request.form.get("title"), request.form.get("body"), request.form.get("goalType")]) and checkGoalList(request.form.get("goalType")):
    uuidStr = str(uuid.uuid4())
    post = Post(title=request.form.get("title"), post=request.form.get("body"), goalType=request.form.get("goalType"), uuid=uuidStr, user_id=current_user.id)
    db.session.add(post)
    db.session.commit()
    print(post)
    return jsonify(uuidStr)
  print("failure")
  return jsonify("")

def alertPost(user, subpost, post):
  if len(post.subposts) == 1:
    user = User.query.filter_by(id=user).first()
    message = subpost+" responded to your post! Go check it out at https://newyear.1234567890hihi.repl.co/chat/"+post.uuid+" . "
    client.send_message({
      'from': '16073072184',
      'to': user.phoneNumber,
      'text': message,
    })

@app.route('/addComment', methods=['POST'])
def addComment():
  print([request.form.get("subpost"), request.form.get("postUUID"), request.form.get("sid")])
  if checkExists([request.form.get("subpost"), request.form.get("postUUID"), request.form.get("sid")]):
    post = Post.query.filter_by(uuid=request.form.get("postUUID")).first()
    subpost = SubPost(subpost=request.form.get("subpost"), post_id=post.id, user_id=current_user.id, username=current_user.username)
    db.session.add(subpost)
    db.session.commit()
    data = [subpost.subpost, subpost.username]
    socketio.emit('recieveComment', data, room=request.form.get("postUUID"), skip_sid=request.form.get("sid"), broadcast=True)
    alertPost(post.user_id, current_user.username, post)
    return jsonify(data)
  print("failure")
  return jsonify("")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
