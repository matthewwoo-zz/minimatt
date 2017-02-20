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

        return busy_slots

    def potential_slot(self,x):
        potential_slots = []
        i = 0
        while i < x:
            raw_slot_day = datetime.datetime.now() + datetime.timedelta(days=i)

            if raw_slot_day.weekday() == 5:
                raw_slot_day = datetime.datetime.now() + datetime.timedelta(days=2)
            elif raw_slot_day.weekday() == 6:
                raw_slot_day = datetime.datetime.now() + datetime.timedelta(days=1)

            raw_morning_slot = raw_slot_day.replace(hour=9, minute=0, second=0)
            morning_slot = datetime.datetime.strftime(raw_morning_slot, "%Y-%m-%dT%H:%M:%S")

            raw_evening_slot = raw_slot_day.replace(hour=13, minute=0, second=0)
            evening_slot = datetime.datetime.strftime(raw_evening_slot, "%Y-%m-%dT%H:%M:%S")

            potential_slots.extend([morning_slot,evening_slot])
            i += 1
        return potential_slots[2:]

    def check_slot(self, slot, slot_list):
        for i in slot_list:
            if i == slot:
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
            cal_slot = free_slots[i]
            raw_slot = datetime.datetime.strptime(free_slots[i], '%Y-%m-%dT%H:%M:%S')
            slot = datetime.datetime.strftime(raw_slot,'%A, %B %d - %I:%M %p')
            date = {
                "title": slot,
                "buttons": [
                    {
                        "type": "json_plugin_url",
                        "url": "http://ab365d25.ngrok.io/newevent/%s" % cal_slot,
                        "title": "Book Time"
                    }
                ]
            }
            date_header['messages'][0]['attachment']['payload']['elements'].append(date)
            i += 1
        return date_header

    def create_event(self, service, name, topic, email, start):
        start_time = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
        end_time = start_time + datetime.timedelta(hours=1)
        event = {
            'summary': "Chat: %s <> Matt" % name,
            'location': 'Google Hangout',
            'description': 'Chat about %s' % topic,
            'start': {
                'dateTime': start_time,
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'America/Los_Angeles',
            },
            'attendees': [
                {'email': 'matthew.edan.woo@gmail.com'},
                {'email': email}
            ],
            'reminders': {
                'useDefault': True
            },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        print 'Event created: %s' % (event.get('htmlLink'))