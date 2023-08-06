# J.A.R.V.I.S. AI By Sam Industries
# Copyright 2021@SamIndustries

# Importing The Modules
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
import gtts
import playsound
from gtts import gTTS
from twilio.rest import Client, TwilioMonitorClient
import pywhatkit as kit
import google_trans_new
from google_trans_new import google_translator
from tkinter import *
import urllib.request
import json

client = wolframalpha.Client('K9T6JG-HWA9LVUUQW')
gt = google_trans_new.google_translator()

# TTS Function
def speak(text):
    print('Jarvis: '+text)
    tts = gTTS(text=text, lang='en', slow=False)
    filename = 'voice.mp3'
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

# STT Function (Hindi)
def myCommand():
   
    r = sr.Recognizer()                                                                                   
    with sr.Microphone() as source:                                                                       
        print("Listening...")
        r.pause_threshold =  1
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='hi')
        print('User: ' + query + '\n')
        
    except sr.UnknownValueError:
        query = myCommand()
        
    return query

#STT Function (English)
def permitcom():
   
    r = sr.Recognizer()                                                                                   
    with sr.Microphone() as source:                                                                       
        print("Listening...")
        r.pause_threshold =  1
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-in')
        print('User: ' + query + '\n')
        
    except sr.UnknownValueError:
        query = myCommand()
        
    return query

# Greeeting Function
def greetMe():
    currentH = int(datetime.datetime.now().hour)
    if currentH >= 0 and currentH < 12:
        speak('Good Morning!')

    if currentH >= 12 and currentH < 18:
        speak('Good Afternoon!')

    if currentH >= 18 and currentH !=0:
        speak('Good Evening!')

# Face BIometric Function

# Wakeword function to trigger Biometric Scan
def wakeword():
    # text = permitcom().lower()
    text = input('pass: ')
    print(text)
    if 'edith' in text or 'edit' in text:
        time.sleep(1)
        speak('अपने बायोमेट्रिक और आँखोंके स्कैन केलिए तैयार होजाओ')
        import cv2

        recognizer = cv2.face.LBPHFaceRecognizer_create() # Local Binary Patterns Histograms
        recognizer.read('trainer/trainer.yml')   #load trained model
        cascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascadePath) #initializing haar cascade for object detection approach

        font = cv2.FONT_HERSHEY_SIMPLEX #denotes the font type


        id = 2 #number of persons you want to Recognize


        names = ['','Spider-Man']  #names, leave first empty bcz counter starts from 0


        cam = cv2.VideoCapture(0, cv2.CAP_DSHOW) #cv2.CAP_DSHOW to remove warning
        cam.set(3, 640) # set video FrameWidht
        cam.set(4, 480) # set video FrameHeight

        # Define min window size to be recognized as a face
        minW = 0.1*cam.get(3)
        minH = 0.1*cam.get(4)

        # flag = True

        while True:

            ret, img =cam.read() #read the frames using the above created object

            converted_image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  #The function converts an input image from one color space to another

            faces = faceCascade.detectMultiScale( 
                converted_image,
                scaleFactor = 1.2,
                minNeighbors = 5,
                minSize = (int(minW), int(minH)),
            )

            for(x,y,w,h) in faces:

                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2) #used to draw a rectangle on any image

                id, accuracy = recognizer.predict(converted_image[y:y+h,x:x+w]) #to predict on every single image

                # Check if accuracy is less them 100 ==> "0" is perfect match 
                if (accuracy < 100):
                    id = names[id]
                    accuracy = "  {0}%".format(round(100 - accuracy))
                    edith()

                else:
                    id = "unknown"
                    accuracy = "  {0}%".format(round(100 - accuracy))
                
                cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
                # cv2.putText(img, str(accuracy), (x+5,y+h-5), font, 1, (255,255,0), 1)  
            
            cv2.imshow('camera',img) 

            k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
            if k == 27:
                break

        # Do a bit of cleanup
        print("Thanks for using this program, have a good day.")
        cam.release()
        cv2.destroyAllWindows()

    else:
        wakeword()

#PDF Reading Function
def pdf_reader():
    speak("sir please enter the full path to file in the shell")
    file = input("Enter the path here: ")
    book = open(file, 'rb')
    pdfReader = PyPDF2.PdfFileReader(book)
    pages = pdfReader.numPages
    speak(f"Total number of pages in this pdf {pages}")
    speak("sir please enter the page number I have to read")
    pg = permitcom()
    pg = int(pg)
    page = pdfReader.getPage(pg)
    text = page.extractText()
    speak(text)

