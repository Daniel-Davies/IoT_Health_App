from flask import Flask, render_template, request
import datetime
from datetime import timedelta

person_tracker = None

class Person(object):
    def __init__(self):
        self.steps = []

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
    week_ago = today - datetime.timedelta(days=7)
    print(week_ago)
    return [1]

def today():
    return [1]

@app.route('/test')
def test():
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
