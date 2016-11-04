import json

import flask
from flask import Flask, request

from src import medium, dates

app = Flask(__name__)

@app.route('/')
def start():
    return "<p>test</p>"

@app.route('/posts', methods=['GET'])
def posts():
    posts = medium.get_posts(3)
    return flask.jsonify(posts)

@app.route('/times', methods=['GET'])
def times():
    date_list = dates.get_dates(3)
    return flask.jsonify(date_list)

@app.route('/re_auth', methods=['GET','POST'])
def auth():
    if request.method == 'GET':
        print "Get method"
        return "<p>Get method executed</p>"
    elif request.method == 'POST':
        print "Post method"
    print "nothing happened"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
