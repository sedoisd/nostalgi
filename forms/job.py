from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    title = StringField('Job title', validators=[DataRequired()])
    team_leader = StringField('team leader id', validators=[DataRequired()])
    duration = IntegerField('work size', validators=[DataRequired()])
    collaborators = StringField('collaborators')
    is_finished = BooleanField('is job finished?')
    submit = SubmitField('Submit')
