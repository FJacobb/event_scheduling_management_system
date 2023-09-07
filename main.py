from smtp import Email
from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from functools import wraps
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_gravatar import Gravatar
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData, Text


app = Flask(__name__)
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
    return render_template("index.html")


@app.route("/about")
@login_required
def about():
    return render_template("about.html")


@app.route("/login")
def login():
    form = ""
    if request.args.get("error") == None:
        error = ""
    else:
        error = request.args.get("error")
    if request.method == "POST":
        email = form.email.data.lower()
        user_info = User.query.filter_by(email=email).first()
        if user_info == None:
            error = f"This email is not registered in the system, please signup"
        else:
            password = hash().passindata(form.password.data)
            if password == user_info.password:
                login_user(user_info)
                return redirect(url_for("get_all_posts"))
            else:
                error = "the password you entered is incorrect!"
    return render_template("login.html", form=form, error=error, login=current_user)


@app.route("/sign-up")
def signup():
    return render_template("index.html")


if __name__=="__main__":
    app.run(debug=True)