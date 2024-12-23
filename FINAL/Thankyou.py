import pyttsx3

assistant = pyttsx3.init('sapi5')
voices = assistant.getProperty('voices')
print(voices)
assistant.setProperty('voices',voices[1].id)
assistant.setProperty('rate',150)


def speak(audio):
    print("    ")
    assistant.say(audio)
    print(f":{audio}")
    assistant.runAndWait()