#Main edith Function
def edith():
    pyautogui.press('esc')
    greetMe()
    a=0
    b=0
    c=float("-inf")
    while c > a+b:
        query = input('Question: ')

# Opening Websites

        if 'youtube' in query:
            speak('सर आप youtube पे क्या देखना पसंद करेंगे ')
            cond = myCommand()
            query = gt.translate(cond, lang_tgt='en')
            query = query.lower()
            kit.playonyt(query)
        
        elif 'google' in query:
            speak('सर आप googleपे क्या search करना चाहेंगे ')
            cond = myCommand()
            query = gt.translate(cond, lang_tgt='en')
            query = query.lower()
            webbrowser.open(f"{query}")
        
        elif 'stackoverflow' in query:
            speak('opening stackoverflow sir')
            webbrowser.open('www.stackoverflow.com')
        
        elif 'facebook' in query:
            speak('openingfacebook sir')
            webbrowser.open('www.facebook.com')
        
        elif 'twitter' in query:
            speak('opening twitter sir')
            webbrowser.open('www.twitter.com')
        
        elif 'gmail' in query:
            speak('opening gmail sir')
            webbrowser.open('mail.google.com')

        elif 'open instagram' in query:
            speak('opening instagram sir')
            webbrowser.open('instagram.com')

# Sending Messages and Making calls using twilio

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

# Open Camera Using OpenCV

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

# Small Talk

        elif 'better than siri' in query or 'better than cortana' in query:
            answer = ['I am friends with all AI devices',"I like all AI's"]
            speak(random.choice(answer))

        elif 'when were you made' in query or 'when were you created' in query:
            speak('I was created on the 18th of June 2020')
            
        elif 'i hate you' in query or 'you are bad' in query or 'you are not good' in query:
            speak("मुझे माफ़ करना अगर मैंने तुम्हे निराश किया हो| मैं अभी भी सीख रही हूँ और बेहतर बनने की कोशिश कर रही हु|")
            b = b-5

        elif 'i like you' in query or 'you are good' in query or 'you are nice' in query or 'you are not bad' in query:
            reply1 = ['शुक्रिया, sam!','सुन कर ख़ुशी हुई, sam',"अरे वाह! तुम कितने अच्छे हो, sam, शुक्रिया","मैं अपनी ख़ुशी तुम्हे बता भी नहीं सकती, sam! Thankyou so much!", 'thanks, sam']
            speak(random.choice(reply1))
            a = a+5
            
        elif 'who created you' in query or 'who made you' in query or 'who is your creator' in query or 'who was your creator' in query or 'who is your maker' in query:
            answer1 = ['Sam created me','I was created by Sam','Sam made me','I was made by Sam']
            speak(random.choice(answer1))

        elif "what's up" in query or 'how are you' in query or 'what are you doing' in query or 'how do you do' in query:
            answer2 = ['बस अपना काम कर रहीं हूँ!', 'मैं तो बढ़िया अपनी बताओ!', 'Never better!', 'मैं बढ़िया, और power से भरी हूँ!']
            speak(random.choice(answer2))
            speak('तुम कैसे हो ')

        elif 'also good' in query or 'am nice' in query or 'am fine' in query:
            speak('सुन कर अच्छा लगा ')

        elif 'not well' in query or 'am sad' in query:
            speak('ohh!, soo sorry')

        elif 'what is your favourite fruit' in query or 'what is your favourite vegetable' in query:
            speak("अभी मेरा कोई शरीर नहीं है जिसकी वजह से मैं कुछ खा नहीं सकती, अब कुछ खा नहीं सकती तो मेरा favourite और ना favourite क्या होगा | पर जल्द ही मेरा भी शरीर होगा तब शायद मेरा कुछ favourite हो ")

        elif 'abort' in query or 'stop' in query or 'bye' in query or 'nothing' in query or 'no command' in query:
            speak('ठीक है, bye sir')

            if a+b > 0:
                speak("बस एक बात और कहना चाहती हूँ।\nतुम्हारे answers को analyze करके, मैं समझ सकती हूँ कि तुम्हे मेरे साथ काफी अच्छा experience हुआ \nthanks sam, क्योंकि ये मेरे लिए काफ़ी मायने रखता है")
                speak('Goodbye!')
                
            if a+b < -1:
                speak("बस एक बात और कहना चाहती हूँ।\nतुम्हारे answers को analyze करके, मैंने देखा है कि तुम्हे मेरे साथ ज्यादा अच्छा experience नहीं हुआ। मैं अगली बार बेहतर होने की कोशिश करुँगी")
                speak('Goodbye!')
                
            if a+b ==0:
                speak('आशा है कि तुमने मेरे साथ अच्छा समय बिताया')
                speak('Goodbye!')
                
            break

        elif 'hello' in query or 'sup' in query:
            speak('hello')

        elif 'your name' in query or 'who are you' in query:
            speak('मैं edith हूँ.')
            speak('Sam की high-tech securityऔरdefense system')
            speak("Edith का मतलब हैं Even Dead, I'm The Hero")
            speak('Sam हीरोगिरी कभी नहीँ छोड़ेंगे|')

