# IoT Introductory Health App

## Background

Built in a class at the University of California, Irvine, the project was a paired programming assignment to use an arduino to make any kind of IoT application/ prodcut.

Our team opted to reproduce a fitbit style product that logs data about it's user (heart rate, PPG etc) and then uploads it to a corresponding frontend that provides analytics on the collected data, also in realtime.

- An arduino with plugged in sensors was used to sample user data
- A frontend written in Flask, Bootstrap and corresponding analytics charts in Highcharts, visualised the data

## Running the Code

- Clone this repo
- The code held in directory "ESP wifi module" can be run on a physical arduino with connected sensors to fire off data to a given endpoint
- Execute "python app.py" in your terminal to run the server to receive and visualise your data in real time 

## Promo

See a live demo of the project [here](https://youtu.be/HeflH-PmvFk)
