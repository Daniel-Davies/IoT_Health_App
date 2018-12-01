from flask import Flask, render_template, request
import datetime
from datetime import timedelta

person_tracker = None

class Person(object):
    def __init__(self):
        self.steps = [datetime.datetime(2018,2,2,3), datetime.datetime(2018,2,13,6), datetime.datetime(2018, 11,25)]
        
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
    return [1]

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
        if (prevDate.month < week_ago.month and prevDate.day < week_ago.day):
            break
        diff = datetime.datetime.today() - prevDate #this is a semi-full timedelta value
        numStepsPerDay[diff.days] += 1
    return(days,numStepsPerDay)

def today():
    return [1]


@app.route('/test')
def test():
    print(week())
    week()
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
