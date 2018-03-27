from flask import Flask,Blueprint,render_template,request,redirect,session,url_for,abort
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os
from models import *
import bcrypt

app = Flask(__name__)
app.config.from_object('config') #specify database file path
db = SQLAlchemy(app)




@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/login',methods=['POST','GET'])
def login(): 
    form = LoginForm()
    error = None
    
    
    if form.validate_on_submit():
        user = User.objects.filter(name=form.name.data).first()
        if user:
            if bcrypt.hashpw(form.password.data, user.password) == user.password:
                session['name'] = form.name.data
                
            else:
                user = None
        if not user:
            error = 'Incorrect credentials'
    return render_template('forms/login.html', form=form, error=error)	



@app.route('/register',methods=['POST','GET'])
def register():
    form=RegisterForm()

    if request.method == 'POST':
        hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt(10))
        data = User(form.name.data, form.email.data, hashed_password, form.user_type.data)
        db.session.add(data)
	db.session.commit()
        return 'User registered'
    return render_template('forms/register.html',form=form)





@app.route('/forgot')
def forgot():
    form = ForgotForm()
    return render_template('forms/forgot.html', form=form)

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug=True)

