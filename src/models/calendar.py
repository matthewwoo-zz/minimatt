import datetime
import json

class Calendar(object):

    def __init__(self):
        pass

    def date_range(self):
        raw_end = datetime.datetime.utcnow() + datetime.timedelta(days=7)
        start = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S-08:00")
        end = raw_end.strftime("%Y-%m-%dT%H:%M:%S-08:00")

        body = {
            "timeMin": start,
            "timeMax": end,
            "items": [{"id": "matthew.edan.woo@gmail.com"}, {"id":"matt@ujet.co"}]
        }
        return body

    def busy_slots(self, body, service):
        eventsResult = service.freebusy().query(body=body).execute()
        personal_dict = eventsResult[u'calendars'][u'matthew.edan.woo@gmail.com']
        work_dict = eventsResult[u'calendars'][u'matt@ujet.co']

        busy_slots = []

        for i in personal_dict[u'busy']:
            raw_date = i[u'start'][:18]
            formatted_date = datetime.datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%S")
            busy_slots.append(formatted_date)

        for i in work_dict[u'busy']:
            raw_date = i[u'start'][:18]
            formatted_date = datetime.datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%S")
            busy_slots.append(formatted_date)
        # print x == datetime.datetime(2016,11,28,5,0,0)
        return busy_slots

    def free_slots(self):
        pass

    def potential_slot(self):
        raw_slot_day = datetime.datetime.now() + datetime.timedelta(days=1)

        if raw_slot_day.weekday() == 5:
            raw_slot_day = datetime.datetime.now() + datetime.timedelta(days=2)
        elif raw_slot_day.weekday() == 6:
            raw_slot_day = datetime.datetime.now() + datetime.timedelta(days=1)

        raw_morning_slot = raw_slot_day.replace(hour=9, minute=0, second=0)
        morning_slot = datetime.datetime.strftime(raw_morning_slot, "%Y-%m-%dT%H:%M:%S")

        raw_evening_slot = raw_slot_day.replace(hour=13, minute=0, second=0)
        evening_slot = datetime.datetime.strftime(raw_evening_slot, "%Y-%m-%dT%H:%M:%S")

        potential_slots = [morning_slot, evening_slot]
        return potential_slots

    def check_slot(self, slot, slot_list):
        for i in slot_list:
            if i == slot:
                return True
            return False





        # slot = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S-08:00")
        #
        #
        # the_datetime2 = the_datetime + datetime.timedelta(hours=1)
        # the_datetime1a = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S-08:00")



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