#Opening and Closing Notepad

        elif 'notepad' in query:
            speak('Opening Notepad')
            path = "C:\\WINDOWS\\system32\\notepad.exe"
            os.startfile(path)

        elif 'close notepad' in query:
            speak('closing notepad')
            os.system("taskkill /f /im notepad.exe")
        
#System Operations

        elif 'shut down' in query or 'shutdown' in query:
            os.system("taskkill /f /im GUI.exe")
            os.system("shutdown /s /t 5")

        elif 'restart the pc' in query or 'restart the system' in query or 'restart the computer' in query:
            os.system("shutdown /r /t 5")

        elif 'sleep the pc' in query or 'sleep the system' in query or 'sleep the computer' in query:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

        elif 'cmd' in query or 'command prompt' in query:
            speak('Opening Shell')
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
            img.save(f"{name}.png")
            speak("done sir, screenshot has been saved in our main folder")

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

# Hiding/Showing Files
        elif 'hide' in query:
            os.system("attrib +h /s /d")
            speak('done sir, all the file in this folder are now hidden')

        elif "visible" in query:
            os.system("attrib -h /s /d")
            speak('done sir, all the files in this are now visible to everyone, I hope you are taking this decision at full peace. ')

# Getting IP Address, Hostname and Location

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
                    print('According to me we are in '+city+' city of '+country+' country')
                    
            except:
                speak('Sorry sir, some of our monitoring systems are not working properly causing me unable to find our location')
                pass

#Reading PDF

        elif "read" in query or 'PDF' in query:
            pdf_reader()

#Downloading Instagram Profile

        elif 'insta profile' in query or 'profile on insta' in query or 'instagram profile' in query or 'profile on instagram' in query:
            speak('sir please enter the username of the profile')
            name = input('Enter the username here: ')
            webbrowser.open(f"www.instagram.com/{name}")
            speak(f"Sir here is the profile of the user {name}")
            time.sleep(3)
            speak('sir would you like to download the profile pic of this user')
            condition = myCommand().lower()
            if "yes" in condition or "ya" in condition or "sure" in condition or "yup" in condition:
                mod = instaloader.Instaloader()
                mod.download_profile(name, profile_pic_only=True)
                speak("done sir, profile pic has been saved in my main folder.")
            else:
                pass

#News

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
                speak('open news from browser')
            else:
                speak('ok no problem sir!')

# Sending Mails

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

#Posting Tweets

        elif 'tweet' in query:
            
            speak('मुझे क्याtweetकरनाचाहिए?')
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

#How-to-do SOmething

        elif 'how to' in query:
            speak('how-to-do mode activated, searching your query')
            how = query
            max_results = 1
            how_to = search_wikihow(how, max_results)
            assert len(how_to) == 1
            how_to[0].print()
            speak(how_to[0].summary)

# If no statement matches the condition then it will automatically try to respond to that

        else:
            query = query
            try:
                try:
                    res = client.query(query)
                    results = next(res.results).text
                    speak(results)
                    
                except:
                    results = wikipedia.summary(query, sentences=2)
                    speak("मुझे wikipedia पर कुछ मिला है - ")
                    speak(results)
        
            except:
                speak("Sorry एक internal server में error आ गया है | प्लीज बाद में try करें ")

#If Users Says rest or order to sleep, then this function will be called
def sleepword():
    text = permitcom().lower()
    if 'edith' in text or 'edit' in text:
        edith()
    else:
        sleepword()

