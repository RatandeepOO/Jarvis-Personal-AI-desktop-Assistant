import requests
import os
from PIL import Image
import pyttsx3
import speech_recognition as sr
import pyaudio


assistant = pyttsx3.init('sapi5')
voices = assistant.getProperty('voices')
assistant.setProperty('voices',voices[0].id)
assistant.setProperty('rate',150)

def speak(audio):
    print("    ")
    assistant.say(audio)
    print(f":{audio}")
    assistant.runAndWait()


def takecommand():
    command = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening..........")
        command.pause_threshold = 1
        audio = command.listen(source)

        try : 
            print("Recognising...")
            querry = command.recognize_google(audio,language="en-in")
            print(f'You said : {querry}')

        except:
            return "none"

        return querry.lower()





def nasanews(date):
    apikey = "4qay02XQL1ADxneyqbFiSOQsFrbqrJlfJUlCg8bc"

    url = "https://api.nasa.gov/planetary/apod?api_key=" + apikey

    params_ = {"date":str(date)}

    r = requests.get(url,params=params_ )
    data = r.json()
    print(data)

    info = data["explanation"]
    title = data['title']
    image = data['url']
    image_r = requests.get(image)
    file_name = str(date) + '.jpg'
    with open(file_name,'wb') as f:
        f.write(image_r.content)

    path_1 = "P:\\POLY\\RATANDEEP\\ratandeep pack\\nasa.py\\" + str(file_name)

    path_2 = "P:\\POLY\\RATANDEEP\\ratandeep pack\\nasa.py\\" + str(file_name)

    os.rename(path_1,path_2)
    img = Image.open(path_2)
    img.show()
    speak(f"Title is : {title}")
    speak(f"The news is :{info}")
