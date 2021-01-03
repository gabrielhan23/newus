from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO
from nexmo import nexmo
from apscheduler.schedulers.background import BackgroundScheduler

#setup 
template_dir = "../templates"
static_dir = "../static"
app = Flask(__name__,template_folder=template_dir)
app.config['SECRET_KEY'] = 'password12345abcde'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
socketio = SocketIO(app, cors_allowed_origins='*')
client = nexmo.Client(key='f511054d', secret='36V6EDkoxlBNfBPw')
scheduler = BackgroundScheduler()
