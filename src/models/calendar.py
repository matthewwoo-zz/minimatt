import datetime

class Calendar(object):

    def __init__(self):
        pass

    def get_freebusy(self, service):
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

    def calendar_list(self, service):
        calendar = service.calendars().get(calendarId='primary').execute()
        print calendar
        print calendar['summary']


    def create_event(self, service):
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