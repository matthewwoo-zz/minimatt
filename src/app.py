import httplib2
import requests
from flask import request
from googleapiclient import discovery
import flask
from flask import Flask
from src import medium
from src.models.calendar import Calendar
from src.get_creds import get_credentials


app = Flask(__name__)
app.secret_key = 'super secret key'

@app.route('/')
def home():
    print "request going through"
    return "<p>Running</p>"

@app.route('/slots', methods=['GET'])
def slots():
    credentials = get_credentials()
    http_auth = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http_auth)
    cal = Calendar()
    today = cal.date_range()
    busy_slots = cal.busy_slots(service=service, body=today)
    slots = cal.potential_slot(5)
    free_slots = []
    i = 0
    while i <= 7:
        if cal.check_slot(slots[i], busy_slots):
            i += 1
        free_slots.append(slots[i])
        i += 1
    json_slots = cal.post_dates(free_slots)
    print json_slots
    return flask.jsonify(json_slots)


@app.route('/meeting', methods=['GET', 'POST'])
def meeting():
    if request.method == 'POST':
        r = request.form
        name = r['fullName']
        topic = r['topic']
        email = r['email']
        setattr(flask.g,'fullName', name)
        print getattr(flask.g, 'fullName')
        print r
    if request.method == 'GET':
        pass
    return 200

# @app.route('/meetingdetails', methods=['POST'])
# def meetingdetails():
#     x = getattr(flask.g, 'fullName')
#     print x
#     return 200


@app.route('/newevent')
def event():
    credentials = get_credentials()
    http_auth = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http_auth)
    cal = Calendar()
    cal.create_event(service=service)
    return 200


@app.route('/posts', methods=['GET'])
def posts():
    posts = medium.get_posts(5)
    print flask.jsonify(posts)
    return flask.jsonify(posts)


@app.route('/test', methods=['GET'])
def test():
    x = {"messages": [{"text": "Welcome to our store!"},{"text": "How can I help you?"}]}
    return flask.jsonify(x)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
