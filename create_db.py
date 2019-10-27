from flask import Flask, render_template, request, flash,\
    redirect, url_for
from flask_sqlalchemy import SQLAlchemy
# from forms import UserForm, FileForm, DocumentationForm, LanguageForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://zsvdaxdweixisy:be124cabeeab510cfb568f0caa4ce35843ce0c6537cc153171916bed142fee56@ec2-75-101-128-10.compute-1.amazonaws.com:5432/da8dfm6fl31skk"
app.config['SECRET_KEY'] = "8ew9fyweuihwe8fwe8fwyefw"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(45), unique=True, primary_key=True, nullable=False)
    name = db.Column(db.String(45))
    password = db.Column(db.String(100))
    # function = db.relationship('Function', backref='user')
    # case = db.relationship('Case', backref='case')

    def __repr__(self):
        return '<User %r>' % self.name


class Function(db.Model):
    __tablename__ = 'functions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    language = db.Column(db.String(40))
    # user_email = db.Column(db.String(100), db.ForeignKey('users.email'))

    def __repr__(self):
        return '<Function %r>' % self.name


class Case(db.Model):
    __tablename__ = 'casess'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45))
    description = db.Column(db.String(100))
    result = db.Column(db.String(100))
    # user_email = db.Column(db.String(100), db.ForeignKey('users.email'))

    def __repr__(self):
        return '<Case %r>' % self.name


User.__table__.drop(db)
Function.__table__.drop(db)
Case.__table__.drop(db)
