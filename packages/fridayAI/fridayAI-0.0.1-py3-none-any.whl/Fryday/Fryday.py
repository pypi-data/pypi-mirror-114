
import googletrans
import pyttsx3
import speech_recognition as sr
import webbrowser
import random
import requests
import sys
from keyboard import *
import instaloader
import smtplib
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import wikipedia
import wolframalpha
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pyautogui
from pyautogui import *
from pywikihow import search_wikihow
import time
import datetime
import socket
import cv2
import PyPDF2
from twilio.rest import Client, TwilioMonitorClient
import pywhatkit as kit
from google_trans_new import google_trans_new
from googletrans import Translator
from tkinter import *
import urllib.request
import json
from geopy.distance import great_circle
from geopy.geocoders import Nominatim
import geocoder
from win10toast import ToastNotifier
import subprocess
import win32clipboard

# n=ToastNotifier()
# n.show_toast("Fryday", "Fryday is now online",
#  icon_path ="./Resources/icons/ironman.ico")

client = wolframalpha.Client('K9T6JG-KJVJTEK8X7')


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate',150)
time.sleep(1)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def greetMe():
    currentH = int(datetime.datetime.now().hour)
    if currentH >= 0 and currentH < 12:
        speak('Good Morning sir!')

    if currentH >= 12 and currentH < 16:
        speak('Good Afternoon sir!')
    
    if currentH >= 16 and currentH < 20:
        speak('Good Evening sir!')

    if currentH >= 20 and currentH !=0:
        speak('Good Night sir!')

def myCommand():
   
    r = sr.Recognizer()                                                                                   
    with sr.Microphone() as source:                                                                       
        print("Listening...")
        r.pause_threshold =  1
        audio = r.listen(source)
    try:
        print('Reconizing...')
        query = r.recognize_google(audio, language='en-in')
        print('User: ' + query + '\n')
        
    except sr.UnknownValueError:
        query = myCommand()
        
    return query

def joinMeet():
    webbrowser.open('https://web.whatsapp.com')
    while True:
        group = pyautogui.locateOnScreen('./Resources/zoom/engwhat.png')
        if group != None:
            pyautogui.click(group)
            print('group opened')
            break
        else:
            print('group not found')
            time.sleep(2)
    
    while True:
        link = pyautogui.locateOnScreen('./Resources/zoom/meet.png')
        if link != None:
            pyautogui.click(link)
            print('link opened')
            break
        else:
            print('group not found')

def joinZoom(id, password):
    subprocess.call("C:\\Users\\Sam\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe")
    while True:
        join1 = pyautogui.locateOnScreen('./Resources/zoom/join1.png')
        if join1 != None:
            pyautogui.click(join1)
            print("joinbtn clicked")
            break
        else:
            print("Couldn't find the btn")
            time.sleep(2)
    
    while True:
        field1 = pyautogui.locateOnScreen('./Resources/zoom/field.png')
        if field1 != None:
            pyautogui.click(field1)
            print("filed clicked")
            pyautogui.typewrite(id)
            pyautogui.click(pyautogui.locateOnScreen('./Resources/zoom/join2.png'))
            break
        else:
            print("Couldn't find the field")
            time.sleep(2)

    while True:
        field2 = pyautogui.locateOnScreen('./Resources/zoom/field2.png')
        if field2 != None:
            pyautogui.click(field2)
            print("filed clicked")
            pyautogui.typewrite(password)
            pyautogui.click(pyautogui.locateOnScreen('./Resources/zoom/join3.png'))
            break
        else:
            print("Couldn't find the field")
            time.sleep(2)

def pdf_reader():
    speak("sir please enter the full path to file in the shell")
    file = input("Enter the path here: ")
    book = open(file, 'rb')
    pdfReader = PyPDF2.PdfFileReader(book)
    pages = pdfReader.numPages
    speak(f"Total number of pages in this pdf {pages}")
    speak("sir please enter the page number I have to read")
    pg = myCommand()
    pg = int(pg)
    page = pdfReader.getPage(pg)
    text = page.extractText()
    speak(text)

def ChromeAuto(command):
    while True:
        query = str(command)
        if 'new tab' in query:
            press_and_release('ctrl + t')
            speak('tab opened')
        elif 'close tab' in query:
            press_and_release('ctrl + w')
            speak('tab closed')
        elif 'new window' in query:
            press_and_release('ctrl + n')
            speak('new window opened')
        elif 'history' in query:
            press_and_release('ctrl + h')
            speak('history opened')
        elif 'downloads' in query or 'download' in query:
            press_and_release('ctrl + j')
            speak('downloads opened')
        elif 'bookmark' in query:
            press_and_release('ctrl + d')
            press('enter')
            speak('tab added to bookmarks')
        elif 'incognito' in query:
            press_and_release('Ctrl + Shift + n')
            speak('incognito window opened')
        elif 'switch tab' in query:
            tab = query.replace("switch tab","")
            Tab = tab.replace("to","")
            num = Tab

            bb = f'ctrl + {num}'
            press_and_release(bb)

def YoutubeAuto(command):
    while True:
        query = str(command)
        if 'pause' in query:
            pyautogui.press('k')
        elif 'mute' in query:
            pyautogui.press('m')
        elif 'widen' in query or 'theatre' in query:
            pyautogui.press('t')
        elif 'full' in query:
            pyautogui.press('f')
        elif 'restart' in query:
            pyautogui.press('0')
        elif 'skip' in query:
            pyautogui.press('l')

