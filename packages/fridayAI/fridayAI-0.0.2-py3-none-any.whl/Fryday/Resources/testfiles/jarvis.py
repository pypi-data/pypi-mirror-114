from logging import exception
import pyttsx3
import webbrowser
import smtplib
import random
import requests
import sys
import instaloader
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import speech_recognition as sr
import wikipedia
import datetime
import wolframalpha
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pyautogui
import pywikihow
from pywikihow import search_wikihow
import time
import socket
import cv2
import PyPDF2
from twilio.rest import Client, TwilioMonitorClient
import pywhatkit as kit
import contextlib
with contextlib.redirect_stdout(None):
    import pygame
from tkinter import *
import urllib.request
import json


client = wolframalpha.Client('K9T6JG-HWA9LVUUQW')
    
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate',150)

def speak(audio):
    print('JARVIS: ' + audio)
    engine.say(audio)
    engine.runAndWait()

def greetMe():
    currentH = int(datetime.datetime.now().hour)
    if currentH >= 0 and currentH < 12:
        speak('Good Morning!')

    if currentH >= 12 and currentH < 18:
        speak('Good Afternoon!')

    if currentH >= 18 and currentH !=0:
        speak('Good Evening!')

def myCommand():
   
    r = sr.Recognizer()                                                                                   
    with sr.Microphone() as source:                                                                       
        print("Listening...")
        r.pause_threshold =  1
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-in')
        print('User: ' + query + '\n')
        
    except sr.UnknownValueError:
        speak('Sorry sir! mujhe samajh nhi aaya! Please repeat your command')
        query = myCommand()
        
    return query

def startup():
    time.sleep(2)
    time.sleep(1)
    greetMe()
    Greet = ["All servers are connected", "All systems are connected", "Matching retinal scans", "Checking User id"]
    speak(random.choice(Greet))
    speak('jarvis is now online')
    wakeword()

def wakeword():
    test = myCommand().lower()
    if 'jarvis' in test or 'wake up' in test:
        jarvis()
    elif 'stop' in test or 'shutdown' in test:
        os.system("taskkill /f /im GUI.exe")
        sys.exit()

