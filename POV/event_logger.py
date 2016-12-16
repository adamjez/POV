import os
import datetime

class EventLogger:
    def __init__(self, filename):
        self.filename = filename
        self.events = []

    def save(self):
        with open(self.filename, 'w') as file:
            for event in self.events:
                file.write(event)

    def addEvent(self, time, eventType, description):
        # Python implicitly add 1 hear in from timestamp 
        eventDatetime = datetime.datetime.fromtimestamp(time/1000.0) - + datetime.timedelta(hours=1)
        event = '{:%H:%M:%S.%f} {} {}'.format(eventDatetime, eventType, description)
        self.events.append(event)

    def addTouch(self, time, dummyId):
        self.addEvent(time, "TOUCH", str(dummyId))

    def addGoal(self, time, playerId):
        self.addEvent(time, "GOAL", str(playerId))