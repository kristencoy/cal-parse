class Event:
    def __init__(self, title, start, end):
        self.title = title
        self.start = start
        self.end = end
    
    def createAllDayEvent(self):
        event = {
            'summary': self.title,
            'start': {
                'date': str(self.start)
            },
            'end': {
                'date': str(self.end)
            },
            'colorId': 2
        }
        return event

    def createTimeEvent(self):
        event = {
            'summary': self.title,
            'start': {
                'dateTime': self.start,
                'timeZone': 'America/New_York'
            },
            'end': {
                'dateTime': self.end,
                'timeZone': 'America/New_York'
            },
            'colorId': 1
        }
        return event