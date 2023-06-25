import sys
from PyQt5.QtWidgets import QApplication,QMessageBox,QDialog
from PyQt5.QtCore import QThread,pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
import pyttsx3
import speech_recognition as sr
import webbrowser
import wikipedia
import os
from datetime import datetime
import random
import cv2
from playsound import playsound

class CommandThread(QThread):
    # Define a signal to update the text browser
    update_text_browser_4 = pyqtSignal(str)
    update_text_browser_3 = pyqtSignal(str)
    update_text_browser = pyqtSignal(str)
    def __init__(self, recognizer, microphone, parent=None):
        super().__init__(parent)
        self.fazeel = pyttsx3.init('sapi5')
        self.voice = self.fazeel.getProperty('voices')
        self.fazeel.setProperty('voices',self.voice[0].id)
        self.recognizer = recognizer
        self.microphone = microphone
    def run(self):
        self.wishme()
        while True:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                    self.update_text_browser_4.emit("Listening....")
                    r.pause_threshold = 1
                    r.energy_threshold=5000
                    r.dynamic_energy_adjustment_damping = 0.01
                    audio = r.listen(source)
            # Try to recognize the voice command
            try:
                self.update_text_browser_4.emit("Recognizing....")
                text = r.recognize_google(audio,language="en-in")
                self.update_text_browser.emit(text)
                text = text.lower()
                if("how are you") in text:
                        sp = "I'm Good Sir!"
                        self.update_text_browser_3.emit(sp)
                        self.speak(sp)
                elif("detect my face") in text:
                        self.update_text_browser_3.emit("Opening CV2 to Detect...")
                        self.speak("Opening CV2 to Detect...")
                        self.face_detect()
                elif("detect my eyes") in text:
                        self.update_text_browser_3.emit("Opening CV2 to Detect...")
                        self.speak("Opening CV2 to Detect...")
                        self.eye_detect()
                elif("detect my body") in text:
                        self.update_text_browser_3.emit("Opening CV2 to Detect...")
                        self.speak("Opening CV2 to Detect...")
                        self.body_detect()
                elif("open google") in text:
                        self.update_text_browser_3.emit("Opening Google...")
                        self.speak("Opening Google")
                        webbrowser.open("www.google.com")
                elif("play song") in text:
                        loc = "D:\\Songs\\New folder"
                        songs = os.listdir(loc)
                        try:
                            i = random.randint(0,len(songs))
                            self.update_text_browser_3.emit("Playing Song...")
                            self.speak("Playing Song")
                            os.startfile(os.path.join(loc,songs[i]))
                            if("abort song") in text:
                                os.kill()
                        except Exception as e:
                            i = random.randint(0,len(songs))
                            os.startfile(os.path.join(loc,songs[i]))
                elif("wikipedia") in text:
                        wk = text.replace("wikipedia","")
                        wk = wikipedia.summary(wk,sentences=2)
                        self.update_text_browser_3.emit("According To Wikipedia: ",wk)
                        self.speak("According to wikipedia: "+wk)
                if ("stop") in text:
                    self.speak("As You Wish")
                    break
            except sr.UnknownValueError:
                self.update_text_browser_3.emit("Couldn't  understand you")
                self.speak("Couldn't understand you")
            except sr.WaitTimeoutError:
                
                self.update_text_browser_3.emit("I think you are not connected to the internet")
                self.speak("I think you are not connected to the internet")
    def speak(self,audio):
            self.fazeel.say(audio)
            self.fazeel.runAndWait()
    def face_detect(self):
        file_loc = "haarcascade_frontalface_default.xml"
        fil_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+file_loc )
        webcam = cv2.VideoCapture(0)
        while True:
            succ_fra,frame = webcam.read()
            frame_grayscale = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            face_coordinates = fil_cascade.detectMultiScale(frame_grayscale)
            for (x,y,w,h) in face_coordinates:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
            cv2.imshow("Window",frame)
            key = cv2.waitKey(1)
            if key == ord("q"):
                    break
        webcam.release()
        cv2.destroyAllWindows()

    def body_detect(self):
        fil_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_fullbody.xml" )
        webcam = cv2.VideoCapture(0)
        while True:
            succ_fra,frame = webcam.read()
            frame_grayscale = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            face_coordinates = fil_cascade.detectMultiScale(frame_grayscale,scaleFactor=1.4,minNeighbors=20)
            for (x,y,w,h) in face_coordinates:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
            cv2.imshow("Window",frame)
            key = cv2.waitKey(1)
            if key == ord("q"):
                    break
        webcam.release()
        cv2.destroyAllWindows()

    def eye_detect(self):
        face_detec = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml")
        eye_detec = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_eye.xml")
        video = cv2.VideoCapture(0)
        while True: 
            succ_frame,frame = video.read()
            frame_gra = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            faces = face_detec.detectMultiScale(frame_gra)
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                the_face = frame[y:y+h,x:x+w]
                face_grascale= cv2.cvtColor(the_face,cv2.COLOR_BGR2GRAY)
                eyes = eye_detec.detectMultiScale(face_grascale,scaleFactor=1.7,minNeighbors=20)
                for(x_,y_,w_,h_) in eyes:
                    cv2.rectangle(the_face,(x_,y_) ,(x_+w_ ,y_+h_),(255,255,255),2)
            cv2.imshow("Eyes_Detection",frame)
            key =cv2.waitKey(1)
            if key == ord("q"):
                break
            
        video.release()
        cv2.destroyAllWindows()
    def wishme(self):
        hour = int(datetime.now().hour)
        if(hour>0 and hour<12):                                                                                         
            sp = "Good Morning Sir!"
            self.update_text_browser_3.emit("Good Morning Sir!")
            self.speak(sp)
        elif(hour>12 and hour<18):
            sp ="Good Afternoon Sir!"
            self.update_text_browser_3.emit("Good Afternoon Sir!")
            self.speak(sp)
        elif(hour>18 and hour <24):
            sp = "Good Evening Sir!"
            self.update_text_browser_3.emit("Good Evening Sir!")
            self.speak(sp)

class my_app(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("Jarvis.ui",self)
        self.Jar_but.clicked.connect(self.start_command)
        
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Initialize the command thread
        self.command_thread = CommandThread(self.recognizer, self.microphone)
        self.command_thread.update_text_browser_4.connect(self.update_text_browser_4)
        self.command_thread.update_text_browser_3.connect(self.update_text_browser_3)
        self.command_thread.update_text_browser.connect(self.update_text_browser)
    def start_command(self):
        playsound("D:\Programming\Python Files\Python_QtPy\\btn.mp3")
        self.command_thread.start()
    def update_text_browser_4(self, text):
        self.textBrowser_4.setText(text)
    def update_text_browser_3(self,text):
        self.textBrowser_3.setText(text)
    def update_text_browser(self,text):
        self.textBrowser_2.setText(text)
if __name__ =="__main__":
    app = QApplication(sys.argv)
    win = my_app()
    win.show()
    win.setWindowIcon(QIcon("Prog.ico"))
    sys.exit(app.exec_())