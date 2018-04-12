from flask_wtf import Form
from wtforms import TextField, FloatField, IntegerField, PasswordField,FileField,DecimalField, StringField, BooleanField, SubmitField, TextAreaField
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError, Email
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename


class RegisterForm(Form):
    name = TextField(
        'name', validators=[DataRequired(), Length(min=6, max=25)]
    )
    
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )   
    
    password = PasswordField(   
        'Password', validators=[DataRequired(), Length(min=6, max=40)]
    )
    
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )

    user_type = TextField(
    'user_type', validators=[DataRequired(), Length(min=6, max=40)]
    ) 
    
    #upload = FileField('image', validators=[FileAllowed(['jpg'],'Upload your shitty face')])



class LoginForm(Form):
    user_id = IntegerField('user id', [DataRequired()])

    name = TextField('name', [DataRequired()])
    
    password = PasswordField('Password', [DataRequired()])


class ForgotForm(Form):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )

class UploadForm(Form):

    WholesellerName = TextField(
        'Seller Name',validators=[DataRequired(), Length(min=6, max=40)]
    )

    VegetableName = TextField(
        'Veggies', validators=[DataRequired(), Length(min=6, max=40)]
    ) 
    
    Price = DecimalField('Price per Kilo',[DataRequired()])

class RegisterComplaintForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


    #upload = FileField('image', validators=[FileAllowed(['jpg'],'Upload your veggies')])