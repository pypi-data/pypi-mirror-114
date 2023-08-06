import wolframalpha
from gtts import *
import google_trans_new
import os
import playsound
import wikipedia
import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate',150)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
speak('Good morning sir')

client = wolframalpha.Client('K9T6JG-KJVJTEK8X7')

# def speak(text):
#     print('Jarvis: '+text)
#     tts = gTTS(text=text, lang='en', slow=False)
#     filename = 'voice.mp3'
#     tts.save(filename)
#     playsound.playsound(filename)
#     os.remove(filename)


# while True:
#     gt = google_trans_new.google_translator()
    
#     query = input('Question: ')

#     try:
#         try:
#             res = client.query(query)
#             results = next(res.results).text
#             # result_hi = gt.translate(results, lang_tgt='eng')
#             speak(results)
                    
#         except:
#             results = wikipedia.summary(query, sentences=5)
#             # result_hi = gt.translate(results, lang_tgt='hi')
#             speak("मुझे हमारे serrvers पर कुछ मिला है  - ")
#             speak(results)
        
#     except:
#         speak("Sorry sir, हमारे कुछ servers अभी काम नहीं कर रहे please बाद में try करे")
