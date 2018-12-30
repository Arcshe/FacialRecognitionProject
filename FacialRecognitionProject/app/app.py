from flask import Flask, render_template, Response
import time
import os

app = Flask(__name__)

@app.route('/')
def index():
    timeNow = time.asctime(time.localtime(time.time()))
    templateData = {
        'time': timeNow
    }
    return render_template('index.html', **templateData)

@app.route('/Face_GetData')
def GetData():
    timeNow = time.asctime(time.localtime(time.time()))
    templateData = {
        'time': timeNow 
    }
    return render_template('Face_GetData.html', **templateData)

@app.route('/Get')
def gen():
    os.popen("python Face_GetData.py")
    os.popen("kill -9 $(ps -aux|grep Face_GetData.py|awk '{print $2}')")


@app.route('/Face_Recognition')
def Recognition():
    timeNow = time.asctime(time.localtime(time.time()))
    templateData = {
        'time': timeNow
    }
    return render_template('Face_Recognition.html', **templateData)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)

