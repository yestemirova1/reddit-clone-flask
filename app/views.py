from app import app

from flask import render_template, request, redirect, jsonify, make_response
from urllib.request import urlopen, Request
from datetime import datetime as dt, timedelta

import requests
import requests.auth
import timeago
from html.parser import HTMLParser

APP_ID = 'jGRIZbqhFLnQdg'
APP_SECRET = '5niyUIvV6noyFrotJuDOKXovtkQ'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5)'


def makeGetRequest(api_url):
    base_url = 'https://www.reddit.com/'
    data = {'grant_type': 'password',
            'username': 'yestemirova', 'password': 'Password1R'}
    auth = requests.auth.HTTPBasicAuth(APP_ID, APP_SECRET)
    r = requests.post(base_url + 'api/v1/access_token', data=data,
                      headers={'user-agent': USER_AGENT}, auth=auth)
    d = r.json()

    token = 'bearer ' + d['access_token']

    base_url = 'https://oauth.reddit.com'

    headers = {'Authorization': token, 'User-Agent': USER_AGENT}
    response = requests.get(base_url + api_url, headers=headers)

    return response


def human_format(num):
    magnitude = 0
    if num >= 1000:
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        return '%.1f%s' % (num, ['', 'k'][magnitude])
    else:
        return num


def endsw(str):
    if str.endswith('.jpg'):
        return True
    elif str.endswith('.png'):
        return True
    elif str.endswith('.jpeg'):
        return True
    elif str.endswith('.gif'):
        return True
    else:
        return False


def time_ago(timestamp):
    now = dt.now() + timedelta(seconds=60 * 3.4)

    date = dt.fromtimestamp(timestamp)

    return timeago.format(date, now)

def is_str(obj):
    return isinstance(obj, str)

def get_subreddit_icon(subreddit):

    s = '/r/'+ subreddit +'/about/'
    response = makeGetRequest(s)

    if response.status_code == 200:
        icon = response.json()['data']['icon_img']

    return icon


@app.route("/", methods=["GET"])
def index():

    response = makeGetRequest('/hot')

    if response.status_code == 200:
        children = response.json()['data']['children']

    return render_template("index.html", children=children, human_format=human_format, time_ago=time_ago, endsw=endsw, get_subreddit_icon=get_subreddit_icon)


@app.route("/profile/<username>")
def profile(username):
    return render_template("profile.html", name=username)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form['query']
    q = '/search/?q='+query
    response = makeGetRequest(q)

    if response.status_code == 200:
        results = response.json()['data']['children']

    return render_template('search_results.html', results=results, q=query, human_format=human_format, time_ago=time_ago, endsw=endsw, get_subreddit_icon=get_subreddit_icon)



@app.route("/sign_in")
def sign_in():
    return render_template('sign_in.html')


@app.route("/r/<subreddit>/comments/<id>/<title>/")
def comments(subreddit, id, title):

    response = makeGetRequest('/r/'+ subreddit +'/comments/'+ id +'/'+ title +'/')

    if response.status_code == 200:
        data = response.json()

    d_post = data[0]['data']['children'][0]['data']
    d_comments = data[1]['data']['children']

    return render_template("comments1.html", d_post=d_post, d_comments=d_comments, is_str=is_str)
