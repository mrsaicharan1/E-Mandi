from flask_wtf import Form
from wtforms import TextField, PasswordField,FileField,DecimalField
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from wtforms.validators import DataRequired, EqualTo, Length
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
    name = TextField('name', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


class ForgotForm(Form):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )

class UploadForm(Form):

    VegetableName = TextField(
        'Veggies', validators=[DataRequired(), Length(min=6, max=40)]
    ) 
    
    Price = DecimalField('Price per Kilo',[DataRequired()])

    #upload = FileField('image', validators=[FileAllowed(['jpg'],'Upload your veggies')])