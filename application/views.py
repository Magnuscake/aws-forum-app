from flask import Blueprint, render_template, redirect, url_for, session

from .decorators import login_required

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def default():
    return redirect(url_for('auth.login'))

@views.route('/user')
@login_required
def user_area():
    return render_template('user.html', username=session['user_info']['username'])

@views.route('/subscription')
@login_required
def subscription():
    return render_template('subscription.html')

@views.route('/query')
@login_required
def query_area():
    return render_template('query.html')

