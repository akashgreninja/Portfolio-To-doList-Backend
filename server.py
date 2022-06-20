
from functools import wraps
from flask import Flask, render_template,request, url_for,flash,redirect,abort
import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from matplotlib.pyplot import title
from sqlalchemy import null
from wtforms import StringField, SubmitField,PasswordField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_ckeditor import CKEditor
from form import LoginForm,FieldForm,CreatePostForm
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///hola-11.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']="akash"
ckeditor = CKEditor(app)

db = SQLAlchemy(app)
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))





    



class User(UserMixin,db.Model):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    posts = relationship("Info", back_populates="author")
    


db.create_all()

class Info(db.Model):
    __tablename__="events"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=True)
    body = db.Column(db.String(100000),nullable=True)
   
    author = relationship("User", back_populates="posts")
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))

db.create_all()

@app.route("/",methods=["POST","GET"])
def home():
    try:
        all_events=Info.query.filter_by(author_id=current_user.id).all()
    
    except:
        all_events=Info.query.filter_by(author_id=None).all()
    finally:  
        return render_template('index.html',all_events=all_events,is_user_in=current_user.is_authenticated )
  



@app.route("/login",methods=["POST","GET"])
def login():
    form=LoginForm()
    the_object=User.query.filter_by(email=form.email.data).first()
    if form.validate_on_submit():
        if not the_object:
            flash("please register again this email does not exist ")
            return redirect(url_for('login'))
        
        elif not check_password_hash(the_object.password,form.password.data):  
            flash("That password is wrong.")
            return redirect(url_for('login'))
        
        else:
            login_user(the_object)
            return redirect(url_for('home'))    
        

    return render_template("login.html",form=form)



@app.route('/register',methods=["POST","GET"])
def register():
    form=FieldForm()
    if form.validate_on_submit():
            if User.query.filter_by(email=form.email.data).first():
                flash("you have already registered ,Sign up")
                return redirect(url_for('login'))

            new_password=generate_password_hash(password=form.password.data, method='pbkdf2:sha256', salt_length=8)
            get_object=User(
    
            email = form.email.data,
            password = new_password,
            name = form.name.data
            )
            db.session.add(get_object)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('register.html',form=form,is_user_in=current_user.is_authenticated )


@app.route("/create_form",methods=["POST","GET"])
def create_form():
    form=CreatePostForm()
    if form.validate_on_submit():
        
        new_obj=Info(
            title = form.title.data,
            body = form.body.data,
            author=current_user
        )
    

        db.session.add(new_obj)
        db.session.commit()
        
        return redirect(url_for('home'))

    return render_template('create_form.html',form=form,is_user_in=current_user.is_authenticated )




@app.route("/edit-post/<int:id>",methods=["POST","GET"])

def edit_post(id):
    the_object=Info.query.get(id)
    form=CreatePostForm(
        title = the_object.title,
        body = the_object.body
    )
    if form.validate_on_submit():
        the_object.title=form.title.data
        the_object.body=form.body.data
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('create_form.html',form=form,is_user_in=current_user.is_authenticated )




@app.route("/delete/<int:id>")

def delete_post(id):
    the_object=Info.query.get(id)
    db.session.delete(the_object)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__=="__main__":
    app.run(debug=True)

    
