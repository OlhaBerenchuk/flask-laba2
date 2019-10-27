from flask import Flask, render_template, request, flash,\
    redirect, url_for
from flask_sqlalchemy import SQLAlchemy
# from forms import UserForm, FileForm, DocumentationForm, LanguageForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://pyaumkueyzideg:04138428c08de9af6e296214ba8f2cf43eb59b0bed0ad3d6bf83e06e667bc23c@ec2-107-21-126-201.compute-1.amazonaws.com:5432/d4btdruvjcdrq9"
app.config['SECRET_KEY'] = "8ew9fyweuihwe8fwe8fwyefw"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(45), unique=True, primary_key=True, nullable=False)
    name = db.Column(db.String(45))
    password = db.Column(db.String(100))
    function = db.relationship('Functions', backref='user')

    def __repr__(self):
        return '<User %r>' % self.name


class Case(db.Model):
    __tablename__ = 'cases'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45))
    version = db.Column(db.String(20))
    function_id = db.Column(db.Integer, db.ForeignKey('functions.id'))

    def __repr__(self):
        return '<Case %r>' % self.name


class Funtion(db.Model):
    __tablename__ = 'functions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    language = db.Column(db.String(40))
    user_email = db.Column(db.String(100), db.ForeignKey('users.email'))

    cases = db.relationship('Cases', backref='functions')

    def __repr__(self):
        return '<Function %r>' % self.link


db.create_all()
