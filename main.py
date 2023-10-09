from smtp import Email
from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from functools import wraps
from datetime import date
from hash import Pwd_hash as hash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_gravatar import Gravatar
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData, Text


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view= "login"

##CONFIGURE TABLES
class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name= db.Column(db.String(100))

class Sub(UserMixin, db.Model):
    __tablename__ = "sub"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    date = db.Column(db.String(250), nullable=False)
    Centre = db.Column(db.String(100))


class BlogPost(db.Model):
    __tablename__ = "event"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250))
    name = db.Column(db.String(250),  nullable=False)
    date = db.Column(db.String(250), nullable=False)
    location = db.Column(db.Text, nullable=False)


db.create_all()



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




@app.route("/")
@login_required
def index():
    return render_template("index.html", login=current_user)

@app.route("/admin")
@login_required
def admin():
    data = Sub.query.filter_by()
    return render_template("admin.html", login=current_user, data=data)

@app.route("/book", methods=["POST","GET"])
@login_required
def book():

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        plan = request.form.get("Centre")
        date = request.form.get("event_date")
        message = f"""
    Hello {name},
    
    We are pleased to confirm your booking details:
        Email: {email}
        Date: {date}
        Centre: {plan}
    
    Thank you for choosing our services. If you have any further questions or need assistance, please don't hesitate to contact us  using this email.
    
Best regards"""
        try:
            Email().send_mail(email, message)
            new_post = Sub(email=email, name=name, Centre=plan, date=date)
            db.session.add(new_post)
            db.session.commit()
            dt = True
        except:
            Email().send_mail(email, message)
            new_post = Sub(email=email, name=name, Centre=plan, date=date)
            db.session.add(new_post)
            db.session.commit()
            dt = True
    else:
        name = ""
        dt = False
    return render_template("book.html", login=current_user, condition=dt, user=name)

@app.route("/about")
@login_required
def about():
    return render_template("about.html", login=current_user)


@app.route("/login", methods=["POST", "GET"])
def login():
    form = ""
    if request.args.get("error") == None:
        error = ""
    else:
        error = request.args.get("error")
    if request.method == "POST":
        email = request.form.get("email").lower()
        user_info = User.query.filter_by(email=email).first()
        print(user_info.id)
        if user_info == None:
            error = f"This email is not registered in the system, please signup"
        else:
            password = hash().passindata(request.form.get("password"))
            if password == user_info.password:
                login_user(user_info)
                if user_info.id == 3:
                    return redirect(url_for("admin"))
                else:
                    return redirect(url_for("index"))
            else:
                error = "the password you entered is incorrect!"
    return render_template("login.html", form=form, error=error, login=current_user)


@app.route("/sign-up", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        password = hash().passindata(request.form.get("password"))
        new_post = User(email=email, name=name, password=password)
        db.session.add(new_post)
        db.session.commit()
        user_info = User.query.filter_by(email=email).first()
        login_user(user_info)
        return redirect(url_for("index"))
    return render_template("signup.html", login=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route("/edit/<int:id>", methods=["POST", 'GET'])
@login_required
def edit(id):
    post = Sub.query.get(id)
    if request.method == "POST":
        post.name = request.form.get("name")
        post.email = request.form.get("email")
        post.date = request.form.get("event_date")
        db.session.commit()
        message = f"""
    Hello {post.name},
    
    We are pleased to confirm your reschedule details:
        Email: {post.email}
        Date: {post.date}
        Centre: {post.Centre}
    
    Thank you for choosing our services. If you have any further questions or need assistance, please don't hesitate to contact us using this email.
    
Best regards"""
        Email().send_mail(post.email,message)
        return redirect(url_for("admin"))
    return render_template("edit.html", post=post, login=current_user)



if __name__=="__main__":
    app.run(debug=True)