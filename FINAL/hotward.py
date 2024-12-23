import os
import speech_recognition as sr

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

while True:

    wake_up = takecommand()

    if "wake up" in wake_up:
            os.startfile('P:\\POLY\\RATANDEEP\\ratandeep pack\\MAIN.py')
    else :
        print("nothing.........")