def Notepad():
    speak('I am creating a new notepad file.')
    speak('What will be the name ofthis file?')
    filename=myCommand() + '-note'
    speak('And sir, what should I write in this file?')
    writes=myCommand()
    os.chdir('./Database/Documents')
    with open(filename,"w") as file:
        file.write(writes)
    path_2=str(filename)
    os.startfile(path_2)

def DownloadYoutube():
    from pytube import YouTube
    from pyperclip import paste

    sleep(2)
    # click(x=1497, y=47)
    hotkey("ctrl","l")
    hotkey('ctrl','c')
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    data = str(data)
    # value=paste
    Link=data

    def Download(link):
        url = YouTube(link)
        video=url.streams.first()
        video.download('./Database/Youtube/')
        n=ToastNotifier()
        n.show_toast("Fryday", "Successfully downloaded youtube video",
        icon_path ="./Resources/icons/ironman.ico")
        speak('Done sir, The youtube video has been saved in our Youtube folder')
    Download(Link)

def GoogleMap(Place):
    Url_Place = 'https://www.google.com/maps/place/'+str(Place)
    geolocator=Nominatim(user_agent="myGeocoder")
    location=geolocator.geocode(Place,addressdetails=True)
    target_latlon=location.latitude, location.longitude
    location=location.raw['address']
    target={'city' : location.get('city',''),
                'state' : location.get('state',''),
                'country' : location.get('country','')}
    current_loca=geocoder.ip('me')
    current_latlon=current_loca.latlng
    distance=str(great_circle(current_latlon,target_latlon))
    distance = str(distance.split(' ',1)[0])
    distance=round(float(distance),2)
    speak(f'Sir , {Place} is {distance} kilometers away from us')
    speak('Let me show you on the map')
    time.sleep(1)
    webbrowser.open(Url_Place)

def tran(line):
    translate =Translator()
    result = translate.translate(line, dest='en')
    speak('The result after translation is '+result.text)

def Wakeword():
    n=ToastNotifier()
    n.show_toast("Fryday", "Fryday is now online",
     icon_path ="./Resources/icons/ironman.ico")
    permit=myCommand().lower()
    if 'friday' in permit or 'fryday' in permit or 'Fryday' in permit or 'Friday' in permit:
        Fryday()

def Sleepword():
    permit=myCommand().lower()
    if 'friday' in permit or 'fryday' in permit or 'Fryday' in permit or 'Friday' in permit:
        Fryday1()

