import sys
from PyQt5.QtWidgets import QApplication, QMessageBox, QDialog
from PyQt5.QtCore import QThread, pyqtSignal
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
        self.fazeel.setProperty('voices', self.voice[0].id)
        self.recognizer = recognizer
        self.microphone = microphone

    def run(self):
        self.wishme()
        while True:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                self.update_text_browser_4.emit("Listening....")
                r.pause_threshold = 1
                r.energy_threshold = 5000
                r.dynamic_energy_adjustment_damping = 0.01
                audio = r.listen(source)
            # Try to recognize the voice command
            try:
                self.update_text_browser_4.emit("Recognizing....")
                text = r.recognize_google(audio, language="en-in")
                self.update_text_browser.emit(text)
                text = text.lower()
                if "how are you" in text:
                    sp = "I'm Good Sir!"
                    self.update_text_browser_3.emit(sp)
                    self.speak(sp)
                elif "detect face" in text:
                    self.update_text_browser_3.emit("Opening CV2 to Detect...")
                    self.speak("Opening CV2 to Detect...")
                    self.face_detect()
                elif "open google" in text:
                    self.update_text_browser_3.emit("Opening Google...")
                    self.speak("Opening Google")
                    webbrowser.open("www.google.com")
                elif "play song" in text:
                    loc = "D:\\Songs\\New folder"
                    songs = os.listdir(loc)
                    try:
                        i = random.randint(0, len(songs))
                        self.update_text_browser_3.emit("Playing Song...")
                        self.speak("Playing Song")
                        os.startfile(os.path.join(loc, songs[i]))
                        if "abort song" in text:
                            os.kill()
                    except Exception as e:
                        i = random.randint(0, len(songs))
                        os.startfile(os.path.join(loc, songs[i]))
                elif "wikipedia" in text:
                    wk = text.replace("wikipedia", "")
                    wk = wikipedia.summary(wk, sentences=2)
                    self.update_text_browser_3.emit("According To Wikipedia: ", wk)
                    self.speak("According to wikipedia: " + wk)
                if "stop" in text:
                    self.speak("As You Wish")
                    break
            except sr.UnknownValueError:
                self.update_text_browser_3.emit("Couldn't  understand you")
                self.speak("Couldn't understand you")
            except sr.WaitTimeoutError:
                self.update_text_browser_3.emit("I think you are not connected to the internet")
                self.speak("I think you are not connected to the internet")

    def speak(self, audio):
        self.fazeel.say(audio)
        self.fazeel.runAndWait()

    def face_detect(self):
        file_loc = "haarcascade_frontalface_default.xml"
        fil_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + file_loc)
        webcam = cv2.VideoCapture(0)
        while True:
            succ_fra, frame = webcam.read()
            frame_grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_coordinates = fil_cascade.detectMultiScale(frame_grayscale)
            for (x, y, w, h) in face_coordinates:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.imshow("Window", frame)
            key = cv2.waitKey(1)
            if key == ord("q"):
                break
        webcam.release()

    @staticmethod
    def body_detect():
        file_loc = "haarcascade_fullbody.xml"
        fil_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + file_loc)
        webcam = cv2.VideoCapture(0)
        while True:
            succ_fra, frame = webcam.read()
            frame_grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_coordinates = fil_cascade.detectMultiScale(frame_grayscale, scaleFactor=1.4, minNeighbors=20)
            for (x, y, w, h) in face_coordinates:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.imshow("Window", frame)
            key = cv2.waitKey(1)
            if key == ord("q"):
                break
        webcam.release()

    def eye_detect(self):
        file_loc = "haarcascade_frontalface_default.xml"
        eye_loc = "haarcascade_eye.xml"
        fil_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + file_loc)
        eye_Cascades = cv2.CascadeClassifier(cv2.data.haarcascades + eye_loc)
        webcam = cv2.VideoCapture(0)
        while True:
            succ_fra, frame = webcam.read()
            frame_grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_coordinates = fil_cascade.detectMultiScale(frame_grayscale, scaleFactor=1.4, minNeighbors=20)
            for (x, y, w, h) in face_coordinates:
                cv2.rectangle(frame, (x, y), (x + w, y + h), 0)
                the_face = frame[y:y + h, x:x + w]
                eye_gray = cv2.cvtColor(the_face, cv2.COLOR_BGR2RGB)
                eye_coordinates = eye_Cascades.detectMultiScale(eye_gray)
                for (x_, y_, w_, h_) in eye_coordinates:
                    cv2.rectangle(the_face, (x_, y_), (x_ + w_, y_ + h_), (0, 0, 0), 3)
            cv2.imshow("Window", frame)
            key = cv2.waitKey(1)
            if key == ord("q"):
                break
        webcam.release()

    def wishme(self):
        self.update_text_browser_3.emit("Welcome back!")
        self.speak("Welcome back!")
        hour = datetime.now().hour
        if 0 <= hour < 12:
            self.update_text_browser_3.emit("Good Morning Sir")
            self.speak("Good Morning Sir")
        elif 12 <= hour < 18:
            self.update_text_browser_3.emit("Good Afternoon Sir")
            self.speak("Good Afternoon Sir")
        else:
            self.update_text_browser_3.emit("Good Evening Sir")
            self.speak("Good Evening Sir")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QDialog()
    ui = loadUi("Jarvis.ui", window)
    ui.setWindowIcon(QIcon("jarvis.png"))
    window.setWindowTitle("Jarvis Assistant")
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    command_thread = CommandThread(recognizer, microphone)
    command_thread.update_text_browser.connect(ui.textBrowser_2.append)
    command_thread.update_text_browser_3.connect(ui.textBrowser_3.append)
    command_thread.update_text_browser_4.connect(ui.textBrowser_4.append)
    ui.Jar_but.clicked.connect(command_thread.start)
    window.show()
    sys.exit(app.exec_())