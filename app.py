from flask import Flask, render_template, request, flash,\
    redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import UserForm, FunctionForm, CaseForm, GroupForm, CompanyForm
import json
import plotly.graph_objs as go
import plotly
from sqlalchemy.sql import func


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://dcdbecjtvigzhu:fdd5f3694bd6b0fc19f1ea5c54157149027196e1c2757eb7d9c0c4202b6eb0c1" \
                                        "@ec2-174-129-255-10.compute-1.amazonaws.com:5432/d3s8u1rking4fp"
app.config['SECRET_KEY'] = "123qweasdzxcrtyfghvbn"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class OrmUser(db.Model):
    __tablename__ = 'orm_user'

    user_email = db.Column(db.String(45), primary_key=True)
    user_name = db.Column(db.String(45), nullable=False)
    user_phone = db.Column(db.String(45), nullable=False)

    user_functions = db.relationship('Function')
    company_name_fk = db.relationship('OrmCompany', secondary='user_has_company')


class UserHasCompany(db.Model):
    __tablename__ = 'user_has_company'
    user_email = db.Column(db.String(45), db.ForeignKey('orm_user.user_email'), primary_key=True)
    company_name = db.Column(db.String(45), db.ForeignKey('orm_company.company_name'), primary_key=True)


class OrmCompany(db.Model):
    __tablename__ = 'orm_company'

    company_name = db.Column(db.String(45), primary_key=True)
    company_location = db.Column(db.String(100), nullable=False)
    company_balance = db.Column(db.Integer)
    company_type = db.Column(db.String(45))

    user_email_fk = db.relationship('OrmUser', secondary='user_has_company')


class Function(db.Model):
    __tablename__ = 'orm_function'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    language = db.Column(db.String(40))
    user_email = db.Column(db.String(45), db.ForeignKey('orm_user.user_email'))

    cases = db.relationship('Case')


class Case(db.Model):
    __tablename__ = 'orm_case'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45))
    version = db.Column(db.String(20))

    function_id = db.Column(db.Integer, db.ForeignKey('orm_function.id'))


@app.route('/', methods=['GET'])
def home():
    return render_template('header.html')


@app.route('/get', methods=['GET'])
def get():
    company1 = OrmCompany(company_name='Qwe', company_location='Location1', company_balance='1111', company_type='edu')
    company2 = OrmCompany(company_name='Asd', company_location='Location2', company_balance='2222', company_type='org')
    company3 = OrmCompany(company_name='Zxc', company_location='Location3', company_balance='3333', company_type='bis')
    db.session.add(company1)
    db.session.add(company2)
    db.session.add(company3)
    db.session.commit()
    return redirect('/company')


@app.route('/company', methods=['GET'])
def company():
    result = []
    form = CompanyForm()
    companies = OrmCompany.query.all()
    for company in companies:
        result.append([company.company_name, company.company_location, company.company_balance, company.company_type])
    return render_template('company.html', rows=result, form=form)


@app.route('/insert_company', methods=['post'])
def insert_company():
    form = CompanyForm()
    name = form.name.data
    location = form.location.data
    balance = form.balance.data
    type = form.type.data
    company = OrmCompany(company_name=name, company_location=location, company_balance=balance, company_type=type)
    db.session.add(company)
    db.session.commit()
    return redirect('/company')


@app.route('/delete_company/<string:name>', methods=['get'])
def delete_company(name):
    company = OrmCompany.query.filter_by(company_name=name).first()
    db.session.delete(company)
    db.session.commit()
    return redirect('/company')


@app.route('/user', methods=['GET'])
def users():
    result = []
    form = UserForm()
    users = OrmUser.query.all()
    for user in users:
        result.append([user.user_email, user.user_name, user.user_phone])
    return render_template('users.html', rows=result, form=form)


@app.route('/insert_user', methods=['post'])
def insert_user():
    form = UserForm()
    name = form.name.data
    email = form.email.data
    phone = form.phone.data
    user = OrmUser(user_name=name, user_email=email, user_phone=phone)
    db.session.add(user)
    db.session.commit()
    return redirect('/user')


@app.route('/update_user', methods=['post'])
def update_user():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    user = OrmUser.query.filter_by(user_email=email).first()
    user.user_name = name
    user.user_email = email
    user.user_phone = phone
    db.session.add(user)
    db.session.commit()
    return redirect('/user')


@app.route('/delete_user/<string:email>', methods=['get'])
def delete_user(email):
    user = OrmUser.query.filter_by(user_email=email).first()
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
    query1 = (
        db.session.query(
            OrmCompany.company_name,
            OrmCompany.company_balance
        )
    ).all()

    name, balance = zip(*query1)
    print(name, balance)
    bar = go.Bar(
        x=name,
        y=balance
    )

    data = {
        "bar": [bar],
        "pie": [('121',), (121,)]
    }
    graphs_json = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', graphsJSON=graphs_json)


if __name__ == '__main__':
    app.run(debug=False)
