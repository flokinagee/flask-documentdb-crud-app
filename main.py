# from app import app
from bson.json_util import dumps
from flask import jsonify, request, url_for, flash, render_template, redirect
from flask_mail import Mail, Message
from flask_login import login_required, current_user, LoginManager
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import logging
import settings
from tables import Results
import json
import os

from flask import Flask

app = Flask(__name__)
app.secret_key = "secret key"
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'XXXXX@gmail.com',
    MAIL_PASSWORD = 'XXXXXXXXX',
))


mail = Mail(app)




from lib import db

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return db.get_user("_id", id)


s = URLSafeTimedSerializer(app.secret_key)



@app.route('/new_user')
def add_user_view():
	return render_template('add.html')


@app.route('/add', methods=['POST'])
def add_user():
        customer_id = request.form['customerId']
        name = request.form['inputName']
        email = request.form['inputEmail']
        amount = request.form['inputAmount']
        month = request.form['inputMonth']
        charm = request.form['Charm']
        # validate the received values
        if name and email and amount and request.method == 'POST':
                # save details
                id = db.add({'_id': customer_id, 'name': name, 'email': email, 'amount': amount, 'month': month, 'charm' : charm})
                flash('User added successfully!')
                return redirect('/')
        else:
                return not_found()

#######
@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        #return '<form action="/" method="POST"><input name="email"><input type="summit"></form>'
        return render_template('index.html')
    return '<h1> The email you endered is {}. The token is {} </h1>' .format(email, token)

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        return '<h1> The token is Expired <\h1>'

    data = db.get_user(email, "email")
    if data['email_confirmation']:
        flash('User already verified successfully! please login')
    else:
        data['email_confirmation'] = "verified"
        results = db.update_user(data)
        flash('User has been verified successfully')
    return render_template('users.html')

@app.route('/profile')
@login_required
def profile():
	# return render_template('profile.html', name=current_user.name)
    return render_template('profile.html', name=current_user.name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    user = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    if user  and password and request.method == 'POST':
        data = db.get_user(user, "user")
        if data['user'] == user and data['password'] == password:
            #return jsonify("You are successfully loged in")
            return redirect('/login?next=' + request.url)
        flash("You username or password incorrect")
        return redirect('/login')
    else:
        return not_found()

@app.route('/signup', methods = ['GET', 'POST'])
def signup(): 
    if request.method == 'GET':
        #return '<form action="/" method="POST"><input name="email"><input type="summit"></form>'
        # return render_template('index.html')
        return render_template('signup.html')

    email = request.form['email']
    user = request.form['name']
    password = request.form['password']
    token = s.dumps(email, salt='email-confirm')

    data = db.get_user(email, "email")
    if data['email'] == email:
        flash("You are rigistered user. Please login")
        return redirect('/login')
    results = db.add_user({'email': email, 'user': user, 'password': password, "email_confirmation": None})

    msg = Message('Confirm Email', sender='secapp.devs@gmail.com', recipients=[email])
    link = url_for('confirm_email', token=token, _external=True)
    msg.body = 'Your link is {}'. format(link)
    mail.send(msg)
	
    return '<h1> The email you endered is {}. The token is {} </h1>' .format(email, token)
		


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp
    
if __name__ == "__main__":
    app.run(host='127.0.0.1')
