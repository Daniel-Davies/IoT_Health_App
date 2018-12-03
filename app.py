from flask import Flask, render_template, request
import datetime
from datetime import timedelta

person_tracker = None

class Person(object):
    def __init__(self):
        self.steps = [datetime.datetime(2018,2,2,3), datetime.datetime(2018,2,13,6), datetime.datetime(2018,10,31), datetime.datetime(2018, 11,24),datetime.datetime(2018, 11,25)]
        
    def add_step(self):
        self.steps.append(datetime.datetime.now())

    def get_step(self):
        return self.steps;


app = Flask(__name__)


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
    return (weeks,numStepsPerWeek)



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
    return(days,numStepsPerDay)

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

        if (prevDate.month != hour_ago.month or prevDate.day != hour_ago.day or diffInHour > 8):
            break
        print(diffInHour)
        
        numStepsPerHour[diffInHour] += 1
    return(hours, numStepsPerHour)


def heartRate():
    #assuming person has a heartDictionary
    # k = 0 - 23
    # v = [] <- list of heart beats
    times = [i for i in range(24)]
    avgHeartBeats = [0 for _ in range(24)]    
    heartBeats = person_tracker.get_heart() #dictionary
    for key in range(24):
        countHeartBeat, sumHearBeat = 0,0
        for heartBeat in heartBeats[key]:
            countHeartBeat += 1
            sumHearBeat += heartBeat
        avgHeartBeats[key] = sumHearBeat/countHeartBeat
    return (times, avgHeartBeats)  


@app.route('/test')
def test():
    print(today())
    return render_template("google_but_better.html")


@app.route('/retrieve_steps/<int:timeframe>')
def retrieve_steps(timeframe):
    if (timeframe == 0):
        return month()
    elif (timeframe == 1):
        return week()
    else:
        return today()


@app.route('/heart', methods=["POST"])
def heart_counter():
    pass


if __name__ == '__main__':
    person_tracker = Person()
    app.debug = True
    app.run(host = '0.0.0.0',port=5000)
