from flask import Flask, render_template, request, jsonify
import datetime
from datetime import timedelta
import random
import atexit
import pickle

person_tracker = None

class Person(object):
    def __init__(self):
        self.steps = [datetime.datetime(2018,2,2,3), datetime.datetime(2018,2,13,6), datetime.datetime(2018,10,31), datetime.datetime(2018, 11,24),datetime.datetime(2018, 11,25), datetime.datetime.today()]
        self.heart = {}
        self.lastHeart = 0
        self.lastTime = datetime.datetime.now()

    def get_heart(self):
        return self.heart

    def add_step(self):
        self.steps.append(datetime.datetime.now())

    def add_heart(self, key, value):
        self.lastHeart = value
        self.lastTime = datetime.datetime.now()
        if (key in self.heart):
            self.heart[key].append(value)
        else:
            self.heart[key] = [value]

    def get_step(self):
        return self.steps;

    def getLastBeat(self):
        return [self.lastHeart, " " + str(self.lastTime.hour) + ":" + str(self.lastTime.minute) + ":" + str(self.lastTime.second)]


app = Flask(__name__)

@app.route('/live_heart')
def live():
    return jsonify(person_tracker.getLastBeat())

@app.route('/step')
def forward():
    person_tracker.add_step()
    return str(person_tracker.get_step())

def month():
    today = datetime.datetime.today()
    month_ago = today - datetime.timedelta(days=30) #this is a full datetime value
    weeks = [0,0,0,0]
    numStepsPerWeek = [0,0,0,0]

    for i in range(4):
        prevWeek = today - datetime.timedelta(days = i * 7)
        weeks[i] = str(prevWeek.month) + '/' + str(prevWeek.day) + '/' + str(prevWeek.year)

    for prevDate in person_tracker.get_step()[::-1]:
        #anytime the month gets too far back and the day is too far back
        if(prevDate.month< month_ago.month or (prevDate.month == month_ago.month and prevDate.day <= month_ago.day)):
            break
        diff = datetime.datetime.today() - prevDate
        numStepsPerWeek[diff.days // 7] += 1
    return jsonify([weeks,numStepsPerWeek])



def week():
    today = datetime.datetime.today()
    week_ago = today - datetime.timedelta(days=7) #this is a full datetime value
    days = [0,0,0,0,0,0,0] #will get updated the different day values.
    numStepsPerDay = [0,0,0,0,0,0,0]

    #setup the days to the correct
    for i in range(7):
        prevDay = today - datetime.timedelta(days = i)
        days[i] = str(prevDay.month) + '/' + str(prevDay.day) + '/' + str(prevDay.year)

    #iterating through the getting of the steps and go from right to left
    for prevDate in person_tracker.get_step()[::-1]:
        if (prevDate.month < week_ago.month or (prevDate.month == week_ago.month and prevDate.day <= week_ago.day)):
            break
        diff = datetime.datetime.today() - prevDate #this is a semi-full timedelta value
        numStepsPerDay[diff.days] += 1
    return jsonify([days,numStepsPerDay])

def today():
    today = datetime.datetime.today()
    hour_ago = today - datetime.timedelta(hours=8)
    hours = [0 for _ in range(8)]
    numStepsPerHour = [0 for _ in range(8)]

    for i in range(8):
        prevHour = today - datetime.timedelta(hours = i)
        ampm = 'pm' if (prevHour.hour//12) else 'am'
        hr = prevHour.hour if (prevHour.hour == 12) else prevHour.hour%12
        hours[i] = str(prevHour.month) + '/' + str(prevHour.day) + ' : ' + str(hr) + ' ' + ampm
    for prevDate in person_tracker.get_step()[::-1]:
        diff = datetime.datetime.today() - prevDate
        diffInHour = int(diff.total_seconds() // 3600)
        print(diffInHour)
        print(prevDate.month)
        print(hour_ago.month)
        print(prevDate.day)
        print(hour_ago.day)
        if (prevDate.month != hour_ago.month or diffInHour > 8):
            break
        print(diffInHour)

        numStepsPerHour[diffInHour] += 1
    print([hours,numStepsPerHour])
    return jsonify([hours, numStepsPerHour])

def heartRate():
    today = datetime.datetime.today()
    times = [0 for _ in range(24)]

    for i in range(24):
        prevHour = today - datetime.timedelta(hours = i)
        ampm = 'pm' if (prevHour.hour//12) else 'am'
        hr = prevHour.hour if (prevHour.hour == 12) else prevHour.hour%12
        times[i] = str(prevHour.month) + '/' + str(prevHour.day) + ' : ' + str(hr) + ' ' + ampm

    #assuming person has a heartDictionary
    # k = 0 - 23
    # v = [] <- list of heart beats
    avgHeartBeats = [0 for _ in range(24)]
    heartBeats = person_tracker.get_heart() #dictionary
    for key,val in heartBeats.items():
    	countHeartBeat, sumHearBeat = 0,0
    	for hb in val:
    		countHeartBeat += 1
    		sumHearBeat += hb
    	avgHeartBeats[key] = sumHearBeat/countHeartBeat
    return [times, avgHeartBeats]

@app.route('/test')
def test():
    weeks = week()
    return render_template("google_but_better.html", data=weeks)


@app.route('/retrieve_steps/<int:timeframe>')
def retrieve_steps(timeframe):
    if (timeframe == 2):
        return (month())
    elif (timeframe == 1):
        return (week())
    else:
        return (today())


@app.route('/heart', methods=["POST"])
def heart_counter():
    x = (request.data)
    x = str(x, 'utf-8')
    x = x.split()
    person_tracker.add_heart(datetime.datetime.now().hour, float(x[1]))
    person_tracker.lastHeart = x[1]
    return str(5)

@app.route('/chart_heart')
def chartHeart():
    return jsonify(heartRate())

def goodbye():
    with open("heart", "wb") as f:
        pickle.dump(person_tracker.heart,f)

    with open("steps", "wb") as f:
        pickle.dump(person_tracker.steps,f)

if __name__ == '__main__':
    person_tracker = Person()
    atexit.register(goodbye)
    app.debug = True
    app.run(host = '0.0.0.0',port=5000)
