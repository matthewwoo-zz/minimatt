import httplib2
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

@app.route('/slots')
def slots():
    credentials = get_credentials()
    http_auth = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http_auth)
    cal = Calendar()
    today = cal.date_range()
    busy_slots = cal.busy_slots(service=service, body=today)
    slots = cal.potential_slot()
    free_slots = []
    i = 0
    while i <= 1:
        if cal.check_slot(slots[i], busy_slots):
            i += 1
        free_slots.append(slots[i])
        i += 1
    json_slots = cal.post_dates(free_slots)
    return flask.jsonify(json_slots)

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
    print "what's up"
    posts = medium.get_posts(5)
    print flask.jsonify(posts)
    return flask.jsonify(posts)


@app.route('/test', methods=['GET'])
def test():
    x = {"messages": [{"text": "Welcome to our store!"},{"text": "How can I help you?"}]}
    return flask.jsonify(x)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
