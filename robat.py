import os
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, 
                             QPushButton, QLabel, QLineEdit, QVBoxLayout)

from PyQt5.QtGui import QPixmap
from PyQt5.Qt import Qt
import time
import pytube
import webbrowser
import speech_recognition as sr
import pyttsx3
import numpy
import cv2

recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 140)
voices = engine.getProperty('voices')  
engine.setProperty('voice', voices[1].id)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Robat'
        self.left = 1000
        self.top = 350
        self.width = 626
        self.height = 424
        self.style_sheet = """

                QWidget {
                        background-color: #222222;
                }

                QLineEdit {
                        background-color: aliceblue;
                        color: #a64dff;
                        font-style: italic;
                        font-weight: bold;
                        border-radius: 5px;
                }

                QPushButton {
                        background-color: #8b0000;
                        color: #ffffff;
                        font-style: italic;
                        border-radius: 5px;
                        border-style: none;
                        height: 25px;
                } 
                        
                QPushButton:hover {
                            background: transparent;
                } 
        
                    """
        self.setup()
        
    def setup(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.setMaximumSize(self.width, self.height)
        self.setMinimumSize(self.width, self.height)
        self.setStyleSheet(self.style_sheet) 
                                        
        self.setWindowTitle(self.title)
        self.image = QLabel(self)
        self.image.setPixmap(QPixmap('robot.jpg'))
        self.image.resize(626, 424)
        self.Titlebox = QLineEdit(self)
        self.Titlebox.resize(170, 25)
        self.Titlebox.move(230, 180)
        self.Titlebox.setMaxLength(50)
        self.Titlebox.returnPressed.connect(self.robat)

        self.btn_exit = QPushButton('exit', self)
        self.btn_exit.resize(70, 30)
        self.btn_exit.move(320, 260)
        self.btn_exit.clicked.connect(lambda : self.close())
        
        self.btn_robat = QPushButton('robat', self)
        self.btn_robat.resize(70, 30)
        self.btn_robat.move(240, 220)
        self.btn_robat.clicked.connect(self.robat)

        self.btn_voice_robat = QPushButton('voice', self)
        self.btn_voice_robat.resize(70, 30)
        self.btn_voice_robat.move(320, 220)
        self.btn_voice_robat.clicked.connect(self.voice_robat)

        self.btn_capture = QPushButton('webcam', self)
        self.btn_capture.resize(70, 30)
        self.btn_capture.move(240, 260)
        self.btn_capture.clicked.connect(self.capture)        

    def voice_robat(self):
            
            try:
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source)
                    audio_text = recognizer.listen(source)
                    text = recognizer.recognize_google(audio_text)
                    self.robat(audio_text=text)

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
            engine.say('Salam Aref')
            engine.runAndWait()

        elif text == 'hello':
            engine.say('Hello My friend')
            engine.say('How Rosette passed ?')
            engine.runAndWait()

        elif text == 'Yes, I had a good day':
            engine.say('OK')
            engine.runAndWait()
            
        elif text == 'how are you':
            engine.say('Im find')
            engine.runAndWait()

        elif text == 'how old are you':
            engine.say('I was before you were born')
            engine.runAndWait()
        
        elif text.split()[0] in ('google', 'Google', 'bmbgk'):   # google search
            engine.say('OK')
            engine.runAndWait()
            google_text = ''
            google_search = text.split()[1:]
            
            for search in google_search:
                google_text += search
                google_text += ' '
            webbrowser.open('http://bmbgk.ir/?q={0}'.format(google_text))


        elif text.split()[0] in ('youtube', 'Youtube'):   # youtube search 
            engine.say('OK')
            engine.runAndWait()
            youtube_search = text.split()[1:]
            youtube_text = ''
            
            if youtube_search == []:
                webbrowser.open('https://www.youtube.com/')
            else:
                for search in youtube_search:
                    youtube_text += search
                    youtube_text += ' '
                webbrowser.open('https://www.youtube.com/results?search_query={0}'.format(youtube_text))
        
        elif text.split('/')[2] == 'youtu.be':   # download youtube
            url = self.Titlebox.text()
            path = 'C:\\Users\\User\\Desktop\\Download Youtube'
            engine.say('Download now')
            engine.runAndWait()
            try:
                if os.path.isdir(path):
                    youtube = pytube.YouTube(url)
                    video = youtube.streams.first()
                    video.download(path)
                else:
                    os.mkdir(path)
                    youtube = pytube.YouTube(url)
                    video = youtube.streams.first()
                    video.download(path)

                engine.say('Finished download')
                engine.runAndWait()
            
            except:
                    engine.say("I can't download")
                    engine.say('You must use a VPN')
                    engine.runAndWait()

    def capture(self):
        '''
            You need to install the droidcam on android or ios
        '''
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