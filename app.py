from flask import Flask, render_template, request, flash,\
    redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import UserForm, FunctionForm, CaseForm, GroupForm
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://qmazhmdshmhlxd:1e503cc07dfd23503fa5faad3ee107fc13a945359aa05102050a557033545632@ec2-54-243-44-102.compute-1.amazonaws.com:5432/d39r230tj7mvp8"
app.config['SECRET_KEY'] = "89cycerucheriufhwejlfbwiuefh2"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    count = db.Column(db.Integer)

    users = db.relationship('User', backref='group')


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    email = db.Column(db.String(45), unique=True, nullable=False)
    name = db.Column(db.String(45))
    password = db.Column(db.String(100))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))

    functions = db.relationship('Function', backref='user')

    def __repr__(self):
        return '<User %r>' % self.name


class Function(db.Model):
    __tablename__ = 'functions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    language = db.Column(db.String(40))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

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


@app.route('/', methods=['GET'])
def home():
    return render_template('header.html')


@app.route('/add', methods=['GET'])
def add():
    group1 = Group(name='KM-61', count=20)
    db.session.add(group1)
    db.session.commit()
    group2 = Group(name='KM-62', count=23)
    db.session.add(group2)
    db.session.commit()
    group3 = Group(name='KM-63', count=21)
    db.session.add(group3)
    db.session.commit()
    return render_template('header.html')


@app.route('/group', methods=['GET'])
def groups():
    result = []
    form = GroupForm()
    groups = Group.query.all()
    for group in groups:
        result.append([group.id, group.name, group.count])
    return render_template('groups.html', rows=result, form=form)


@app.route('/insert_group', methods=['post'])
def insert_group():
    form = GroupForm()
    name = form.name.data
    count = form.count.data
    group = Group(name=name, count=count)
    db.session.add(group)
    db.session.commit()
    return redirect('/group')


@app.route('/update_group', methods=['post'])
def update_group():
    id = request.form['id']
    name = request.form['name']
    count = request.form['count']
    group = Group.query.filter_by(id=id).first()
    group.name = name
    group.count = count
    db.session.add(group)
    db.session.commit()
    return redirect('/group')


@app.route('/delete_group/<string:id>', methods=['get'])
def delete_group(id):
    group = Group.query.filter_by(id=id).first()
    db.session.delete(group)
    db.session.commit()
    return redirect('/group')


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
    print(id)
    name = request.form['name']
    print(name)
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


@app.route('/function', methods=['GET'])
def function():
    result = []
    form = FunctionForm()
    functions = Function.query.all()
    for function in functions:
        result.append([function.id, function.name, function.language])
    return render_template('functions.html', rows=result, form=form)


@app.route('/insert_function', methods=['post'])
def insert_function():
    form = FunctionForm()
    name = form.name.data
    language = form.language.data
    function = Function(name=name, language=language)
    db.session.add(function)
    db.session.commit()
    return redirect('/function')


@app.route('/update_function', methods=['post'])
def update_function():
    id = request.form['id']
    name = request.form['name']
    language = request.form['language']
    function = Function.query.filter_by(id=id).first()
    function.name = name
    function.language = language
    db.session.add(function)
    db.session.commit()
    return redirect('/function')


@app.route('/delete_function/<string:id>', methods=['get'])
def delete_function(id):
    function = Function.query.filter_by(id=id).first()
    db.session.delete(function)
    db.session.commit()
    return redirect('/function')


@app.route('/case', methods=['GET'])
def case():
    result = []
    form = CaseForm()
    cases = Case.query.all()
    for case in cases:
        result.append([case.id, case.name, case.version])
    return render_template('cases.html', rows=result, form=form)


@app.route('/insert_case', methods=['post'])
def insert_case():
    form = CaseForm()
    name = form.name.data
    version = form.version.data
    case = Case(name=name, version=version)
    db.session.add(case)
    db.session.commit()
    return redirect('/case')


@app.route('/update_case', methods=['post'])
def update_case():
    id = request.form['id']
    name = request.form['name']
    version = request.form['version']
    case = Case.query.filter_by(id=id).first()
    case.name = name
    case.version = version
    db.session.add(case)
    db.session.commit()
    return redirect('/case')


@app.route('/delete_case/<string:id>', methods=['get'])
def delete_case(id):
    doc = Case.query.filter_by(id=id).first()
    db.session.delete(doc)
    db.session.commit()
    return redirect('/case')


@app.route('/dashboard', methods=['get'])
def dashboard():
    labels = ['Users', 'Files', 'Documentation']
    count = [
        len(User.query.all()),
        len(Function.query.all()),
        len(Case.query.all())
    ]

    fig, ax = plt.subplots()
    ax.pie(count, labels=labels, autopct='%1.1f%%')
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
    ax.set_title('Count rows')
    pie = "pie"+str(datetime.now())+".png"
    plt.savefig(f'./static/images/{pie}')

    plt.clf()

    objects = ('Python', 'Not python')
    y_pos = np.arange(len(objects))
    admin_count = (Function.query.filter_by(language='python').count())
    performance = [admin_count, len(Function.query.all()) - admin_count]

    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Usage')
    plt.title('Python vs not')
    bar = "bar" + str(datetime.now()) + ".png"
    plt.savefig(f'./static/images/{bar}')

    return render_template('dash.html', bar=bar, pie=pie)


if __name__ == '__main__':
    app.run(debug=False)