#Secondary Edith Function(Called after exiting sleep)
def edith1():
    pyautogui.press('esc')
    start = ['at your service sir', 'always with you sir', 'always here sir', 'waiting for your command sir', 'yes sir', 'hello sir, may I help you with something']
    speak(random.choice(start))
    a=0
    b=0
    c=float("-inf")
    while c > a+b:
        query = input('Question: ')

# Opening Websites

        if 'youtube' in query:
            speak('सर आप youtube पे क्या देखना पसंद करेंगे ')
            cond = myCommand()
            query = gt.translate(cond, lang_tgt='en')
            query = query.lower()
            kit.playonyt(query)
        
        elif 'google' in query:
            speak('सर आप googleपे क्या search करना चाहेंगे ')
            cond = myCommand()
            query = gt.translate(cond, lang_tgt='en')
            query = query.lower()
            webbrowser.open(f"{query}")
        
        elif 'stackoverflow' in query:
            speak('opening stackoverflow sir')
            webbrowser.open('www.stackoverflow.com')
        
        elif 'facebook' in query:
            speak('openingfacebook sir')
            webbrowser.open('www.facebook.com')
        
        elif 'twitter' in query:
            speak('opening twitter sir')
            webbrowser.open('www.twitter.com')
        
        elif 'gmail' in query:
            speak('opening gmail sir')
            webbrowser.open('mail.google.com')

        elif 'open instagram' in query:
            speak('opening instagram sir')
            webbrowser.open('instagram.com')

# Sending Messages and Making calls using twilio

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

# Open Camera Using OpenCV

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

# Small Talk

        elif 'better than siri' in query or 'better than cortana' in query:
            answer = ['I am friends with all AI devices',"I like all AI's"]
            speak(random.choice(answer))

        elif 'when were you made' in query or 'when were you created' in query:
            speak('I was created on the 18th of June 2020')
            
        elif 'i hate you' in query or 'you are bad' in query or 'you are not good' in query:
            speak("मुझे माफ़ करना अगर मैंने तुम्हे निराश किया हो| मैं अभी भी सीख रही हूँ और बेहतर बनने की कोशिश कर रही हु|")
            b = b-5

        elif 'i like you' in query or 'you are good' in query or 'you are nice' in query or 'you are not bad' in query:
            reply1 = ['शुक्रिया, sam!','सुन कर ख़ुशी हुई, sam',"अरे वाह! तुम कितने अच्छे हो, sam, शुक्रिया","मैं अपनी ख़ुशी तुम्हे बता भी नहीं सकती, sam! Thankyou so much!", 'thanks, sam']
            speak(random.choice(reply1))
            a = a+5
            
        elif 'who created you' in query or 'who made you' in query or 'who is your creator' in query or 'who was your creator' in query or 'who is your maker' in query:
            answer1 = ['Sam created me','I was created by Sam','Sam made me','I was made by Sam']
            speak(random.choice(answer1))

        elif "what's up" in query or 'how are you' in query or 'what are you doing' in query or 'how do you do' in query:
            answer2 = ['बस अपना काम कर रहीं हूँ!', 'मैं तो बढ़िया अपनी बताओ!', 'Never better!', 'मैं बढ़िया, और power से भरी हूँ!']
            speak(random.choice(answer2))
            speak('तुम कैसे हो ')

        elif 'also good' in query or 'am nice' in query or 'am fine' in query:
            speak('सुन कर अच्छा लगा ')

        elif 'not well' in query or 'am sad' in query:
            speak('ohh!, soo sorry')

        elif 'what is your favourite fruit' in query or 'what is your favourite vegetable' in query:
            speak("अभी मेरा कोई शरीर नहीं है जिसकी वजह से मैं कुछ खा नहीं सकती, अब कुछ खा नहीं सकती तो मेरा favourite और ना favourite क्या होगा | पर जल्द ही मेरा भी शरीर होगा तब शायद मेरा कुछ favourite हो ")

        elif 'abort' in query or 'stop' in query or 'bye' in query or 'nothing' in query or 'no command' in query:
            speak('ठीक है, bye sir')

            if a+b > 0:
                speak("बस एक बात और कहना चाहती हूँ।\nतुम्हारे answers को analyze करके, मैं समझ सकती हूँ कि तुम्हे मेरे साथ काफी अच्छा experience हुआ \nthanks sam, क्योंकि ये मेरे लिए काफ़ी मायने रखता है")
                speak('Goodbye!')
                
            if a+b < -1:
                speak("बस एक बात और कहना चाहती हूँ।\nतुम्हारे answers को analyze करके, मैंने देखा है कि तुम्हे मेरे साथ ज्यादा अच्छा experience नहीं हुआ। मैं अगली बार बेहतर होने की कोशिश करुँगी")
                speak('Goodbye!')
                
            if a+b ==0:
                speak('आशा है कि तुमने मेरे साथ अच्छा समय बिताया')
                speak('Goodbye!')
                
            break

        elif 'hello' in query or 'sup' in query:
            speak('hello')

        elif 'your name' in query or 'who are you' in query:
            speak('मैं edith हूँ.')
            speak('Sam की high-tech securityऔरdefense system')
            speak("Edith का मतलब हैं Even Dead, I'm The Hero")
            speak('Sam हीरोगिरी कभी नहीँ छोड़ेंगे|')

