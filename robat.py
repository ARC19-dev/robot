import sys
from PyQt5.QtWidgets import (QApplication, QWidget, 
                             QPushButton, QLabel, QLineEdit)
import time
import speech_recognition as sr
import pyttsx3
import numpy
import cv2

recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 140)
voices = engine.getProperty('voices')  
engine.setProperty('voice', voices[1].id)

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.setGeometry(1000,350,300,300)
        self.setWindowTitle('Hello')
        self.Titlebox = QLineEdit(self)
        self.Titlebox.resize(100, 20)
        self.Titlebox.move(100, 120)
        
        self.btn_exit = QPushButton('exit', self)
        self.btn_exit.resize(50, 20)
        self.btn_exit.move(150, 170)
        self.btn_exit.clicked.connect(lambda : self.close())
        
        self.btn_robat = QPushButton('robat', self)
        self.btn_robat.resize(50, 20)
        self.btn_robat.move(100, 150)
        self.btn_robat.clicked.connect(self.robat)

        self.btn_voice_robat = QPushButton('voice', self)
        self.btn_voice_robat.resize(50, 20)
        self.btn_voice_robat.move(150, 150)
        self.btn_voice_robat.clicked.connect(self.voice_robat)

        self.btn_capture = QPushButton('webcam', self)
        self.btn_capture.resize(50, 20)
        self.btn_capture.move(100, 170)
        self.btn_capture.clicked.connect(self.capture)        

    def voice_robat(self):
        with sr.Microphone() as source:
            try:
                recognizer.adjust_for_ambient_noise(source)
                audio_text = recognizer.listen(source)
                self.robat(audio_text=recognizer.recognize_google(audio_text))

            except:
                engine.say('Sorry')
                engine.say('Say again')
                engine.runAndWait()
        

    def robat(self, *, audio_text=None):
        if audio_text is None:
            text = self.Titlebox.text()
        else:
            text = audio_text

        if text in ('Salam', 'salam', 'set alarm', 'alarm'):
            engine.say('Salam aref')
            engine.runAndWait()

        elif text == 'hello':
            engine.say('Hello My friend')
            engine.runAndWait()

        elif text == 'how are you':
            engine.say('Im find')
            engine.runAndWait()

        elif text == 'how old are you':
            engine.say('I was before you were born')
            engine.runAndWait()

    def capture(self):
        ip = self.Titlebox.text()
        port = ':4747'
        url = 'http://' + ip + port + '/mjpegfeed?640x480'
        cap = cv2.VideoCapture(url)
        
        while True:
            _ , frame = cap.read()
            cv2.imshow('frame', frame)
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())    