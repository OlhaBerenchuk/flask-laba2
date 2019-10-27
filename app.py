from flask import Flask, render_template, request, flash,\
    redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import UserForm, FileForm, DocumentationForm
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


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


@app.route('/', methods=['GET'])
def home():
    return render_template('header.html')


@app.route('/user', methods=['GET'])
def users():
    result = []
    form = UserForm()
    users = User.query.all()
    for user in users:
        result.append([user.id, user.name, user.email])
    return render_template('users.html', rows=result, form=form)


@app.route('/insert_user', methods=['post'])
def insert_user():
    form = UserForm()
    name = form.name.data
    email = form.email.data
    user = User(name=name, email=email)
    db.session.add(user)
    db.session.commit()
    return redirect('/user')


@app.route('/update_user', methods=['post'])
def update_user():
    id = request.form['id']
    name = request.form['name']
    email = request.form['email']
    user = User.query.filter_by(id=id).first()
    user.name = name
    user.email = email
    db.session.add(user)
    db.session.commit()
    return redirect('/user')


@app.route('/delete_user/<string:id>', methods=['get'])
def delete_user(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect('/user')


@app.route('/file', methods=['GET'])
def files():
    result = []
    form = FileForm()
    files = File.query.all()
    for file in files:
        result.append([file.id, file.name, file.link])
    return render_template('files.html', rows=result, form=form)


@app.route('/insert_file', methods=['post'])
def insert_file():
    form = FileForm()
    name = form.name.data
    link = form.link.data
    file = File(name=name, link=link)
    db.session.add(file)
    db.session.commit()
    return redirect('/file')


@app.route('/update_file', methods=['post'])
def update_file():
    id = request.form['id']
    name = request.form['name']
    link = request.form['link']
    file = User.query.filter_by(id=id).first()
    file.name = name
    file.link = link
    db.session.add(file)
    db.session.commit()
    return redirect('/file')


@app.route('/delete_file/<string:id>', methods=['get'])
def delete_file(id):
    file = File.query.filter_by(id=id).first()
    db.session.delete(file)
    db.session.commit()
    return redirect('/file')


@app.route('/doc', methods=['GET'])
def doc():
    result = []
    form = DocumentationForm()
    docs = Documentation.query.all()
    for doc in docs:
        result.append([doc.id, doc.actor, doc.link])
    return render_template('doc.html', rows=result, form=form)


@app.route('/insert_doc', methods=['post'])
def insert_doc():
    form = DocumentationForm()
    actor = form.actor.data
    link = form.link.data
    doc = Documentation(actor=actor, link=link)
    db.session.add(doc)
    db.session.commit()
    return redirect('/doc')


@app.route('/update_doc', methods=['post'])
def update_doc():
    id = request.form['id']
    actor = request.form['actor']
    link = request.form['link']
    doc = Documentation.query.filter_by(id=id).first()
    doc.actor = actor
    doc.link = link
    db.session.add(doc)
    db.session.commit()
    return redirect('/doc')


@app.route('/delete_doc/<string:id>', methods=['get'])
def delete_doc(id):
    doc = Documentation.query.filter_by(id=id).first()
    db.session.delete(doc)
    db.session.commit()
    return redirect('/doc')


@app.route('/dashboard', methods=['get'])
def dashboard():
    labels = ['Users', 'Files', 'Documentation']
    count = [
        len(User.query.all()),
        len(File.query.all()),
        len(Documentation.query.all())
    ]

    fig, ax = plt.subplots()
    ax.pie(count, labels=labels, autopct='%1.1f%%')
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
    ax.set_title('Count rows')
    pie = "pie"+str(datetime.now())+".png"
    plt.savefig(f'./static/images/{pie}')

    plt.clf()

    objects = ('Admin', 'Not admin')
    y_pos = np.arange(len(objects))
    admin_count = (Documentation.query.filter_by(actor='Admin').count())
    performance = [admin_count, len(Documentation.query.all()) - admin_count]

    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Usage')
    plt.title('Actors documentations')
    bar = "bar" + str(datetime.now()) + ".png"
    plt.savefig(f'./static/images/{bar}')

    return render_template('dash.html', bar=bar, pie=pie)


if __name__ == '__main__':
    app.run(debug=False)