#Opening and Closing Notepad

        elif 'notepad' in query:
            speak('Opening Notepad')
            path = "C:\\WINDOWS\\system32\\notepad.exe"
            os.startfile(path)

        elif 'close notepad' in query:
            speak('closing notepad')
            os.system("taskkill /f /im notepad.exe")
        
#System Operations

        elif 'shut down' in query or 'shutdown' in query:
            os.system("taskkill /f /im GUI.exe")
            os.system("shutdown /s /t 5")

        elif 'restart the pc' in query or 'restart the system' in query or 'restart the computer' in query:
            os.system("shutdown /r /t 5")

        elif 'sleep the pc' in query or 'sleep the system' in query or 'sleep the computer' in query:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

        elif 'cmd' in query or 'command prompt' in query:
            speak('Opening Shell')
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
            img.save(f"{name}.png")
            speak("done sir, screenshot has been saved in our main folder")

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

# Hiding/Showing Files
        elif 'hide' in query:
            os.system("attrib +h /s /d")
            speak('done sir, all the file in this folder are now hidden')

        elif "visible" in query:
            os.system("attrib -h /s /d")
            speak('done sir, all the files in this are now visible to everyone, I hope you are taking this decision at full peace. ')

# Getting IP Address, Hostname and Location

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
                    print('According to me we are in '+city+' city of '+country+' country')
                    
            except:
                speak('Sorry sir, some of our monitoring systems are not working properly causing me unable to find our location')
                pass

#Reading PDF

        elif "read" in query or 'PDF' in query:
            pdf_reader()

#Downloading Instagram Profile

        elif 'insta profile' in query or 'profile on insta' in query or 'instagram profile' in query or 'profile on instagram' in query:
            speak('sir please enter the username of the profile')
            name = input('Enter the username here: ')
            webbrowser.open(f"www.instagram.com/{name}")
            speak(f"Sir here is the profile of the user {name}")
            time.sleep(3)
            speak('sir would you like to download the profile pic of this user')
            condition = myCommand().lower()
            if "yes" in condition or "ya" in condition or "sure" in condition or "yup" in condition:
                mod = instaloader.Instaloader()
                mod.download_profile(name, profile_pic_only=True)
                speak("done sir, profile pic has been saved in my main folder.")
            else:
                pass

#News

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
                speak('open news from browser')
            else:
                speak('ok no problem sir!')

# Sending Mails

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

#Posting Tweets

        elif 'tweet' in query:
            
            speak('मुझे क्याtweetकरनाचाहिए?')
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

#How-to-do SOmething

        elif 'how to' in query:
            speak('how-to-do mode activated, searching your query')
            how = query
            max_results = 1
            how_to = search_wikihow(how, max_results)
            assert len(how_to) == 1
            how_to[0].print()
            speak(how_to[0].summary)

# If no statement matches the condition then it will automatically try to respond to that

        else:
            query = query
            try:
                try:
                    res = client.query(query)
                    results = next(res.results).text
                    speak(results)
                    
                except:
                    results = wikipedia.summary(query, sentences=2)
                    speak("मुझे wikipedia पर कुछ मिला है - ")
                    speak(results)
        
            except:
                speak("Sorry एक internal server में error आ गया है | प्लीज बाद में try करें ")


if __name__ == "__main__":
    edith()