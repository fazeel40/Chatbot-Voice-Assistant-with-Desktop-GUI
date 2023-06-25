import pyttsx3
import webbrowser
import os
import wikipedia
import speech_recognition as sr
import cv2
from datetime import datetime
import random

fazeel = pyttsx3.init('sapi5')
voice = fazeel.getProperty('voices')
fazeel.setProperty('voices',voice[0].id)

def speak(audio):
    fazeel.say(audio)
    fazeel.runAndWait()

def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.adjust_for_ambient_noise(source)
        r.listen_in_background=False
        r.energy_threshold=500000
        r.dynamic_energy_adjustment_damping = 0.001
        audio = r.listen(source)
    try:
        print("Recognizing....")
        text = r.recognize_google(audio,language='en-in')
        print(f"You said: {text}")
    except Exception as e:
        print("Will you say that right Sir?")
        speak("Will you say that right Sir?")
        return "None"
    return text
def face_detect():
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

def body_detect():
    file_loc = "haarcascade_fullbody.xml"
    fil_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+file_loc )
    webcam = cv2.VideoCapture(0)
    while True:
        succ_fra,frame = webcam.read()
        frame_grayscale = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        face_coordinates = fil_cascade.detectMultiScale(frame_grayscale,scaleFactor=1.4,minNeighbors=20)
        for (x,y,w,h) in face_coordinates:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
        cv2.imshow("Window",frame)
        key =cv2.waitKey(1)
        if key == ord("q"):
            break
    webcam.release()

def eye_detect():
    fil_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml" )
    eye_Cascades = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_eye.xml")
    webcam = cv2.VideoCapture(0)
    while True:
        succ_fra,frame = webcam.read()
        frame_grayscale = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        face_coordinates = fil_cascade.detectMultiScale(frame_grayscale,scaleFactor=1.4,minNeighbors=20)
        for (x,y,w,h) in face_coordinates:
            cv2.rectangle(frame,(x,y),(x+w,y+h),0)
            the_face = frame[y:y+h,x:x+w]
            eye_gray = cv2.cvtColor(the_face,cv2.COLOR_BGR2RGB)
            eye_coordinates = eye_Cascades.detectMultiScale(eye_gray)
            for(x_,y_,w_,h_) in eye_coordinates:
                cv2.rectangle(the_face,(x_,y_),(x_+w_,y_+h_),(0,0,0),3)
        cv2.imshow("Window",frame)
        key = cv2.waitKey(1)
        if key == ord("q"):
            break
    webcam.release()
    
def wishme():
    hour = int(datetime.now().hour)
    if(hour>0 and hour<12):
        sp = "Good Morning Sir!"
        print(sp)
        speak(sp)
    elif(hour>=12 and hour<18):
        sp ="Good Afternoon Sir!"
        print(sp)
        speak(sp)
    elif(hour>=18 and hour <24):
        sp = "Good Evening Sir!"
        print(sp)
        speak(sp)

def command2():
    speak("Yes Sir!")
    print("Yes Sir!")
    while True:
            text3 = command().lower()
            if("how are you") in text3:
                    sp = "I'm Good Sir!"
                    print(sp)
                    speak(sp)
            elif("detect face") in text3:
                    speak("detecting Sir!")
                    print("detecting Sir!")
                    face_detect()
            elif("detect body") in text3:
                    speak("detecting Sir!")
                    print("detecting Sir!")
                    body_detect()
            elif("detect my eyes") in text3:
                    speak("detecting Sir!")
                    print("detecting Sir!")
                    eye_detect()
            elif("open google") in text3:
                    webbrowser.open("www.google.com")
            elif("play song") in text3:
                    loc = "D:\SONGS"
                    songs = os.listdir(loc)
                    try:
                        i = random.randint(0,len(songs))
                        os.startfile(os.path.join(loc,songs[i]))
                        if("abort song") in text3:
                            os.kill()
                    except Exception as e:
                        i = random.randint(0,len(songs))
                        os.startfile(os.path.join(loc,songs[i]))
            elif("wikipedia") in text3:
                    wk = text3.replace("wikipedia","")
                    wk = wikipedia.summary(wk,sentences=2)
                    print("According To Wikipedia: ",wk)
                    speak("According to wikipedia: "+wk)
            if ("exit") in text3:
                break

if __name__=="__main__":
    wishme()
    while True:
        text2 = command().lower()
        if "hello" in text2:
            while True:
                command2()
        else:
            speak("you didn't SAY anything")
            print("you didn't say anything")