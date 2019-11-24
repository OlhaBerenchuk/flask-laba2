from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://qmazhmdshmhlxd:1e503cc07dfd23503fa5faad3ee107fc13a945359aa05102050a557033545632@ec2-54-243-44-102.compute-1.amazonaws.com:5432/d39r230tj7mvp8"
app.config['SECRET_KEY'] = "89cycerucheriufhwejlfbwiuefh2"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


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


# Case.__table__.drop(db.engine)
# Function.__table__.drop(db.engine)
# User.__table__.drop(db.engine)
# Group.__table__.drop(db.engine)
if __name__ == '__main__':
    manager.run()

# db.create_all()
