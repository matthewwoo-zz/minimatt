import time


class Post(object):
    def __init__(self, title, reading_time, subtitle, url):
        self.title = title,
        self.reading_time = reading_time
        self.subtitle = subtitle,
        self.url = 'https://medium.com/@matthewedanwoo/%s' % url

    def json(self):
        title = unicode(self.title).strip("(),' "" ")
        title = title[:79]
        subtitle = unicode(self.subtitle).strip("(),'")
        subtitle = subtitle[:79]
        reading_time = round(float(unicode(self.reading_time).strip("(),")),2)
        return {
            'title': title,
            'reading_time': reading_time,
            'subtitle': subtitle,
            'url': self.url
        }

