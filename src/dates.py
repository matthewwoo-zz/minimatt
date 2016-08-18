import random
import time
import datetime

def strTimeProp(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))

def randomDate(start, end, prop):
    return strTimeProp(start, end, '%m/%d/%Y', prop)

def date_list(x):
    i = 0
    list = []
    while i < x:
        date = str(randomDate("8/19/2016", "8/23/2016", random.random()))
        list.append(date)
        i += 1
    list = sorted(list, key=lambda list: map(int, list.split('/')))
    return list

def int_list(x):
    i = 0
    integers = []
    while i < x:
        hour = random.randint(1,5)
        integers.append(hour)
        i += 1
    integers = sorted(integers, key=int)
    return integers


def get_dates(x):
    date_header = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [

                ]
            }
        }
    }
    i = 0
    list = date_list(x)
    integers = int_list(x)
    while i < x:
        date = {
            "title": str(list[i]) + ' at ' + str(integers[i]) + ':00 PM',
            "buttons": [
                {
                    "type": "show_block",
                    "block_name": "Sent",
                    "title": "Book Time"
                }
            ]
        }
        date_header['attachment']['payload']['elements'].append(date)
        i += 1
    return date_header







