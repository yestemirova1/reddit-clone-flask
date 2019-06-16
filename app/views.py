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


def get_user():
    response = makeGetRequest('/api/v1/me/')

    if response.status_code == 200:
        user = response.json()

    return user


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


def short_url(str):
    s = str[8:24] + '...'
    return s


def get_subreddit_icon(subreddit):

    s = '/r/' + subreddit + '/about/'
    response = makeGetRequest(s)

    if response.status_code == 200:
        icon = response.json()['data']['icon_img']

    return icon


def format_date(date):
    ts = dt.utcfromtimestamp(date)
    return (ts.strftime('%B %d, %Y'))


@app.route("/", methods=["GET"])
def index():

    response = makeGetRequest('/hot')
    user = get_user()

    if response.status_code == 200:
        children = response.json()['data']['children']

    return render_template("index.html", children=children,
                           human_format=human_format, time_ago=time_ago,
                           endsw=endsw, get_subreddit_icon=get_subreddit_icon,
                           user=user, short_url=short_url)


@app.route("/profile")
def profile():
    user = get_user()
    s = '/user/' + user['name'] + '/overview'
    response = makeGetRequest(s)

    if response.status_code == 200:
        data = response.json()['data']['children']

    return render_template("profile.html", user=user, data=data,
                           time_ago=time_ago, short_url=short_url,
                           format_date=format_date)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form['query']
    q = '/search/?q=' + query
    response = makeGetRequest(q)
    user = get_user()

    if response.status_code == 200:
        results = response.json()['data']['children']

    return render_template('search_results.html', results=results, q=query, human_format=human_format, time_ago=time_ago, endsw=endsw, get_subreddit_icon=get_subreddit_icon, user=user)


@app.route("/sign_in")
def sign_in():
    return render_template('sign_in.html')


@app.route("/history")
def history():
    user = get_user()
    s = '/user/' + user['name'] + '/submitted'
    s1 = '/user/' + user['name'] + '/comments'
    s2 = '/user/' + user['name'] + '/upvoted'
    s3 = '/user/' + user['name'] + '/downvoted'
    s4 = '/user/' + user['name'] + '/hidden'
    s5 = '/user/' + user['name'] + '/saved'
    s6 = '/user/' + user['name'] + '/gilded'

    response = makeGetRequest(s)
    r1 = makeGetRequest(s1)
    r2 = makeGetRequest(s2)
    r3 = makeGetRequest(s3)
    r4 = makeGetRequest(s4)
    r5 = makeGetRequest(s5)
    r6 = makeGetRequest(s6)

    data = response.json()['data']['children']
    d1 = r1.json()['data']['children']
    d2 = r2.json()['data']['children']
    d3 = r3.json()['data']['children']
    d4 = r4.json()['data']['children']
    d5 = r5.json()['data']['children']
    d6 = r6.json()['data']['children']

    return render_template("history.html", user=user, data=data,
                           d1=d1, d2=d2, d3=d3, d4=d4, d5=d5, d6=d6,
                           time_ago=time_ago, short_url=short_url,
                           format_date=format_date)


@app.route("/r/<subreddit>/comments/<id>/<title>/")
def comments(subreddit, id, title):
    response = makeGetRequest(
        '/r/' + subreddit + '/comments/' + id + '/' + title + '/')
    user = get_user()

    if response.status_code == 200:
        data = response.json()

    d_post = data[0]['data']['children'][0]['data']
    d_comments = data[1]['data']['children']

    return render_template("comments1.html", d_post=d_post, d_comments=d_comments,
                           is_str=is_str, user=user, human_format=human_format,
                           get_subreddit_icon=get_subreddit_icon, time_ago=time_ago,
                           endsw=endsw)
