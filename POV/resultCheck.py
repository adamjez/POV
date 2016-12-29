import sys
from datetime import datetime

####################
# FILE DESCRIPTION #
####################
# Every line is one EVENT with space separated informations:
# 1. Line stars with time of event in format: %H:%M:%S.%f
# 2. Type of event, one of these values: GOAL, TOUCH
# 3a. For GOL event there will be id of player: 1 or 2
# 3b. For TOUCH event there will be line id indexed from left and id of dummy indexed from top separeted with comma, for example: 1,3  
#     which mean that dummy on first line and third from top touched the ball
# Example: sample_output.txt

TIME_TOLERANCE = 1500  # Tolerance in ms for same events


def millis_interval(start, end):
    """start and end are datetime instances"""
    diff = end - start
    millis = diff.days * 24 * 60 * 60 * 1000
    millis += diff.seconds * 1000
    millis += diff.microseconds / 1000
    return millis


class resultCheck(object):
    """description of class"""

    def __init__(self, correctOutputPath, scriptOutputPath):
        self.correctOutputPath = correctOutputPath
        self.scriptOutputPath = scriptOutputPath
        self.missedEvents = []
        self.addedEvents = []
        self.correctEvents = []
        self.correctEventsCount = 0
        self.scriptEventsCount = 0

    def run(self):
        try:
            with open(self.correctOutputPath) as correctFile:
                with open(self.scriptOutputPath) as scriptFile:
                    correctLines = [line.rstrip('\n') for line in correctFile]
                    scriptLines = [line.rstrip('\n') for line in scriptFile]

                    loadNewCorrectLine = True
                    loadNewScriptLine = True
                self.correctEventsCount = len(correctLines)
                self.scriptEventsCount = len(scriptLines)
                while len(correctLines) > 0 or len(scriptLines) > 0:
                    if loadNewScriptLine and len(scriptLines) > 0:
                        (time2, type2, id2) = self.parseLine(scriptLines.pop(0))
                    if loadNewCorrectLine and len(correctLines) > 0:
                        (time, type, id) = self.parseLine(correctLines.pop(0))

                    loadNewCorrectLine = True
                    loadNewScriptLine = True

                    deltaTime = abs(millis_interval(time, time2))

                    if deltaTime < TIME_TOLERANCE:
                        if type == type2 and id == id2:
                            self.correctEvents.append((type, deltaTime))
                            print("Correct event detected: " + type)
                        else:
                            if time2 < time:
                                loadNewCorrectLine = False
                                self.addedEvents.append((time2, type2))
                            else:
                                loadNewScriptLine = False
                                self.missedEvents.append((time, type))

                            if id == id2:
                                print("Missinterpreted event: " + type + " missed id (" + str(deltaTime) + ")")
                            elif type == type2:
                                print(
                                    "Bad ids for event type: " + type + " given: " + id2 + " instead of: " + id + " (" + str(
                                        deltaTime) + ")")
                            else:
                                print("Different event at given time: " + type + " instead of " + type2 + " (" + str(
                                    deltaTime) + ")")
                    elif time2 < time:
                        self.addedEvents.append((time2, type2))
                        loadNewCorrectLine = False

                    else:
                        self.missedEvents.append((time, type))
                        loadNewScriptLine = False

                if len(correctLines) > len(scriptLines):
                    print("Correct file have some events but script file doesn't")
                    for line in correctLines:
                        (time, type, id) = self.parseLine(line)
                        self.missedEvents.append((time, type))

                if len(scriptLines) > len(correctLines):
                    print("Script file have some events but correct file doesn't")
                    for line in scriptLines:
                        (time, type, id) = self.parseLine(line)
                        self.addedEvents.append((time, type))
        except FileNotFoundError:
            print("Skipping result check because file not exists")

    def printResult(self):
        print("Result Check Completed!")

        correctEventCount = len(self.correctEvents)
        timeDiff = 0
        if correctEventCount != 0:
            timeDiff = sum([x[1] for x in self.correctEvents]) / correctEventCount

        print("Events count: " + str(self.correctEventsCount) + " (correct) " + str(
            self.scriptEventsCount) + " (script result)")
        print("Correct events: " + str(correctEventCount) + " time differs: " + str(timeDiff) + " ms" +  
              " (Touch: " + str(len([x for x in self.correctEvents if x[0] == "TOUCH"])) + 
              ", Goal: " + str(len([x for x in self.correctEvents if x[0] == "GOAL"])) + ")")

        print("Missed events: " + str(len(self.missedEvents)) 
              + " (Touch: " + str(len([x for x in self.missedEvents if x[1] == "TOUCH"])) 
              + ", Goal: " + str(len([x for x in self.missedEvents if x[1] == "GOAL"])) + ")")

        print("Added events: " + str(len(self.addedEvents)) 
              + " (Touch: " + str(len([x for x in self.addedEvents if x[1] == "TOUCH"])) 
              + ", Goal: " + str(len([x for x in self.addedEvents if x[1] == "GOAL"])) + ")")

    def parseLine(self, line):
        parts = line.split()

        time = datetime.strptime(parts[0], "%H:%M:%S.%f")
        type = parts[1]
        id = parts[2]
        return (time, type, id)


if __name__ == "__main__":
    check = resultCheck(sys.argv[1], sys.argv[2])
    check.run()
    check.printResult()
