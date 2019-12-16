from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://dcdbecjtvigzhu:fdd5f3694bd6b0fc19f1ea5c54157149027196e1c2757eb7d9c0c4202b6eb0c1" \
                                        "@ec2-174-129-255-10.compute-1.amazonaws.com:5432/d3s8u1rking4fp"
app.config['SECRET_KEY'] = '123qweasdzxcrtyfghvbn'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


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
    company_balance = db.Column(db.String(45))
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


if __name__ == '__main__':
    manager.run()