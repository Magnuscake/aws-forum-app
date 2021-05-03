from flask import Blueprint, request, render_template, redirect, url_for, session

from .decorators import login_required
from application.dynamodb.music import get_music_on_query
from .dynamodb.subscription import (
    get_subscriptions, put_subscription, delete_subscription
)

views = Blueprint('views', __name__)

@views.route('/')
def root():
    if session['logged_in']:
        return redirect(url_for('views.user_area'))
    return redirect(url_for('auth.login'))

@views.route('/user')
@login_required
def user_area():
    return render_template('user.html', username=session['user_info']['username'])

@views.route('/subscription')
@login_required
def subscription_area():
    username = session['user_info']['username']
    user_subscriptions = get_subscriptions(username)

    return render_template('subscription.html', subscriptions=user_subscriptions)

@views.route('/query', methods=['GET', 'POST'])
@login_required
def query_area():
    query_results = get_music_on_query()

    if request.method == 'POST':
        data = request.form

        artist = data.get('artist')
        title = data.get('title')
        year = data.get('year')

        query_results = get_music_on_query(artist, title, year)

    return render_template('query.html', query_results=query_results)


@views.route('/add', methods = ['POST', 'PUT'])
def add_subscription():
    username = session['user_info']['username']
    title = request.args.get('title', None)
    artist = request.args.get('artist', None)
 
    put_subscription(username, title, artist)

    return redirect(url_for('views.query_area'))

@views.route('/remove', methods = ['POST', 'DELETE'])
def remove_subscription():
    username = session['user_info']['username']
    title = request.args.get('title', None)

    delete_subscription(username, title)

    return redirect(url_for('views.subscription_area'))


