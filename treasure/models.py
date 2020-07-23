from treasure import db ,login_manager
from flask_login import LoginManager,UserMixin,login_user,current_user,logout_user

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100),nullable=False,unique=True) 
    password=db.Column(db.String(100),nullable=False)
    score=db.Column(db.Integer,default=0)

    def __repr__(self):
        return f"User('{self.username},{self.score}')" 

class Questions(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    quest=db.Column(db.Text, nullable=False)
    answer=db.Column(db.Text , nullable=False)
    
    def __repr__(self):
        return f"Questions('{self.quest},{self.answer}')" 