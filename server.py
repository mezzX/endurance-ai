from flask import Flask
from flask import request
from endurance_ai import *


app = Flask(__name__)

@app.route('/')
def run_app():
    startDate = str(request.args.get('startDate'))
    endDate = str(request.args.get('endDate'))
    numPerWeek = int(request.args.get('numPerWeek'))
    fitnessLevel = int(request.args.get('fitnessLevel'))
    goalDistance = int(request.args.get('goalDistance'))
    sport = str(request.args.get('sport'))
    numDays, startDay, dayOfWeek = getNumDays(startDate, endDate)
    schedule = makeSchedule(numDays, startDay, dayOfWeek, numPerWeek, fitnessLevel, goalDistance, sport)
    return json.dumps(schedule)