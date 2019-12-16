from flask_wtf import Form
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import Email, InputRequired, URL, NumberRange


class CompanyForm(Form):
    name = StringField('Name', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    balance = IntegerField('Balance', validators=[NumberRange(min=1000, max=1000000, message='More than 1000!')])
    type = SelectField('Type', choices=[('org', 'ORG'), ('edu', 'EDU'), ('bis', 'BIS')])


class UserForm(Form):
    name = StringField('Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email(message="It\'s not an email!")])
    phone = StringField('Phone', validators=[InputRequired()])


class FunctionForm(Form):
    name = StringField('Name', validators=[InputRequired()])
    language = StringField('Language', validators=[InputRequired()])


class CaseForm(Form):
    name = StringField('Name', validators=[InputRequired()])
    version = StringField('Version', validators=[InputRequired()])


class GroupForm(Form):
    name = StringField('Name', validators=[InputRequired()])
    count = IntegerField('Count', validators=[InputRequired()])
