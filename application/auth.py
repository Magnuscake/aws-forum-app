from flask import (
    Blueprint, request, render_template, redirect, url_for, flash, session
)

from .dynamodb.user import (
    put_user, login_user, key_exists, attr_exists
)

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form

        email = data.get('email')
        username = data.get('username')
        password1 = data.get('password1')
        password2 = data.get('password2')

        if (not email or len(email) < 2):
            flash('Please enter a valid email', category='error')
        elif (not username or len(username) < 3):
            flash('Please enter a valid username', category='error')

        # Uniquness checks
        elif (key_exists('email', email)):
            flash("This email already exists", category='error')
        elif (attr_exists('username', username)):
              flash("This username already exists", category='error')

        elif (password1 == '' or password2 == ''):
            flash("Please enter a valid password", category='error')
        elif (password1 != password2):
            flash("Passwords do not match", category='error')
        else:
            put_user(email, username, password1)
            flash("Account has been successfully been created", category='success')
            return redirect(url_for('auth.login'))

    return render_template('register.html', title="Register")

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form

        email = data.get('email')
        password = data.get('password')

        user = login_user(email, password)

        if user:
            flash("Login successful", category='success')
            session['user_info'] = user
            session['logged_in'] = True
            return redirect(url_for('views.user_area'))

        else:
            flash("ID or password is invalid", category='error')

    return render_template('login.html', title="Login")

@auth.route('/logout')
def logout():
    # Reset session token
    session.pop('user_info', None)
    session['logged_in'] = False
    return redirect(url_for('auth.login'))
