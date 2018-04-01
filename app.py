from flask import Flask,Blueprint,render_template,request,redirect,session,url_for,abort
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os
from models import *
import bcrypt
from werkzeug import secure_filename, FileStorage

app = Flask(__name__)
app.config.from_object('config') # specify database file path
db = SQLAlchemy(app)
bootstrap=Bootstrap(app)

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos) 


@app.route('/')
def home():
    return render_template('pages/index.html')


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/login',methods=['POST','GET'])
def login(): 
    form = LoginForm()
    error = None
    
    
    if request.method == 'POST':
        user = User.query.filter_by(name=form.name.data).first()
        if user:
            if bcrypt.hashpw(form.password.data.encode('utf-8'), user.password.encode('utf-8')) == user.password.encode('utf-8'):
                session['name'] = form.name.data
                return render_template('pages/index.html')
            else:
                user = not_found_error
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
    if request.method == 'GET':
        return render_template('forms/register.html',form=form)





@app.route('/forgot')
def forgot():
    form = ForgotForm()
    return render_template('forms/forgot.html', form=form)

@app.route('/product')
def product():
    return render_template('pages/product.html')

@app.route('/checkout.html')
def checkout():
    return render_template('pages/checkout.html')    

# Vegetable Upload routes

@app.route('/upload', methods=['GET','POST'])
def upload():
    form = WUploadForm()

    if request.method == 'POST':
        filename = photos.save(form.upload.data)
        file_url = photos.url(filename)
        return render_template('index.html',file_url=file_url)
    #else:
        #file_url = None

    return render_template('forms/wholeseller-upload.html', form=form)

    





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

