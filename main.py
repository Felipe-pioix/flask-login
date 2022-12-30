from flask import Flask, request, render_template,session, redirect,url_for
from flask_login import LoginManager,UserMixin,login_required,login_user,current_user,logout_user

app = Flask(__name__)

app.secret_key = b'cf4efd72536836f4725189ff9d71b98a93365f436b12e12abed170418a97dfd7'

login_manager = LoginManager()
login_manager.init_app(app)

# Our mock database.
users = {'foo@bar.tld': {'password': 'secret'}}

# defino el objeto User que hereda de UserMixin y nada mas (el pass es un codigo vacio que no da error)
class User(UserMixin):
    pass 

#This sets the callback for reloading a user from the session. The function you set should take a user ID (a str) and return a user object, or None if the user does not exist.
@login_manager.user_loader
def user_loader(email):
    print("user_loader")
    if email not in users:
        return
    user = User()
    user.id = email
    return user

#This sets the callback for loading a user from a Flask request. The function you set should take Flask request object and return a user object, or None if the user does not exist.
@login_manager.request_loader
def request_loader(request):
    print("request_loader")
    email = request.form.get('email')
    if email not in users:
        return
    user = User()
    user.id = email
    return user

#This will set the callback for the unauthorized method, which among other things is used by login_required. It takes no arguments, and should return a response to be sent to the user instead of their normal view.
@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'no estas autarizado', 401


'''This is the reason why you shoud use request_loader with flask_login.

There will be a lot of @login_required from flask_login used in your api to guard the request access.
You need to make a request to pass the check of auth.

And there will be a lot of current_user imported from flask_login,
Your app need to use them to let the request act as the identity of the current_user.

There are two ways to achieve the above with flask_login.

Using user_loader makes the request to be OK for @login_required.
It is often used for UI logins from browser.
It will store session cookies to the browser and use them to auth later.
So you need to login only once and the session will keep for a time.

Using request_loader will also be OK with @login_required.
But it is often used with api_key or basic auth.
For example used by other apps to interact with your flask app.
There will be no session cookies,
so you need to provide the auth info every time you send request.

With both user_loader and request_loader,
now you got 2 ways of auth for the same api,
protected by @login_required,
and with current_user usable,
which is really smart.'''


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    if email in users and request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        login_user(user)
        return redirect(url_for('userHome'))

    return 'Bad login'

@app.route('/userHome')
@login_required
def userHome():
	return render_template('userHome.html', user=current_user.id)

@app.route('/logout')
def logout():
    logout_user()
    return render_template('logout.html')
@app.route('/')
def home():
		return render_template('home.html')


if __name__ == "__main__":
	app.run()
