import datetime


class Event(object):

    def __init__(self):
        self.summary,
        self.description,
        self.start,
        self.end,
        self.attendees,
        self.reminders

    # def get_freebusy(slot):
    #     the_datetime = datetime.datetime.utcnow()
    #     the_datetime2 = the_datetime + datetime.timedelta(hours=1)
    #     the_datetime1a = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S-08:00")
    #     the_datetime2a = the_datetime2.strftime("%Y-%m-%dT%H:%M:%S-08:00")
    #
    #     body = {
    #         "timeMin": the_datetime1a,
    #         "timeMax": the_datetime2a,
    #         "items": [{"id": "matthew.edan.woo@gmail.com"}, {"id": "matt@ujet.co"}]
    #     }
    #
    #     eventsResult = service.freebusy().query(body=body).execute()
    #     cal_dict = eventsResult[u'calendars']
    #     for cal_name in cal_dict:
    #         print(cal_name, cal_dict[cal_name])

    def potential_slots(x):

        # Generate time slots between 1:00 - 2:00pm and 5:00 - 5:30pm on weekdays
        today = datetime.datetime.now()
        while today.weekday() > 4 and today.weekday() < 6:
            today = datetime.timedelta(days=1)
        start_day = today + datetime.timedelta(days=1)

        period_1_start_hour = 1
        period_1_end_minutes = 30

        period_2_start_hour = 5
        period_2_end_minutes = 30

        i = 0
        slot_list = []
        while i < x:
            slot_1_start = datetime.datetime(
                start_day.year,
                start_day.month,
                start_day.day,
                period_1_start_hour,
            )

            slot_1_end = datetime.datetime(
                start_day.year,
                start_day.month,
                start_day.day,
                period_1_end_minutes
            )

            if get_freebusy(slot_1_start, slot_1_end) == True:
                ...

            slot1 = slot.strftime("%Y-%m-%dT%H:%M:%S-08:00")


            slot_list.append(slot)



            i += 1





            = datetime.datetime(start_day.year, start_day.month, start_day.day, 8)
        time_period_2 = datetime.datetime



            start = today + datetime.timedelta(days=1)
            start = start.

        the_datetime = datetime.datetime.utcnow()
        the_datetime2 = the_datetime + datetime.timedelta(hours=1)
        the_datetime1a = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S-08:00")
        the_datetime2a = the_datetime2.strftime("%Y-%m-%dT%H:%M:%S-08:00")



    def avaialble_slots(x):
        slots = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [

                    ]
                }
            }
        }
        list = Event.potential_slots()
        i = 0
        while i < x:
            date = {
                "title": str(list[i]),
                "buttons": [
                    {
                        "type": "show_block",
                        "block_name": "Sent",
                        "title": "Book Time"
                    }
                ]
            }
            slots['attachment']['payload']['elements'].append(date)
            i += 1
        return slots

    def create_event(self, guest, guest_email, description, start, end):
        event = {
            'summary': 'Chat: {},Matt'.format(guest),
            'location': 'Skype',
            'description': '{}'.format(description),
            'start': {
                'dateTime': '{}'.format(start),
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': '{}'.format(end),
                'timeZone': 'America/Los_Angeles',
            },
            'attendees': [
                {'email': 'matthew.edan.woo@gmail.com'},
                {'email': '{}'.format(guest_email)}
            ],
            'reminders': {
                'useDefault': True
            },
        }
        event = service.events().insert(calendarId='primary', body=event).execute()
        return True



    def calendar_list():
        calendar = service.calendars().get(calendarId='primary').execute()
        print calendar
        print calendar['summary']


    get_freebusy()
    calendar_list()
    create_event()