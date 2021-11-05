"""
BSD 3-Clause License

Copyright (c) 2021, Muhammed Bassiouni
All rights reserved.


# Note: you have to install opencv, use the following:
    >> pip install opencv-python==3.4.2.16 
the new version of opencv with this example causes unexpected problems

"""

import cv2
import base64
import os
import photongui
from photongui import Util


util = Util()
util.exposeAll("faceEyeDetection", locals())

indexFile = os.path.join(os.path.dirname(__file__), "view/index.html")

settings = {
    "view":indexFile
}
window = photongui.createWindow(settings)


class capture():
    def __init__(self, optionsSelected):
        self.faceSelected = optionsSelected[0]
        self.eyeSelected = optionsSelected[1]
        self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye_tree_eyeglasses.xml")
        self.ok = True
    
    def draw_found(self, detected, image, color: tuple):
        for (x, y, width, height) in detected:
            cv2.rectangle(
                image,
                (x, y),
                (x + width, y + height),
                color,
                thickness=2
            )

    def genImg(self):
        if self.faceSelected and self.eyeSelected:
            while self.ok:
                _, image = self.video.read()
                image = cv2.flip(image, 1)
                grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                detected_faces = self.face_cascade.detectMultiScale(image=grayscale_image, scaleFactor=1.3, minNeighbors=4)
                detected_eyes = self.eye_cascade.detectMultiScale(image=grayscale_image, scaleFactor=1.3, minNeighbors=4)
                self.draw_found(detected_faces, image, (0, 0, 255))
                self.draw_found(detected_eyes, image, (0, 255, 0))
                _, jpeg = cv2.imencode('.jpg', image)
                jpgBytes = jpeg.tobytes()
                self.getImg(jpgBytes)

        elif self.faceSelected and not self.eyeSelected:
            while self.ok:
                _, image = self.video.read()
                image = cv2.flip(image, 1)
                grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                detected_faces = self.face_cascade.detectMultiScale(image=grayscale_image, scaleFactor=1.3, minNeighbors=4)
                self.draw_found(detected_faces, image, (0, 0, 255))
                _, jpeg = cv2.imencode('.jpg', image)
                jpgBytes = jpeg.tobytes()
                self.getImg(jpgBytes)
            
        elif not self.faceSelected and self.eyeSelected:
            while self.ok:
                _, image = self.video.read()
                image = cv2.flip(image, 1)
                grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                detected_eyes = self.eye_cascade.detectMultiScale(image=grayscale_image, scaleFactor=1.3, minNeighbors=4)
                self.draw_found(detected_eyes, image, (0, 255, 0))
                _, jpeg = cv2.imencode('.jpg', image)
                jpgBytes = jpeg.tobytes()
                self.getImg(jpgBytes)
                
        else:
            while self.ok:
                _, image = self.video.read()
                image = cv2.flip(image, 1)
                _, jpeg = cv2.imencode('.jpg', image)
                jpgBytes = jpeg.tobytes()
                self.getImg(jpgBytes)


        self.video.release()
        cv2.destroyAllWindows()

    def getImg(self, jpgBytes):
        imageBase64 = base64.b64encode(jpgBytes)
        imageDecoded = imageBase64.decode("utf-8")
        window.execJsAsync(f"updateImageSrc('{imageDecoded}')")

def startVideo(optionsSelected):
    global videoRun
    videoRun = capture(optionsSelected)
    videoRun.genImg()

def stopVideo():
    videoRun.ok = False


if __name__ == "__main__":
    photongui.start(debug=True)
    