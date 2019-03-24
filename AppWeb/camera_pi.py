import io
import cv2
import time
import threading
import picamera
import numpy as np

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('Face_Trainer.yml')
cascadePath = "frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
font = cv2.FONT_HERSHEY_SIMPLEX
names = ['None','liyuxiang','huge','Ilza','Z','w']


class Camera(object):
    thread = None
    frame = None
    last_access = 0

    def initialize(self): 
        if Camera.thread is None:
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            while self.frame is None:
                time.sleep(0)

    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return self.frame

    @classmethod
    def _thread(cls):
        id = 0
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            camera.hflip = True
            camera.vflip = True

            camera.start_preview()
            time.sleep(2)

            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg', 
                                                 use_video_port = True):
                data = np.fromstring(stream.getvalue(), dtype=np.uint8)
                image = cv2.imdecode(data, cv2.IMREAD_UNCHANGED)

                image = cv2.flip(image, -1)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                faces = faceCascade.detectMultiScale(
                    gray,
                    scaleFactor = 1.2,
                    minNeighbors = 5,
                    minSize = (64, 48),
                    )

                for(x,y,w,h) in faces:
                    cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)
                    id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

                    if (confidence < 100):
                        id = names[id]
                        confidence = "   {0}%".format(round(100-confidence))
                    else:
                        id = "unknown"
                        confidence = "   {0}%".format(round(100-confidence))

                    cv2.putText(image, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
                    cv2.putText(image, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)
                cv2.imshow("camera", image)
                k = cv2.waitKey(100) & 0xff
            

                stream.seek(0)
                cls.frame = stream.read()

                stream.seek(0)
                stream.truncate()

                if k == 27:
                    break
            cv2.destroyAllWindows()

        cls.thread = None
