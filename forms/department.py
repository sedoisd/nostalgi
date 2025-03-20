from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class DepartmentForm(FlaskForm):
    title = StringField('Title of department', validators=[DataRequired()])
    chief = StringField('Chief', validators=[DataRequired()])
    members = IntegerField('Members', validators=[DataRequired()])
    email = StringField('Department email')
    submit = SubmitField('Submit')