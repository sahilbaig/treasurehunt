from flask import Flask, render_template, url_for,redirect,flash
from forms import LoginForm, RegistrationForm , Answer
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin,login_user,current_user,logout_user
from flask_bcrypt import Bcrypt

# Flask and Flask-SQLAlchemy initialization here

import os

app= Flask(__name__)
app.config['SECRET_KEY']= 'MEOWMEOW'
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL')
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)

login_manager=LoginManager(app)

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

@app.route("/")
@app.route("/home")
def index():
    return render_template('index.html')

@app.route("/login",methods=['POST','GET'])
def home():
    form=LoginForm()
    if form.validate_on_submit():
        user_check = User.query.filter_by(username=form.username.data).first()
        if user_check and bcrypt.check_password_hash(user_check.password , form.password.data):
            login_user(user_check)
            return redirect(url_for('questions',number=current_user.score+1))
        else:
            return redirect(url_for('home'))
    return render_template('home.html', form=form)

@app.route("/register", methods=['POST','GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pass=bcrypt.generate_password_hash(form.password.data).decode('utf-8') #this part added
        register_user=User(username=form.username.data , password=hash_pass)
        db.session.add(register_user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html', form= form)

@app.route("/question/<int:number>" ,methods=['POST','GET'])
def questions(number):
    if number==0:
        return redirect(url_for('questions',number=1))
    if (number>4):
        return redirect(url_for('leader'))
    if (number-1)!=current_user.score:
        return render_template('cheat.html')
    else:
        show= Questions.query.filter_by(id=number).first()
        form=Answer()
        image_file = url_for('static', filename=str(number)+'.jpg')
        if form.validate_on_submit():
            if form.answer.data==show.answer:
                current_user.score=current_user.score+1 
                db.session.commit()    
                return redirect(url_for('questions',number=show.id+1))
            else:
                return redirect(url_for('questions',number=show.id))
    return render_template("hunt.html",question=show , form= form ,image_file=image_file)

@app.route("/score")
def score_zero():
    current_user.score=0
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/see",methods=['GET'])
def see():
    return render_template('see.html')

@app.route("/leader")
def leader():
    score= User.query.order_by(User.score.desc())
    return render_template('leader.html',users=score)

@click.command(name='create_table')
@with_appcontext
def create_tables():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)