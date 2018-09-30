import json
import datetime
import calendar
import random

def read_json(file_name):
    with open(file_name) as json_data:
        f = json.load(json_data)
        return f


def getNumDays(startDate, endDate):
    startString = startDate.split('-')
    startY = int(startString[0])
    startM = int(startString[1])
    startD = int(startString[2])
    start = datetime.date(startY, startM, startD)

    endString = endDate.split('-')
    endY = int(endString[0])
    endM = int(endString[1])
    endD = int(endString[2])
    end = datetime.date(endY, endM, endD)

    days = end - start
    return days.days, start, start.weekday()


def roundTime(time):
    return(5 * round(time / 5))


def addWorkout(dayOfWeek, numPerWeek, startDate, day, numDays, fitnessLevel, goalDistance, sportNum):
    plan = {2 : {5:'interval', 6:'recovery'},
            3 : {2:'interval', 5:'endurance', 6:'recovery'},
            4 : {2:'interval', 3:'recovery', 5:'endurance', 6:'recovery'},
            5 : {1:'interval', 2:'recovery', 3:'interval', 5:'endurance', 6:'recovery'},
            6 : {1:'interval', 2:'recovery', 3:'interval', 4:'recovery', 5:'endurance', 6:'recovery'},
    }

    max_ = {0 : {'interval' : 60, 'recovery' : 30, 'endurance' : 180},
            1 : {'interval' : 20, 'recovery' : 10, 'endurance' : 60},
            2 : {'interval' : 120, 'recovery' : 60, 'endurance' : 360}
    }

    min_ = {0 : 15,
            1 : 30,
            2 : 30
    }

    days = list(calendar.day_name)
    dayDelta = datetime.timedelta(days=day)
    date = startDate + dayDelta

    if dayOfWeek in plan[numPerWeek].keys():
        workout = plan[numPerWeek][dayOfWeek]
        startLevel = float(fitnessLevel) / 100.
        increaseLevel = (1. - startLevel) * (day / numDays)
        intensity = roundTime(min_[sportNum] + 
            (startLevel + increaseLevel) * (max_[sportNum][workout] - min_[sportNum]))
        data = [str(date), workout, intensity]
        return data

    else:
        return [str(date)]


def makeSchedule(numDays, startDay, dayOfWeek, numPerWeek, fitnessLevel, goalDistance, sport):
    dayOfWeek = dayOfWeek
    sports = ['running', 'swimming', 'cycling']
    days = {}
    sportNum = 0
    for day in range(0, numDays):
            if sport == 'ironman':
                sportNum +=1
                if sportNum > 2:
                    sportNum = 0
            data = addWorkout(dayOfWeek, numPerWeek, startDay, day, numDays,
                       fitnessLevel, goalDistance, sportNum)
            if len(data) > 1:
                print(sports[sportNum] + str(data))
                days[data[0]] = [{'sport' : sports[sportNum],
                                 'type' : data[1],
                                 'duration' : data[2]
                }]

            else:
                days[data[0]] = []


            if dayOfWeek == 7:
                dayOfWeek = 0

            else:
                dayOfWeek += 1

    return days


def main(fileName):
    f = read_json(fileName)
    startDate = f['startDate']
    endDate = f['endDate']
    numPerWeek = f['numPerWeek']
    fitnessLevel = f['fitnessLevel']
    goalDistance = f['goalDistance']
    #goalTime = f['goalTime']
    sport = f['sport']
    numDays, startDay, dayOfWeek = getNumDays(startDate, endDate)
    makeSchedule(numDays, startDay, dayOfWeek, numPerWeek, fitnessLevel, goalDistance, sport)



if __name__ == '__main__':
    main('sample.json')