def Fryday():
    greetMe()
    Greet = ["All servers are connected", "All systems are connected", "Checking User id", 'All drivers are checked', 'charging arc reactors']
    speak(random.choice(Greet))
    speak('Friday is now online')
    while True:
        a=0
        b=0
        c=float("-inf")
        # query = myCommand().lower()
        query = input('Enter question: ')

        if 'open youtube' in query:
            speak('Opening YouTube, sir!')
            speak('Sir, what do you want to search for?')
            search = myCommand()
            speak('ok sir, enjoy')
            kit.playonyt(search)

        elif 'play' in query:
            song = query.replace("play","")
            song = song.replace("on youtube","")
            song = song.replace("Friday","")
            song = song.replace("Fryday","")
            song = song.replace("friday","")
            song = song.replace("fryday","")
            play = song
            speak('ok sir')
            kit.playonyt(play)

        elif 'open google' in query:
            speak('Sir, What should I search?')
            cm = myCommand().lower()
            webbrowser.open(f"{cm}")

        elif 'open wikipedia' in query:
            speak('Opening Wikipedia Sir')
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

        elif 'open asset store' in query:
            speak('Opening Unity Asset Store Sir')
            webbrowser.open('assetstore.unity3d.com')

        elif 'open instagram' in query:
            speak('opening instagram')
            webbrowser.open('www.instagram.com')

        elif 'open code' in query or 'open visual code' in query or 'open visual studio code' in query:
            speak('Opening visual studio code editor')
            os.startfile('C://Users//Sam//AppData//Local//Programs//Microsoft VS Code//Code.exe')

        elif 'close code' in query or 'close visual code' in query or 'close visual studion code' in query:
            speak('closing visual studio code editor')
            os.system("taskkill /f /im code.exe")

        elif 'open notepad' in query:
            Notepad()

        elif 'close notepad' in query:
            os.system("taskkill /f /im notepad.exe")
        
        elif 'open cmd' in query or 'open command prompt' in query or 'open shell' in query:
            speak('Opening command prompt')
            os.system('start cmd')

        elif 'switch the window' in query or 'switch window' in query:
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            time.sleep(1)
            pyautogui.keyUp("alt")

        elif "screenshot" in query:
            speak("sir what will be the name of this screenshot")
            name = myCommand().lower()
            speak("hold the screen sir, I am taking the screenshot now")
            time.sleep(2)
            img = pyautogui.screenshot()
            img.save(f"./Database/screenshots/{name}.png")
            speak("done sir, screenshot has been saved in our main folder") 

        elif 'shut down' in query or 'shutdown' in query:
            os.system("shutdown /s /t 5")

        elif 'restart the pc' in query or 'restart the system' in query or 'restart the computer' in query:
            os.system("shutdown /r /t 5")

        elif 'sleep the pc' in query or 'sleep the system' in query or 'sleep the computer' in query:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

        elif 'online class' in query:
            speak('checking the shedule of online classes sir')
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M")
            print("Current Time =", current_time)

            nowday = datetime.datetime.now()
            print(nowday.strftime("%A"))

            if current_time >= '8:00' or current_time < '8:40':
                if nowday=='Monday':
                    speak('Chemistry class is on the way sir')
                    joinZoom('432 806 5164', 'Pe7QDv')
                elif nowday=='Tuesday':
                    speak('Chemistry class is on the way sir')
                    joinZoom('432 806 5164', 'Pe7QDv')
                elif nowday=='Wednesday':
                    speak('Chemistry class is on the way sir')
                    joinZoom('432 806 5164', 'Pe7QDv')
                else:
                    speak('There is no online class available at this time')

            if current_time >= '9:00' or current_time < '9:40':
                if nowday=='Monday':
                    speak('Maths class is on the way sir')
                    joinZoom('780 754 1122', '1234')
                elif nowday=='Tuesday':
                    speak('Maths class is on the way sir')
                    joinZoom('780 754 1122', '1234')
                elif nowday=='Wednesday':
                    speak('Maths class is on the way sir')
                    joinZoom('780 754 1122', '1234')
                elif nowday=='Thursday':
                    speak('Chemistry class on the way sir')
                    joinZoom('432 806 5164', 'Pe7QDv')
                elif nowday=='Friday':
                    speak('Chemistry class on the way sir')
                    joinZoom('432 806 5164', 'Pe7QDv')
                elif nowday=='Saturday':
                    speak('Chemistry class on the way sir')
                    joinZoom('432 806 5164', 'Pe7QDv')
                else:
                    speak('Today is Sunday sir! Take a rest')
            
            elif current_time >= '10:00' or current_time < '10:40':
                if nowday=='Monday':
                    speak('IP class is on the way sir')
                    joinZoom('780 754 1122', '1234')
                elif nowday=='Tuesday':
                    speak('IP class is on the way sir')
                    joinZoom('780 754 1122', '1234')
                elif nowday=='Wednesday':
                    speak('IP class is on the way sir')
                    joinZoom('780 754 1122', '1234')
                elif nowday=='Thursday':
                    speak('Maths class on the way sir')
                    joinZoom('432 806 5164', 'Pe7QDv')
                elif nowday=='Friday':
                    speak('Maths class on the way sir')
                    joinZoom('432 806 5164', 'Pe7QDv')
                elif nowday=='Saturday':
                    speak('Maths class on the way sir')
                    joinZoom('432 806 5164', 'Pe7QDv')
                else:
                    speak('Today is Sunday sir! Take a rest')
            
            elif current_time >= '11:00' or current_time < '11:40':
                if nowday=='Monday' or nowday=='Tuesday' or nowday=='Wednesday' or nowday=='Thursday' or nowday=='Friday' or nowday=='Saturday':
                    speak('English class on the way sir')
                    joinMeet()
                else:
                    speak('Today is Sunday sir! Take a rest')
            
            elif current_time >= '12:00' or current_time < '12:40':
                speak('Physics Class on the way')
                joinZoom('769 723 3861', '652975')
            
            else:
                speak('There is no online classes available at this time')
                joinZoom('432 806 5164', 'Pe7QDv')

        elif 'download video' in query or 'download youtube video' in query or 'save this video' in query:
            DownloadYoutube()

        elif 'internet speed' in query or 'network speed' in query:
            speak('Starting our speed test servers, you will get the result in few seconds')
            import speedtest as st
            speed_test = st.Speedtest()
            speed_test.get_best_server()
            ping = speed_test.results.ping
            download = speed_test.download()
            upload = speed_test.upload()
            download_mbs = round(download / (10**6), 2)
            upload_mbs = round(upload / (10**6), 2)
            speak('Your Download Speed is');speak(download_mbs);speak('mega bits per second')
            speak('And Your upload Speed is');speak(upload_mbs);speak('mega bits per second')
        
        elif 'battery' in query or 'power' in query:
            import psutil
            battery = psutil.sensors_battery()
            percentage = battery.percent
            speak('sir our system has {percentage} percent battery')

            if percentage>=75:
                speak('we have enough power to continue our work')
            elif percentage>=40 and percentage<=75:
                speak('our power is enough but you may connect our system to a charging point')
            elif percentage>=15 and percentage<=30:
                speak("we don't have enough power to work, please connect our system to a charging point")
            elif percentage<=15:
                speak("we have very low power, please consider to charge the system otherwise system will shut down soon")
        
        elif 'volume up' in query:
            pyautogui.press("volumeup")

        elif 'volume down' in query:
            pyautogui.press("volumedown")

        elif 'mute' in query:
            pyautogui.press("volumemute")
        
        elif 'hide my files' in query or 'hide all files' in query or 'hide files' in query:
            os.system("attrib +h /s /d")
            speak('done sir, all the file in this folder are now hidden')

        elif "visible the files" in query or 'show all files' in query or 'show files' in query:
            os.system("attrib -h /s /d")
            speak('done sir, all the files in this are now visible to everyone, I hope you are taking this decision at your own')
        
        elif "ip address" in query:
            hostname = socket.gethostname() 
            IPAddr = socket.gethostbyname(hostname)
            speak('Your Computer IP address is: ' + IPAddr)
            print('Your Computer IP address is: ' + IPAddr)

        elif "where are we" in query or "where am I" in query or "location" in query or "where i am" in query or "where we are" in query:
            try:
                with urllib.request.urlopen("http://ip-api.com/json/?fields=61439") as url:
                    data = json.loads(url.read().decode())
                    country = data['country']
                    city = data['city']
                    speak('According to me we are in '+city+', '+country)
                    
            except:
                speak('Sorry sir, some of our monitoring systems are not working properly causing me unable to find our location')
                pass

        elif 'read PDF' in query:
            speak('ok sir')
            pdf_reader()

        elif 'insta profile' in query or 'profile on insta' in query or 'instagram profile' in query or 'profile on instagram' in query:
            speak('sir please enter the username of the profile')
            name = input('Enter the username here: ')
            webbrowser.open(f"www.instagram.com/{name}")
            speak(f"Sir here is the profile of the user {name}")
            time.sleep(3)
            speak('sir would you like to download the profile pic of this user')
            condition = myCommand().lower()
            if "yes" in condition or "ya" in condition or "sure" in condition or "yup" in condition or 'yeah' in condition:
                mod = instaloader.Instaloader()
                os.chdir('./Database/Instagram')
                filename=mod.download_profile(name, profile_pic_only=True)
                n=ToastNotifier()
                n.show_toast("Fryday", "Downloaded Intagram profile pic",
                icon_path ="./Resources/icons/ironman.ico")
                speak('Done Sir, profile pic has been saved in our Instagram folder')
                
            else:
                pass
        
        elif 'news' in query or 'headlines' in query or "what's the update" in query:
            speak('Getting news from server')
            speak("server found....... staring narration")
            url = 'http://newsapi.org/v2/top-headlines?sources=the-times-of-india&apiKey=dd3dad0f0aa342a2b141913cb6993b39'
            url = 'http://newsapi.org/v2/top-headlines?sources=the-times-of-india&apiKey=dd3dad0f0aa342a2b141913cb6993b39'
            news = requests.get(url).text
            news_dict = json.loads(news)
            arts = news_dict['articles']
            speak('Source: The Times Of India')
            speak('Todays Headlines are..')
            for index, articles in enumerate(arts):
                speak(articles['title'])
                if index == len(arts)-1:
                    break
                speak('Next headline..')
            speak('These were the top headlines, Have a nice day Sir!!..')
            speak('sir do you want to read the full news')
            condition = myCommand().lower()
            if 'yes' in condition or 'ya' in condition:
                speak('opening news from browser')
                webbrowser.open('http://newsapi.org/v2/top-headlines?sources=the-times-of-india&apiKey=dd3dad0f0aa342a2b141913cb6993b39')
            else:
                speak('ok no problem sir!')

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
                    server.login('mk42jarvisreloaded@gmail.com', 'justaratherveryintelligentsystem')
                    server.sendmail('mk42jarvisreloaded@gmail.com', 'mkpasi253@gmail.com', content)
                    server.close()
                    speak('Email has been sent succesfully!')

            elif 'mumma' in recipient or 'mummy' in recipient or 'mom' in recipient or 'momma' in recipient:
                speak('What should I say? ')
                query = myCommand()
                if 'send a file' in query or 'send file' in query or 'send a folder' in query or 'send folder' in query:
                    fromaddr = "mk42jarvisreloaded@gmail.com"
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
                    server.login('mk42jarvisreloaded@gmail.com', 'justaratherveryintelligentsystem')
                    server.sendmail('mk42jarvisreloaded@gmail.com', 'savisomya@gmail.com', content)
                    server.close()
                    speak('Email has been sent succesfully!')

            elif 'ana' in recipient or 'aana' in recipient or 'sis' in recipient or 'sister' in recipient or "Anna" in recipient:
                speak('What should I say? ')
                query = myCommand()
                if 'send a file' in query or 'send file' in query or 'send a folder' in query or 'send folder' in query:
                    fromaddr = "mk42jarvisreloaded@gmail.com"
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
                    server.login('mk42jarvisreloaded@gmail.com', 'justaratherveryintelligentsystem')
                    server.sendmail('mk42jarvisreloaded@gmail.com', 'savi19somya@gmail.com', content)
                    server.close()
                    speak('Email has been sent succesfully!')
        
        elif 'tweet' in query:
            
            speak('sir what should I tweet?')
            tweet = myCommand()
            email = 'Jarvis31496332'
            password = 'jarvis@123'
            options = Options()
            options.add_argument("start-maximized")
            driver = webdriver.Chrome(options=options)
            driver.get("https://twitter.com/login")
            email_xpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[1]/label/div/div[2]/div/input'
            password_xpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[2]/label/div/div[2]/div/input'
            login_xpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[3]/div/div'
            time.sleep(1)
            driver.find_element_by_xpath(email_xpath).send_keys(email)
            time.sleep(0.5)
            driver.find_element_by_xpath(password_xpath).send_keys(password)
            time.sleep(0.5)
            driver.find_element_by_xpath(login_xpath).click()

            tweet_xpath = '//*[@id="react-root"]/div/div/div[2]/header/div/div/div/div[1]/div[3]/a/div'
            message_xpath = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[3]/div/div/div/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div'
            post_xpath = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[3]/div/div/div/div[1]/div/div/div/div/div[2]/div[3]/div/div/div[2]/div[4]/div'
            time.sleep(1)

            driver.find_element_by_xpath(tweet_xpath).click()
            time.sleep(0.5)
            driver.find_element_by_xpath(message_xpath).send_keys(tweet)
            time.sleep(0.5)
            driver.find_element_by_xpath(post_xpath).click()
        
        elif 'how to' in query:
            speak('how-to-do mode activated, searching your query')
            how = query
            max_results = 1
            how_to = search_wikihow(how, max_results)
            assert len(how_to) == 1
            how_to[0].print()
            speak(how_to[0].summary)
        
        elif 'send whatsapp message' in query or 'whatsapp message' in query:
            speak('Sir who is the recipient?') 
            recipient = myCommand()
            if 'papa' in query or 'dad' in query:
                speak('and sir what is the message for your dad?')
                mes = myCommand()
                webbrowser.open('https://web.whatsapp.com/send?phone=+919899992756&text='+mes)
                time.sleep(10)
                pyautogui.press('enter')

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
            speak("I'd have a favourite fruit or vegetable when I'll be able to eat like you\n(Maybe in the future, you never know!)")

        elif 'abort' in query or 'stop' in query or 'bye' in query or 'nothing' in query or 'no command' in query:
            speak('Ok, bye sir')

            if a+b > 0:
                speak("Just wanted to say one more thing, By analyzing your replies I've found that you had a nice experience with me.")
                speak('Goodbye!')
                
            if a+b < -1:
                speak("Just wanted to say one more thing, By analyzing your replies I've found that you had a bad impression on me. I will be better next time")
                speak('Goodbye!')
                
            if a+b ==0:
                speak('We will meet again')
                
            break

        elif 'take a break' in query or 'you may sleep' in query:
            speak('Ok sir you can call me anytime')
            n=ToastNotifier()
            n.show_toast("Fryday", "I am sleeping",
            icon_path ="./Resources/icons/ironman.ico")
            Sleepword()

        elif 'hello' in query or 'sup' in query or 'hi friday' in query or 'hi Friday' in query:
            speak('Hello, Sir')
        
        elif 'i hate you' in query or 'you are bad' in query or 'you are not good' in query:
             speak("I am sorry if I disappointed you, my work is still in progress. Maybe one day I will be perfect.")
             b = b-5

        elif 'i like you' in query or 'you are good' in query or 'you are nice' in query or 'you are not bad' in query:
            reply1 = ['Thanks, sam!','Nice to hear, sam',"Thanks, Sir","I was made to hear that", 'thanks, sam']
            speak(random.choice(reply1))
            a = a+5

        elif 'your name' in query:
            ans = ['you can call me friday','I am Friday','Friday']
            speak(random.choice(ans))
        
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
        
        elif 'chrome' in query:
            ChromeAuto(query)

        elif 'youtube' in query:
            YoutubeAuto(query)

        elif 'where is' in query:
            Place = query.replace("where is","")
            Place = Place.replace("friday","")
            Place = Place.replace("fryday","")
            Place = Place.replace("Fryday","")
            Place = Place.replace("Friday","")
            place = Place
            GoogleMap(place)

        elif 'translate' in query:
            line = query.replace("translate","")
            line = line.replace("Friday","")
            line = line.replace("Fryday","")
            line = line.replace("friday","")
            line = line.replace("fryday","")
            tran(line)

        else:
            query = query
            client = wolframalpha.Client('K9T6JG-KJVJTEK8X7')
            try:
                try:
                    res = client.query(query)
                    results = next(res.results).text
                    speak(results)
                        
                except:
                    results = wikipedia.summary(query, sentences=5)
                    speak("I have Found that - ")
                    print(results)
                    speak(results)
            
            except:
                speak("Sorry some servers are not responding, please try again later ")

