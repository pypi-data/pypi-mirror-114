from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.3'
DESCRIPTION = 'fridayAI'
LONG_DESCRIPTION = '''A virtual assistant to automate windows based systems.
To install:
Run in Command Prompt: pip install fridayAI==<current_version>
Warning: Use the latest release only

Get Started:
This package comes with premade SpeechRecognition and Text-to-Speech systems.
Also it has premade function to get started including Automation(Chrome, Youtube, Windows, Instagram, Twitter, Gmail),
tell your loacation, AI-chatbot, Online-Class-Automation(Only for me), Answer any question, weather prediction, How-to-Do something
and many more.

To Use:
create a new pythonn file and write the following code:
from Fryday import Fryday
Fryday.Fryday()
'''

setup(
    name="fridayAI",
    version=VERSION,
    author="Sam",
    author_email="sam06eer@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['opencv-python','Pyaudio','pyttsx3','SpeechRecognition','keyboard','instaloader','wikipedia','wolframalpha','selenium','pyautogui','pywikihow','PyPDF2','twilio','pywhatkit','googletrans','google_trans_new','geopy','geocoder','win10toast'],
    keywords=['assistant','AI','Virtual','python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
