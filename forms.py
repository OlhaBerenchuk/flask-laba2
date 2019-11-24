from flask_wtf import Form
from wtforms import StringField, IntegerField
from wtforms.validators import Email, InputRequired, URL


class UserForm(Form):
    name = StringField('Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email(message="It\'s not an email!")])


class FunctionForm(Form):
    name = StringField('Name', validators=[InputRequired()])
    language = StringField('Language', validators=[InputRequired()])


class CaseForm(Form):
    name = StringField('Name', validators=[InputRequired()])
    version = StringField('Version', validators=[InputRequired()])


class GroupForm(Form):
    name = StringField('Name', validators=[InputRequired()])
    count = IntegerField('Count', validators=[InputRequired()])
