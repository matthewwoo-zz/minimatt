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
                print i
                print type(i)
                return True
            return False

    def post_dates(self, free_slots):
        date_header = {
            "messages": [
                {
                    "attachment": {
                        "type": "template",
                        "payload": {
                            "template_type": "generic",
                            "elements": []
                        }
                    }
                }
            ]
        }
        i = 0
        num_slots = len(free_slots)
        while i < num_slots:
            slot = datetime.datetime.strptime(free_slots[i], '%Y-%m-%dT%H:%M:%S')
            slot = datetime.datetime.strftime(slot,'%A, %B %d - %I:%M %p')
            print slot
            date = {
                "title": slot,
                "buttons": [
                    {
                        "type": "show_block",
                        "block_name": "Sent",
                        "title": "Book Time"
                    },
                    {
                        "type": "json_plugin_url",
                        "url": "http://3d8dc4c5.ngrok.io/newevent",
                        "title": "Create Event"
                    }
                ]
            }
            date_header['messages'][0]['attachment']['payload']['elements'].append(date)
            i += 1
        return date_header

    def create_event(self, service):
        event = {
            'summary': 'Google I/O 2015',
            'location': '800 Howard St., San Francisco, CA 94103',
            'description': 'A chance to hear more about Google\'s developer products.',
            'start': {
                'dateTime': '2017-03-26T09:00:00-08:00',
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': '2017-03-27T17:00:00-08:00',
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