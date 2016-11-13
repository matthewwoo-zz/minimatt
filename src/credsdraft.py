import os

import datetime
import httplib2
from oauth2client import client, tools
from oauth2client.file import Storage
from googleapiclient.discovery import build


SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = '/Users/mattw/Dropbox/Programming/MiniWooBot/client_secret.json'
REDIRECT_URI = 'https://e909201b.ngrok.io/re_auth/'

def get_credentials():
    home_dir = os.path.expanduser('/Users/mattw/Dropbox/Programming/MiniWooBot')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,'script-python.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES,REDIRECT_URI)
        flow.user_agent = "Test App"
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to' + credential_path)
    return credentials

credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
service = build('calendar','v3', http=http)

def get_freebusy():
    the_datetime = datetime.datetime.utcnow()
    the_datetime2 = the_datetime + datetime.timedelta(hours=1)
    the_datetime1a = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S-08:00")
    the_datetime2a = the_datetime2.strftime("%Y-%m-%dT%H:%M:%S-08:00")

    body = {
        "timeMin": the_datetime1a,
        "timeMax": the_datetime2a,
        "items": [{"id": "matthew.edan.woo@gmail.com"}, {"id":"matt@ujet.co"}]
    }

    eventsResult = service.freebusy().query(body=body).execute()
    cal_dict = eventsResult[u'calendars']
    for cal_name in cal_dict:
        print(cal_name, cal_dict[cal_name])

def calendar_list():
    calendar = service.calendars().get(calendarId='primary').execute()
    print calendar
    print calendar['summary']


def create_event():
    event = {
        'summary': 'Google I/O 2015',
        'location': '800 Howard St., San Francisco, CA 94103',
        'description': 'A chance to hear more about Google\'s developer products.',
        'start': {
            'dateTime': '2016-11-30T09:00:00-08:00',
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': '2016-11-30T17:00:00-08:00',
            'timeZone': 'America/Los_Angeles',
        },
        'attendees': [
            {'email': 'matthew.edan.woo@gmail.com'},
            {'email': 'matt@ujet.co', 'responseStatus':'accepted'}
        ],
        'reminders': {
            'useDefault': True
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print 'Event created: %s' % (event.get('htmlLink'))


get_freebusy()
calendar_list()
create_event()
