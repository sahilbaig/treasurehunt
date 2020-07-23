from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin,login_user,current_user,logout_user
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os

app= Flask(__name__)
app.config['SECRET_KEY']= 'MEOWMEOW'
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
admin = Admin(app)
login_manager=LoginManager(app)

from treasure import routes

from treasure.models import User,Questions

class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.username == '#@234ij':
            return True

admin.add_view(MyModelView(User,db.session))
admin.add_view(MyModelView(Questions,db.session))



