from flask import Flask, render_template, request, flash,\
    redirect, url_for
from flask_sqlalchemy import SQLAlchemy
# from forms import UserForm, FileForm, DocumentationForm, LanguageForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://qmazhmdshmhlxd:1e503cc07dfd23503fa5faad3ee107fc13a945359aa05102050a557033545632@ec2-54-243-44-102.compute-1.amazonaws.com:5432/d39r230tj7mvp8"
app.config['SECRET_KEY'] = "89cycerucheriufhwejlfbwiuefh2"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(45), unique=True, primary_key=True, nullable=False)
    name = db.Column(db.String(45))
    password = db.Column(db.String(100))
    functions = db.relationship('Function', backref='user')

    def __repr__(self):
        return '<User %r>' % self.name


class Function(db.Model):
    __tablename__ = 'functions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    language = db.Column(db.String(40))
    user_email = db.Column(db.String(100), db.ForeignKey('users.email'))

    cases = db.relationship('Case', backref='function')

    def __repr__(self):
        return '<Function %r>' % self.link


class Case(db.Model):
    __tablename__ = 'cases'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45))
    version = db.Column(db.String(20))
    function_id = db.Column(db.Integer, db.ForeignKey('functions.id'))

    def __repr__(self):
        return '<Case %r>' % self.name


db.create_all()