def Fryday1():
    waking=['Always here sir','Always with you sir','at your service sir','waiting for your command sir']
    speak(random.choice(waking))
    while True:
        a=0
        b=0
        c=float("-inf")
        query = myCommand().lower()
        # query = input('Enter question: ')

        if 'open youtube' in query:
            speak('Opening YouTube, sir!')
            speak('Sir, what do you want to search for?')
            search = myCommand()
            speak('ok sir, enjoy')
            kit.playonyt(search)

        elif 'play' in query:
            song = query.replace("play","")
            song = song.replace("on youtube","")
            song = song.replace("Friday","")
            song = song.replace("Fryday","")
            song = song.replace("friday","")
            song = song.replace("fryday","")
            play = song
            speak('ok sir')
            kit.playonyt(play)

        elif 'open google' in query:
            speak('Sir, What should I search?')
            cm = myCommand().lower()
            webbrowser.open(f"{cm}")

        elif 'open wikipedia' in query:
            speak('Opening Wikipedia Sir')
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

        elif 'open asset store' in query:
            speak('Opening Unity Asset Store Sir')
            webbrowser.open('assetstore.unity3d.com')

        elif 'open instagram' in query:
            speak('opening instagram')
            webbrowser.open('www.instagram.com')

        elif 'open code' in query or 'open visual code' in query or 'open visual studio code' in query:
            speak('Opening visual studio code editor')
            os.startfile('C://Users//Sam//AppData//Local//Programs//Microsoft VS Code//Code.exe')

        elif 'close code' in query or 'close visual code' in query or 'close visual studion code' in query:
            speak('closing visual studio code editor')
            os.system("taskkill /f /im code.exe")

        elif 'open notepad' in query:
            Notepad()

        elif 'close notepad' in query:
            os.system("taskkill /f /im notepad.exe")
        
        elif 'open cmd' in query or 'open command prompt' in query or 'open shell' in query:
            speak('Opening command prompt')
            os.system('start cmd')

        elif 'switch the window' in query or 'switch window' in query:
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            time.sleep(1)
            pyautogui.keyUp("alt")

        elif "screenshot" in query:
            speak("sir what will be the name of this screenshot")
            name = myCommand().lower()
            speak("hold the screen sir, I am taking the screenshot now")
            time.sleep(2)
            img = pyautogui.screenshot()
            img.save(f"./Database/screenshots/{name}.png")
            speak("done sir, screenshot has been saved in our main folder") 

        elif 'shut down' in query or 'shutdown' in query:
            os.system("shutdown /s /t 5")

        elif 'restart the pc' in query or 'restart the system' in query or 'restart the computer' in query:
            os.system("shutdown /r /t 5")

        elif 'sleep the pc' in query or 'sleep the system' in query or 'sleep the computer' in query:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

        elif 'online class' in query:
            speak('checking the shedule of online classes sir')
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M")
            print("Current Time =", current_time)

            nowday = datetime.datetime.now()
            print(nowday.strftime("%A"))

            if current_time >= '8:00' or current_time < '8:40':
                if nowday=='Monday':
                    speak('Chemistry class is on the way sir')
                    joinZoom('432 806 5164', 'Pe7QDv')
                elif nowday=='Tuesday':
                    speak('Chemistry class is on the way sir')
                    joinZoom('432 806 5164', 'Pe7QDv')
                elif nowday=='Wednesday':
                    speak('Chemistry class is on the way sir')
                    joinZoom('432 806 5164', 'Pe7QDv')
                else:
                    speak('there is no online class at this time')

            elif current_time >= '9:00' or current_time < '9:40':
                if nowday=='Monday':
                    speak('Maths class is on the way sir')
                    joinZoom('780 754 1122', '1234')
                elif nowday=='Tuesday':
                    speak('Maths class is on the way sir')
                    joinZoom('780 754 1122', '1234')
                elif nowday=='Wednesday':
                    speak('Maths class is on the way sir')
                    joinZoom('780 754 1122', '1234')
                elif nowday=='Thursday':
                    speak('Chemistry class on the way sir')
                    joinZoom('432 806 5164', 'Pe7QDv')
                elif nowday=='Friday':
                    speak('Chemistry class on the way sir')
                    joinZoom('432 806 5164', 'Pe7QDv')
                elif nowday=='Saturday':
                    speak('Chemistry class on the way sir')
                    joinZoom('432 806 5164', 'Pe7QDv')
                else:
                    speak('Today is Sunday sir! Take a rest')
            
            elif current_time >= '10:00' or current_time < '10:40':
                if nowday=='Monday':
                    speak('IP class is on the way sir')
                    joinZoom('780 754 1122', '1234')
                elif nowday=='Tuesday':
                    speak('IP class is on the way sir')
                    joinZoom('780 754 1122', '1234')
                elif nowday=='Wednesday':
                    speak('IP class is on the way sir')
                    joinZoom('780 754 1122', '1234')
                elif nowday=='Thursday':
                    speak('Maths class on the way sir')
                    joinZoom('432 806 5164', 'Pe7QDv')
                elif nowday=='Friday':
                    speak('Maths class on the way sir')
                    joinZoom('432 806 5164', 'Pe7QDv')
                elif nowday=='Saturday':
                    speak('Maths class on the way sir')
                    joinZoom('432 806 5164', 'Pe7QDv')
                else:
                    speak('Today is Sunday sir! Take a rest')
            
            elif current_time >= '11:00' or current_time < '11:40':
                if nowday=='Monday' or nowday=='Tuesday' or nowday=='Wednesday' or nowday=='Thursday' or nowday=='Friday' or nowday=='Saturday':
                    speak('English class on the way sir')
                    joinMeet()
                else:
                    speak('Today is Sunday sir! Take a rest')
            
            elif current_time >= '12:00' or current_time < '12:40':
                speak('Physics Class on the way')
                joinZoom('769 723 3861', '652975')
            
            else:
                speak('There is no online classes available at this time')

        elif 'download video' in query or 'download youtube video' in query or 'save this video' in query:
            DownloadYoutube()

        elif 'internet speed' in query or 'network speed' in query:
            speak('Starting our speed test servers, you will get the result in few seconds')
            import speedtest as st
            speed_test = st.Speedtest()
            speed_test.get_best_server()
            ping = speed_test.results.ping
            download = speed_test.download()
            upload = speed_test.upload()
            download_mbs = round(download / (10**6), 2)
            upload_mbs = round(upload / (10**6), 2)
            speak('Your Download Speed is');speak(download_mbs);speak('mega bits per second')
            speak('And Your upload Speed is');speak(upload_mbs);speak('mega bits per second')
        
        elif 'battery' in query or 'power' in query:
            import psutil
            battery = psutil.sensors_battery()
            percentage = battery.percent
            speak('sir our system has {percentage} percent battery')

            if percentage>=75:
                speak('we have enough power to continue our work')
            elif percentage>=40 and percentage<=75:
                speak('our power is enough but you may connect our system to a charging point')
            elif percentage>=15 and percentage<=30:
                speak("we don't have enough power to work, please connect our system to a charging point")
            elif percentage<=15:
                speak("we have very low power, please consider to charge the system otherwise system will shut down soon")
        
        elif 'volume up' in query:
            pyautogui.press("volumeup")

        elif 'volume down' in query:
            pyautogui.press("volumedown")

        elif 'mute' in query:
            pyautogui.press("volumemute")
        
        elif 'hide my files' in query or 'hide all files' in query or 'hide files' in query:
            os.system("attrib +h /s /d")
            speak('done sir, all the file in this folder are now hidden')

        elif "visible the files" in query or 'show all files' in query or 'show files' in query:
            os.system("attrib -h /s /d")
            speak('done sir, all the files in this are now visible to everyone, I hope you are taking this decision at your own')
        
        elif "ip address" in query:
            hostname = socket.gethostname() 
            IPAddr = socket.gethostbyname(hostname)
            speak('Your Computer IP address is: ' + IPAddr)
            print('Your Computer IP address is: ' + IPAddr)

        elif "where are we" in query or "where am I" in query or "location" in query or "where i am" in query or "where we are" in query:
            try:
                with urllib.request.urlopen("http://ip-api.com/json/?fields=61439") as url:
                    data = json.loads(url.read().decode())
                    country = data['country']
                    city = data['city']
                    print('According to me we are in '+city+', '+country+'')
                    
            except:
                speak('Sorry sir, some of our monitoring systems are not working properly causing me unable to find our location')
                pass

        elif 'read PDF' in query:
            speak('ok sir')
            pdf_reader()

        elif 'insta profile' in query or 'profile on insta' in query or 'instagram profile' in query or 'profile on instagram' in query:
            speak('sir please enter the username of the profile')
            name = input('Enter the username here: ')
            webbrowser.open(f"www.instagram.com/{name}")
            speak(f"Sir here is the profile of the user {name}")
            time.sleep(3)
            speak('sir would you like to download the profile pic of this user')
            condition = myCommand().lower()
            if "yes" in condition or "ya" in condition or "sure" in condition or "yup" in condition or 'yeah' in condition:
                mod = instaloader.Instaloader()
                os.chdir('./Database/Instagram')
                filename=mod.download_profile(name, profile_pic_only=True)
                n=ToastNotifier()
                n.show_toast("Fryday", "Successfully downloaded profile pic",
                icon_path ="./Resources/icons/ironman.ico")
                speak('Done Sir, profile pic has been saved in our Instagram folder')
                
            else:
                pass
        
        elif 'news' in query or 'headlines' in query or "what's the update" in query:
            speak('Getting news from server')
            speak("server found....... staring narration")
            url = 'http://newsapi.org/v2/top-headlines?sources=the-times-of-india&apiKey=dd3dad0f0aa342a2b141913cb6993b39'
            url = 'http://newsapi.org/v2/top-headlines?sources=the-times-of-india&apiKey=dd3dad0f0aa342a2b141913cb6993b39'
            news = requests.get(url).text
            news_dict = json.loads(news)
            arts = news_dict['articles']
            speak('Source: The Times Of India')
            speak('Todays Headlines are..')
            for index, articles in enumerate(arts):
                speak(articles['title'])
                if index == len(arts)-1:
                    break
                speak('Next headline..')
            speak('These were the top headlines, Have a nice day Sir!!..')
            speak('sir do you want to read the full news')
            condition = myCommand().lower()
            if 'yes' in condition or 'ya' in condition:
                speak('opening news from browser')
                webbrowser.open('http://newsapi.org/v2/top-headlines?sources=the-times-of-india&apiKey=dd3dad0f0aa342a2b141913cb6993b39')
            else:
                speak('ok no problem sir!')

        elif 'send email' in query or 'send an email' in query or 'email' in query or 'send mail' in query:
            speak('Who is the recipient? ')
            recipient = myCommand()

            if 'me' in recipient or 'myself' in recipient or 'I' in recipient or 'sam' in recipient:
                speak('What should I say? ')
                query = myCommand()
                if 'send a file' in query or 'send file' in query or 'send a folder' in query or 'send folder' in query:
                    fromaddr = "mk42jarvisreloaded@gmail.com"
                    toaddr = "mk42jarvisreloaded@gmail.com"
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
                    server.login('mk42jarvisreloaded@gmail.com', 'justaratherveryintelligentsystem')
                    server.sendmail('mk42jarvisreloaded@gmail.com', 'mk42jarvisreloaded@gmail.com', content)
                    server.close()
                    speak('Email has been sent succesfully!')

            elif 'papa' in recipient or 'dadda' in recipient or 'dad' in recipient or 'daddy' in recipient:
                speak('What should I say? ')
                query = myCommand()
                if 'send a file' in query or 'send file' in query or 'send a folder' in query or 'send folder' in query:
                    fromaddr = "mk42jarvisreloaded@gmail.com"
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
                    server.login('mk42jarvisreloaded@gmail.com', 'justaratherveryintelligentsystem')
                    server.sendmail('mk42jarvisreloaded@gmail.com', 'mkpasi253@gmail.com', content)
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

            elif 'ana' in recipient or 'aana' in recipient or 'sis' in recipient or 'sister' in recipient or "Anna" in recipient:
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
        
        elif 'tweet' in query:
            
            speak('sir what should I tweet?')
            tweet = myCommand()
            email = 'Jarvis31496332'
            password = 'jarvis@123'
            options = Options()
            options.add_argument("start-maximized")
            driver = webdriver.Chrome(options=options)
            driver.get("https://twitter.com/login")
            email_xpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[1]/label/div/div[2]/div/input'
            password_xpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[2]/label/div/div[2]/div/input'
            login_xpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[3]/div/div'
            time.sleep(1)
            driver.find_element_by_xpath(email_xpath).send_keys(email)
            time.sleep(0.5)
            driver.find_element_by_xpath(password_xpath).send_keys(password)
            time.sleep(0.5)
            driver.find_element_by_xpath(login_xpath).click()

            tweet_xpath = '//*[@id="react-root"]/div/div/div[2]/header/div/div/div/div[1]/div[3]/a/div'
            message_xpath = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[3]/div/div/div/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div'
            post_xpath = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[3]/div/div/div/div[1]/div/div/div/div/div[2]/div[3]/div/div/div[2]/div[4]/div'
            time.sleep(1)

            driver.find_element_by_xpath(tweet_xpath).click()
            time.sleep(0.5)
            driver.find_element_by_xpath(message_xpath).send_keys(tweet)
            time.sleep(0.5)
            driver.find_element_by_xpath(post_xpath).click()
        
        elif 'how to' in query:
            speak('how-to-do mode activated, searching your query')
            how = query
            max_results = 1
            how_to = search_wikihow(how, max_results)
            assert len(how_to) == 1
            how_to[0].print()
            speak(how_to[0].summary)
        
        elif 'send whatsapp message' in query or 'whatsapp message' in query:
            speak('Sir who is the recipient?') 
            recipient = myCommand()
            if 'papa' in query or 'dad' in query:
                speak('and sir what is the message for your dad?')
                mes = myCommand()
                webbrowser.open('https://web.whatsapp.com/send?phone=+919899992756&text='+mes)
                time.sleep(10)
                pyautogui.press('enter')

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
            speak("I'd have a favourite fruit or vegetable when I'll be able to eat like you\n(Maybe in the future, you never know!)")

        elif 'abort' in query or 'stop' in query or 'bye' in query or 'nothing' in query or 'no command' in query:
            speak('Ok, bye sir')

            if a+b > 0:
                speak("Just wanted to say one more thing, By analyzing your replies I've found that you had a nice experience with me.")
                speak('Goodbye!')
                
            if a+b < -1:
                speak("Just wanted to say one more thing, By analyzing your replies I've found that you had a bad impression on me. I will be better next time")
                speak('Goodbye!')
                
            if a+b ==0:
                speak('We will meet again')
                
            break

        elif 'take a break' in query or 'you may sleep' in query:
            speak('Ok sir you can call me anytime')
            n=ToastNotifier()
            n.show_toast("Fryday", "I am Sleeping",
            icon_path ="./Resources/icons/ironman.ico")
            Sleepword()

        elif 'hello' in query or 'sup' in query or 'hi friday' in query or 'hi Friday' in query:
            speak('Hello, Sir')
        
        elif 'i hate you' in query or 'you are bad' in query or 'you are not good' in query:
             speak("I am sorry if I disappointed you, my work is still in progress. Maybe one day I will be perfect.")
             b = b-5

        elif 'i like you' in query or 'you are good' in query or 'you are nice' in query or 'you are not bad' in query:
            reply1 = ['Thanks, sam!','Nice to hear, sam',"Thanks, Sir","I was made to hear that", 'thanks, sam']
            speak(random.choice(reply1))
            a = a+5

        elif 'your name' in query:
            ans = ['you can call me friday','I am Friday','Friday']
            speak(random.choice(ans))
        
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
        
        elif 'chrome' in query:
            ChromeAuto(query)

        elif 'youtube' in query:
            YoutubeAuto(query)

        elif 'where is' in query:
            Place = query.replace("where is","")
            Place = Place.replace("friday","")
            Place = Place.replace("fryday","")
            Place = Place.replace("Fryday","")
            Place = Place.replace("Friday","")
            place = Place
            GoogleMap(place)

        elif 'translate' in query:
            line = query.replace("translate","")
            line = line.replace("Friday","")
            line = line.replace("Fryday","")
            line = line.replace("friday","")
            line = line.replace("fryday","")
            tran(line)

        else:
            query = query
            client = wolframalpha.Client('K9T6JG-KJVJTEK8X7')
            try:
                try:
                    res = client.query(query)
                    results = next(res.results).text
                    speak(results)
                        
                except:
                    results = wikipedia.summary(query, sentences=5)
                    speak("I have Found that - ")
                    print(results)
                    speak(results)
            
            except:
                speak("Sorry some servers are not responding, please try again later ")
        
if __name__ == "__main__":
    Fryday()
