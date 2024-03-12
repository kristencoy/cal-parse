class Event:
    def __init__(self, title, start, end):
        self.title = title
        self.start = start
        self.end = end

    
    def createAllDayEvent(self):
        event = {
            'summary': self.title,
            'start': {
                'date': self.start,
            },
            'end': {
                'date': self.end
            },
        }
        print(event)

    def createTimeEvent(self):
        event = {
            'summary': self.title,
            'start': {
                'dateTime': self.start,
            },
            'end': {
                'dateTime': self.end
            },
        }
        print(event)