from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Optional, URL
from models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ProfileSetupForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=150)])
    college = StringField('College', validators=[DataRequired(), Length(max=200)])
    branch = StringField('Branch', validators=[DataRequired(), Length(max=150)])
    year_of_study = SelectField('Year of Study', choices=[
        ('1', '1st Year'),
        ('2', '2nd Year'),
        ('3', '3rd Year'),
        ('4', '4th Year'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    target_role = StringField('Target Role', validators=[DataRequired(), Length(max=150)])
    github_link = StringField('GitHub Link (Optional)', validators=[Optional(), URL()])
    linkedin_link = StringField('LinkedIn Link (Optional)', validators=[Optional(), URL()])
    submit = SubmitField('Save Profile')

class EditProfileForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=150)])
    college = StringField('College', validators=[DataRequired(), Length(max=200)])
    branch = StringField('Branch', validators=[DataRequired(), Length(max=150)])
    year_of_study = SelectField('Year of Study', choices=[
        ('1', '1st Year'),
        ('2', '2nd Year'),
        ('3', '3rd Year'),
        ('4', '4th Year'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    target_role = StringField('Target Role', validators=[DataRequired(), Length(max=150)])
    github_link = StringField('GitHub Link (Optional)', validators=[Optional(), URL()])
    linkedin_link = StringField('LinkedIn Link (Optional)', validators=[Optional(), URL()])
    submit = SubmitField('Update Profile')

class SkillForm(FlaskForm):
    name = StringField('Skill Name', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Add Skill')

class ApplicationForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired(), Length(max=150)])
    role = StringField('Role', validators=[DataRequired(), Length(max=150)])
    status = SelectField('Status', choices=[
        ('Applied', 'Applied'),
        ('Interview Scheduled', 'Interview Scheduled'),
        ('Rejected', 'Rejected'),
        ('Offer Received', 'Offer Received')
    ], validators=[DataRequired()])
    deadline = DateField('Deadline (Optional)', format='%Y-%m-%d', validators=[Optional()])
    rejection_reason = SelectField('Rejection Reason', choices=[
        ('', '--- Select Reason ---'),
        ('Resume Weak', 'Resume Weak'),
        ('Missing Skills', 'Missing Skills'),
        ('Failed Coding Round', 'Failed Coding Round'),
        ('Failed Interview', 'Failed Interview')
    ], validators=[Optional()])
    submit = SubmitField('Save Application')
