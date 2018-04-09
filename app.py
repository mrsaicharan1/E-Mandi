from flask import Flask,flash,Blueprint,render_template,request,redirect,session,url_for,abort
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os
from models import *
import bcrypt
from werkzeug import secure_filename, FileStorage
from flask_uploads import UploadSet,configure_uploads, IMAGES

app = Flask(__name__)

photos = UploadSet('photos',IMAGES)

app.config.from_object('config') # link config.py to this file(with all databse file paths, image upload paths)

configure_uploads(app,photos)

db = SQLAlchemy(app)
bootstrap=Bootstrap(app)


@app.route('/')
def home():
    items = Wholeseller.query.all()
    return render_template('pages/index.html',items=items,cart=cart)


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/login',methods=['POST','GET'])
def login(): 
    form = LoginForm()
    error = None
    
    
    if request.method == 'POST':
        user = User.query.filter_by(name=form.name.data).first()
        # customer login
        if user and user.user_type == 'customer' :
            kind = user.user_type 
            if bcrypt.hashpw(form.password.data.encode('utf-8'), user.password.encode('utf-8')) == user.password.encode('utf-8'):
                session['name'] = form.name.data
                session['user_type']=kind
                return redirect(url_for('home'))

        # retailer login
        if user and user.user_type == 'retailer' :
            kind = user.user_type 
            if bcrypt.hashpw(form.password.data.encode('utf-8'), user.password.encode('utf-8')) == user.password.encode('utf-8'):
                session['name'] = form.name.data
                session['user_type']=kind
                return redirect(url_for('home'))
        # wholeseller login        
        if user and user.user_type == 'wholeseller' :
            kind = user.user_type    
            if bcrypt.hashpw(form.password.data.encode('utf-8'), user.password.encode('utf-8')) == user.password.encode('utf-8'):
                session['name'] = form.name.data
                session['user_type']=kind
                return redirect(url_for('home')) 
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
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('forms/register.html',form=form)


@app.route('/admin', methods=['GET','POST'])
def admin():
    data = User.query.all()
    return render_template('pages/admin.html',data=data)

@app.route('/forgot')
def forgot():
    form = ForgotForm()
    return render_template('forms/forgot.html', form=form)

@app.route('/product')
def product():
    return render_template('pages/product.html')

@app.route('/cart',methods=['GET','POST'])
def cart():
    total =0
    cart = {}
    cart.update({request.form['vegetable_name']:request.form['vegetable_price']})
    total =+ float(request.form['vegetable_price'])

    return render_template('forms/checkout.html',cart=cart,total=total,vegetable=request.form['vegetable_name'],vegetable_price=request.form['vegetable_price'])

        

@app.route('/logout',methods=['POST','GET'])
def logout():
    session.clear()
    return redirect(url_for('home'))    
# Vegetable Upload routes-----------------





@app.route('/w_upload', methods=['GET','POST'])
def w_upload():
    form = UploadForm()
    if request.method == 'POST':
        # store in database with transaction id
        vegetable_data = Wholeseller(form.WholesellerName.data,form.VegetableName.data,form.Price.data)
        db.session.add(vegetable_data)
        db.session.commit()
        items = Wholeseller.query.all()
        # render in page 

        return render_template('pages/index.html',items=items,name_vegetable=form.VegetableName.data,price_vegetable=form.Price.data,wholeseller_name=form.WholesellerName.data)

    return render_template('forms/wholeseller-upload.html', form=form)

@app.route('/r_upload', methods=['GET','POST'])
def r_upload():
    form = UploadForm()
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        return render_template('pages/index.html',name_vegetable=form.VegetableName.data,price_vegetable=form.Price.data,filename=filename)

    return render_template('forms/retailer-upload.html', form=form)
    

@app.route('/register_complaint', methods = ['GET','POST'])
def register_complaint():
    form = RegisterComplaintForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('forms/register-complaint.html', title='Register', form=form)




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