def jarvis():
    start = ['at your service sir', 'always with you sir', 'always here sir', 'waiting for your command sir', 'yes sir', 'hello sir, may I help you with something']
    speak(random.choice(start))

    while True:
        # query = myCommand()
        query = input('Question: ')

      
        if 'open youtube' in query or 'youtube' in query:
            speak('Opening YouTube, sir!')
            speak('Sir, what do you want to search for?')
            search = myCommand()
            speak('ok sir, enjoy')
            kit.playonyt(search)
            
        elif 'send message to papa' in query or 'send text to papa' in query or 'papa ko message' in query:
            speak('sir what should i say')
            msz = myCommand()
            account_sid = 'ACa7e8c3e0c3af97935fa148c772365603'
            auth_token = 'fa252e933a07189e70c7c21f786b36a2'

            client = Client(account_sid, auth_token)
            message = client.messages \
                .create(
                    body= msz,
                    from_= '+19544195388',
                    to= '+919899992756'
                )
            print(message.sid)
            speak('sir message has been sent')

        elif 'send message to mummy' in query or 'send text to mummy' in query or 'mummy ko message' in query:
            speak('sir what should i say')
            msz = myCommand()
            account_sid = 'ACa7e8c3e0c3af97935fa148c772365603'
            auth_token = 'fa252e933a07189e70c7c21f786b36a2'

            client = Client(account_sid, auth_token)
            message = client.messages \
                .create(
                    body= msz,
                    from_= '+19544195388',
                    to= '+919711424205'
                )
            print(message.sid)
            speak('sir message has been sent')

        elif 'call to papa' in query or 'call papa' in query or 'papa ko call' in query:
            speak('sir what should i say')
            msz = myCommand()
            account_sid = 'ACa7e8c3e0c3af97935fa148c772365603'
            auth_token = 'fa252e933a07189e70c7c21f786b36a2'

            client = Client(account_sid, auth_token)
            message = client.calls \
                .create(
                    twiml= '<Response><Say>'+msz+'</Say></Response>',
                    from_= '+19544195388',
                    to= '+919899992756'
                )
            print(message.sid)

        elif 'call to mummy' in query or 'call mummy' in query or 'mummy ko call' in query:
            speak('sir what should i say')
            msz = myCommand()
            account_sid = 'ACa7e8c3e0c3af97935fa148c772365603'
            auth_token = 'fa252e933a07189e70c7c21f786b36a2'

            client = Client(account_sid, auth_token)
            message = client.calls \
                .create(
                    twiml= '<Response><Say>'+msz+'</Say></Response>',
                    from_= '+19544195388',
                    to= '+919711424205'
                )
            print(message.sid)

        elif 'open google' in query:
            speak('Sir, What should I search?')
            cm = myCommand().lower()
            webbrowser.open(f"{cm}")

        elif 'open wikipedia' in query:
            speak('Opening wikipedia, sir!')
            webbrowser.open('www.wikipedia.org')

        elif 'open stackoverflow' in query:
            speak('opening stackoverflow')
            webbrowser.open('www.stackoverflow.com')

        elif 'open facebook' in query:
            speak('opening facebook')
            webbrowser.open('www.facebook.com')

        elif 'open twitter' in query:
            speak('opening twitter')
            webbrowser.open('www.twitter.com')

        elif 'open instagram' in query:
            speak('opening instagram')
            webbrowser.open('www.instagram.com')

        elif 'open gmail' in query:
            speak('Opening gmail, sir')
            webbrowser.open('www.gmail.com')

        elif 'camera' in query:
            speak('starting camera, click the esc or escape key to close it')
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow('Webcam', img)
                k = cv2.waitKey(50)
                if k==27:
                    break
            cap.release()
            cv2.destroyAllWindows()

        elif 'better than siri' in query or 'better than cortana' in query:
            answer = ['I am friends with all AI devices',"I like all AI's"]
            speak(random.choice(answer))

        elif 'when were you made' in query or 'when were you created' in query:
            speak('I was created on the 18th of June 2020')
            
        elif 'i hate you' in query or 'you are bad' in query or 'you are not good' in query:
            speak("I'm sorry that I disappointed you. I'm still learning and trying to be better")

        elif 'i like you' in query or 'you are good' in query or 'you are nice' in query or 'you are not bad' in query:
            reply1 = ['Thanks a lot, sir!','I appreciate that, sir',"That's very nice of you, sir","I can't express my gratitude, sir! Thanks so much!"]
            speak(random.choice(reply1))
            
        elif 'who created you' in query or 'who made you' in query or 'who is your creator' in query or 'who was your creator' in query or 'who is your maker' in query:
            answer1 = ['Sameer created me','I was created by Samer','Sameer made me','I was made by Sameer']
            speak(random.choice(answer1))
            
        elif "what's up" in query or 'what are you doing' in query or 'how do you do' in query:
            answer2 = ['Just doing my thing!', 'just passing the time']
            speak(random.choice(answer2))

        elif 'how are you' in query:
            ans = ['I am fine sir, what about you','Never better! what about you', 'I am nice and full of energy, what about you']
            speak(random.choice(ans))

        elif 'also good' in query or 'am nice' in query or 'am fine' in query:
            speak('nice to hear that sir')

        elif 'not well' in query or 'am sad' in query:
            speak('sorry to hear that')

        elif 'what is your favourite fruit' in query or 'what is your favourite vegetable' in query:
            speak("I'd have a favourite fruit/vegetable when I'll be able to eat like you\n(Maybe in the future, you never know!)")

        elif 'abort' in query or 'stop' in query or 'bye Jarvis ' in query or 'nothing' in query or 'no command' in query or 'no' in query:
            speak('OK, bye sir')
            break

        elif 'hello' in query or 'sup' in query:
            speak('Hello, Sir')

        elif 'send email' in query or 'send an email' in query or 'email' in query or 'send mail' in query:
            speak('Who is the recipient? ')
            recipient = myCommand()

            if 'me' in recipient or 'myself' in recipient or 'I' in recipient or 'sam' in recipient:
                speak('What should I say? ')
                query = myCommand()
                if 'send a file' in query or 'send file' in query or 'send a folder' in query or 'send folder' in query:
                    fromaddr = "mk42jarvisreloadedQ@gmail.com"
                    toaddr = "mk42jarvisreloadedQ@gmail.com"
                    speak('ok sir what is the subject for this email')
                    query = myCommand().lower()
                    subject = query
                    speak('and sir what is the message for this email')
                    query2 = myCommand().lower()
                    message = query2
                    speak('sir please enter the correct path to the file in the shell')
                    file_location = input("Please Enter the Path Here:  ")

                    speak('please wait sir, I am sending your email')

                    msg = MIMEMultipart()
                    msg['From'] = fromaddr
                    msg['To'] = toaddr
                    msg['Subject'] = subject

                    msg.attach(MIMEText(message, 'plain'))

                    #Setting the attachment
                    filename = os.path.basename(file_location)
                    attachment = open(file_location, "rb")
                    p = MIMEBase('application', 'octet-stream')
                    p.set_payload((attachment).read())
                    encoders.encode_base64(p)
                    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

                    #attach the attachment
                    msg.attach(p)

                    s = smtplib.SMTP('smtp.gmail.com', 587)
                    s.starttls()
                    pwd = "justaratherveryintelligentsystem"
                    s.login(fromaddr, pwd)
                    text = msg.as_string()
                    s.sendmail(fromaddr, toaddr, text)
                    s.quit()
                    speak('email has been sent successfully')

                else:
                    content = query

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.ehlo()
                    server.starttls()
                    server.login('mk42jarvisreloadedQ@gmail.com', 'justaratherveryintelligentsystem')
                    server.sendmail('mk42jarvisreloadedQ@gmail.com', 'mk42jarvisreloadedQ@gmail.com', content)
                    server.close()
                    speak('Email has been sent succesfully!')

            elif 'papa' in recipient or 'dadda' in recipient or 'dad' in recipient or 'daddy' in recipient:
                speak('What should I say? ')
                query = myCommand()
                if 'send a file' in query or 'send file' in query or 'send a folder' in query or 'send folder' in query:
                    fromaddr = "mk42jarvisreloadedQ@gmail.com"
                    toaddr = "mkpasi253@gmail.com"
                    speak('ok sir what is the subject for this email')
                    query = myCommand().lower()
                    subject = query
                    speak('and sir what is the message for this email')
                    query2 = myCommand().lower()
                    message = query2
                    speak('sir please enter the correct path to the file in the shell')
                    file_location = input("Please Enter the Path Here:  ")

                    speak('please wait sir, I am sending your email')

                    msg = MIMEMultipart()
                    msg['From'] = fromaddr
                    msg['To'] = toaddr
                    msg['Subject'] = subject

                    msg.attach(MIMEText(message, 'plain'))

                    #Setting the attachment
                    filename = os.path.basename(file_location)
                    attachment = open(file_location, "rb")
                    p = MIMEBase('application', 'octet-stream')
                    p.set_payload((attachment).read())
                    encoders.encode_base64(p)
                    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

                    #attach the attachment
                    msg.attach(p)

                    s = smtplib.SMTP('smtp.gmail.com', 587)
                    s.starttls()
                    pwd = "justaratherveryintelligentsystem"
                    s.login(fromaddr, pwd)
                    text = msg.as_string()
                    s.sendmail(fromaddr, toaddr, text)
                    s.quit()
                    speak('email has been sent successfully')

                else:
                    content = query

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.ehlo()
                    server.starttls()
                    server.login('mk42jarvisreloadedQ@gmail.com', 'justaratherveryintelligentsystem')
                    server.sendmail('mk42jarvisreloadedQ@gmail.com', 'mkpasi253@gmail.com', content)
                    server.close()
                    speak('Email has been sent succesfully!')

            elif 'mumma' in recipient or 'mummy' in recipient or 'mom' in recipient or 'momma' in recipient:
                speak('What should I say? ')
                query = myCommand()
                if 'send a file' in query or 'send file' in query or 'send a folder' in query or 'send folder' in query:
                    fromaddr = "mk42jarvisreloadedQ@gmail.com"
                    toaddr = "savisomya@gmail.com"
                    speak('ok sir what is the subject for this email')
                    query = myCommand().lower()
                    subject = query
                    speak('and sir what is the message for this email')
                    query2 = myCommand().lower()
                    message = query2
                    speak('sir please enter the correct path to the file in the shell')
                    file_location = input("Please Enter the Path Here:  ")

                    speak('please wait sir, I am sending your email')

                    msg = MIMEMultipart()
                    msg['From'] = fromaddr
                    msg['To'] = toaddr
                    msg['Subject'] = subject

                    msg.attach(MIMEText(message, 'plain'))

                    #Setting the attachment
                    filename = os.path.basename(file_location)
                    attachment = open(file_location, "rb")
                    p = MIMEBase('application', 'octet-stream')
                    p.set_payload((attachment).read())
                    encoders.encode_base64(p)
                    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

                    #attach the attachment
                    msg.attach(p)

                    s = smtplib.SMTP('smtp.gmail.com', 587)
                    s.starttls()
                    pwd = "justaratherveryintelligentsystem"
                    s.login(fromaddr, pwd)
                    text = msg.as_string()
                    s.sendmail(fromaddr, toaddr, text)
                    s.quit()
                    speak('email has been sent successfully')

                else:
                    content = query

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.ehlo()
                    server.starttls()
                    server.login('mk42jarvisreloadedQ@gmail.com', 'justaratherveryintelligentsystem')
                    server.sendmail('mk42jarvisreloadedQ@gmail.com', 'savisomya@gmail.com', content)
                    server.close()
                    speak('Email has been sent succesfully!')

            if 'ana' in recipient or 'aana' in recipient or 'sis' in recipient or 'sister' in recipient or "Anna" in recipient:
                speak('What should I say? ')
                query = myCommand()
                if 'send a file' in query or 'send file' in query or 'send a folder' in query or 'send folder' in query:
                    fromaddr = "mk42jarvisreloadedQ@gmail.com"
                    toaddr = "savi19somya@gmail.com"
                    speak('ok sir what is the subject for this email')
                    query = myCommand().lower()
                    subject = query
                    speak('and sir what is the message for this email')
                    query2 = myCommand().lower()
                    message = query2
                    speak('sir please enter the correct path to the file in the shell')
                    file_location = input("Please Enter the Path Here:  ")

                    speak('please wait sir, I am sending your email')

                    msg = MIMEMultipart()
                    msg['From'] = fromaddr
                    msg['To'] = toaddr
                    msg['Subject'] = subject

                    msg.attach(MIMEText(message, 'plain'))

                    #Setting the attachment
                    filename = os.path.basename(file_location)
                    attachment = open(file_location, "rb")
                    p = MIMEBase('application', 'octet-stream')
                    p.set_payload((attachment).read())
                    encoders.encode_base64(p)
                    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

                    #attach the attachment
                    msg.attach(p)

                    s = smtplib.SMTP('smtp.gmail.com', 587)
                    s.starttls()
                    pwd = "justaratherveryintelligentsystem"
                    s.login(fromaddr, pwd)
                    text = msg.as_string()
                    s.sendmail(fromaddr, toaddr, text)
                    s.quit()
                    speak('email has been sent successfully')

                else:
                    content = query

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.ehlo()
                    server.starttls()
                    server.login('mk42jarvisreloadedQ@gmail.com', 'justaratherveryintelligentsystem')
                    server.sendmail('mk42jarvisreloadedQ@gmail.com', 'savi19somya@gmail.com', content)
                    server.close()
                    speak('Email has been sent succesfully!')
           
        else:
            query = query
            try:
                try:
                    res = client.query(query)
                    results = next(res.results).text
                    speak(results)
                    
                except:
                    results = wikipedia.summary(query, sentences=2)
                    speak("Here's something I found on Wikipedia - ")
                    speak(results)
        
            except:
                speak("Sorry, I couldn't find anything related to that. Try searching it on Google.")

                time.sleep(4)

if __name__ == '__main__':
    jarvis()