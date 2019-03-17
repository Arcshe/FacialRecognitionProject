from camera_pi import Camera
from flask import Flask
from flask import make_response
from flask import request
from flask import render_template
from flask import Response
from flask import send_file
import time
import os
import io

app = Flask(__name__)

@app.route('/')
def index():
    timeNow = time.asctime(time.localtime(time.time()))
    templateData = {
        'time': timeNow
    }
    return render_template('index.html', **templateData)

@app.route('/Face_GetData',methods=['GET','POST'])
def GetData():
    timeNow = time.asctime(time.localtime(time.time()))
    templateData = {
        'time': timeNow 
    }
    return render_template('Face_GetData.html', **templateData)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/Face_GetData/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/Face_Recognition')
def Recognition():
    timeNow = time.asctime(time.localtime(time.time()))
    templateData = {
        'time': timeNow
    }
    return render_template('Face_Recognition.html', **templateData)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port =5040, debug=True, threaded=True)
    

