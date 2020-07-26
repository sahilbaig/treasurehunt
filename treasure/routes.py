from treasure.models import User, Questions
from flask import render_template, url_for,redirect,flash
from treasure.forms import LoginForm, RegistrationForm , Answer
from treasure import app,bcrypt
from flask_login import LoginManager,UserMixin,login_user,current_user,logout_user

from treasure import db


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
        register_user=User(username=form.username.data , password=hash_pass ,email=form.email.data)
        db.session.add(register_user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html', form= form)

@app.route("/question/<int:number>" ,methods=['POST','GET'])
def questions(number):
    if number==0:
        return redirect(url_for('questions',number=1))
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
            if form.answer.data=="swiggy" and number==4:
                current_user.score=0
                db.session.commit()
                return render_template('index.html', trap="In case you have not noticed you fell right into my trap")
            else:
                # return redirect(url_for('questions',number=show.id ))
                return render_template("hunt.html",question=show , form= form ,image_file=image_file, error="Not that easy, try something else")
    return render_template("hunt.html",question=show , form= form ,image_file=image_file)

# @app.route("/score")
# def score_zero():
#     current_user.score=0
#     db.session.commit()
#     return redirect(url_for('home'))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

# @app.route("/see",methods=['GET'])
# def see():
#     return render_template('see.html')

@app.route("/leader")
def leader():
    score= User.query.order_by(User.score.desc())
    return render_template('leader.html',users=score)

@app.errorhandler(404)
def error_404(error):
    return render_template('404.html'),404

@app.errorhandler(403)
def error_403(error):
    return render_template('403.html'),403

@app.errorhandler(401)
def error_500(error):
    return render_template('404.html'),401