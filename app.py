from flask import Flask, render_template, request

person_tracker = None

class Person(object):
    def __init__(self):
        self.steps = 0

    def add_step(self):
        self.steps = self.steps + 1;

    def get_step(self):
        return self.steps;


app = Flask(__name__)

@app.route('/step')
def forward():
    person_tracker.add_step()
    return str(person_tracker.get_step())

if __name__ == '__main__':
    person_tracker = Person()
    app.debug = True
    app.run(host = '0.0.0.0',port=5000)
