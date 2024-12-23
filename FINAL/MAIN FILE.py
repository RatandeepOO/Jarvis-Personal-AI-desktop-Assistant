import smtplib
import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import threading
import requests
import whatsapp as wt
from transformers import pipeline  

class Assistant:
    def __init__(self):
        # Initialize the text-to-speech engine
        self.assistant = pyttsx3.init('sapi5')
        voices = self.assistant.getProperty('voices')
        self.assistant.setProperty('voice', voices[1].id)
        self.assistant.setProperty('rate', 150)

        # Initialize the speech recognition
        self.recognizer = sr.Recognizer()

        # Initialize the question-answering pipeline
        self.question_answerer = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

        # User name
        self.user_name = None

    # Function to speak out loud
    def speak(self, audio):
        self.assistant.say(audio)
        print(f": {audio}")
        self.assistant.runAndWait()

    # Function to take voice commands
    def take_command(self):
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.pause_threshold = 0.8
            self.recognizer.energy_threshold = 300  

            while True:
                try:
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)
                    print("Recognizing...")
                    query = self.recognizer.recognize_google(audio, language="en-in")
                    print(f'You said: {query}')
                    return query.lower()
                except sr.WaitTimeoutError:
                    print("Timeout occurred, restarting listening...")
                    continue
                except sr.UnknownValueError:
                    self.speak("Sorry, I didn't understand. Could you please repeat?")
                    continue
                except sr.RequestError:
                    self.speak("Could not request results from the speech recognition service.")
                    return "none"

    # Get user name at startup
    def get_user_name(self):
        self.speak("Hello, Would you like to tell me your name?")
        self.user_name = self.take_command().split()[0]
        self.speak(f"Nice to meet you, {self.user_name}. You can call me by saying my name Jarvis.")

    # Method for getting weather information
    def get_weather(self):
        self.speak("Tell me your city")
        city = self.take_command()
        api_key = "2a52eb44477d710bab5b4734ef32344b"  # Replace with your actual OpenWeatherMap API key
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        
        try:
            response = requests.get(weather_url)
            data = response.json()
            
            if data["cod"] != "404":
                main = data['main']
                temperature = main['temp'] - 273.15  # Convert from Kelvin to Celsius
                weather_desc = data['weather'][0]['description']
                self.speak(f"The temperature in {city} is {temperature:.2f} degrees Celsius with {weather_desc}.")
            else:
                self.speak("City not found.")
        except Exception as e:
            self.speak("Unable to get weather information.")

    # Method for getting location using IP
    def get_location(self):
        try:
            response = requests.get("http://ip-api.com/json/")
            data = response.json()
            city = data['city']
            country = data['country']
            self.speak(f"You are currently in {city}, {country}.")
        except Exception as e:
            self.speak("Unable to determine your location.")

    # Method for searching Google
    def google_search(self, query):
        self.speak(f"Searching Google for {query}.")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    # Method for sending emails
    def send_email(self):
        self.speak("What is the subject of the email?")
        subject = self.take_command()
        self.speak("What should I say in the email?")
        body = self.take_command()
        email_content = f"Subject: {subject}\n\n{body}"
        
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login('your_email@gmail.com', 'your_password')  # Replace with actual credentials
            server.sendmail('your_email@gmail.com', 'recipient_email@gmail.com', email_content)  # Update as needed
            server.close()
            self.speak("Email has been sent.")
        except Exception as e:
            self.speak("Unable to send the email. Check your internet connection or email credentials.")

    # Method for asking questions using Hugging Face
    def ask_question(self, query):
        self.speak("What would you like to ask?")
        question = query
        context = "I am your personal assistant. I can help you with various tasks and answer your questions."
        result = self.question_answerer(question=question, context=context)
        answer = result['answer']
        self.speak(answer)
        
    def whatmsg(self,query):
        self.speak("Whom would you like to send message")
        person = query()
        self.speak("What would you like to say ")
        message = self.take_command()
        msg = wt.whatsapp(person,message)
        self.speak("Your message is ready to be sent")
        self.speak("Please confirm your message")
        
        

    # Main method to run the assistant
    def run_assistant(self):
        username=self.get_user_name()  # Get user name at startup

        while True:
            query = self.take_command()
            if query == "none":
                continue

            # Create threads for different tasks
            if 'weather' in query:
                threading.Thread(target=self.get_weather).start()
            elif 'location' in query:
                threading.Thread(target=self.get_location).start()
            elif 'email' in query:
                threading.Thread(target=self.send_email).start()
            elif 'google' in query:
                self.speak("What should I search for on Google?")
                threading.Thread(target=self.google_search, args=(self.take_command(),)).start()
            elif 'question' in query or 'tell me' in query:
                self.speak("You can tell me any thing")
                threading.Thread(target=self.ask_question, args=(self.take_command(),)).start()
            elif 'whatsapp' in query:
                self.speak("Sending whatsapp message")
                threading.Thread(target=self.whatmsg , args=(self.take_command(),)).start()
            elif 'shutdown' in query:
                self.speak("Shutting your device down. Thankyou!!")
                threading.Thread(target=os.system("shutdown /s /t 1"))
            elif 'restart' in query:
                self.speak("Restarting your device. Thankyou!!")
                threading.Thread(target=os.system("shutdown /r /t 1"))
            elif 'stop' in query or 'exit' in query:
                self.speak(f"Goodbye!, Nice to meet you Mr. {username}")
                break
            else:
                self.speak("Sorry, I didn't understand that command.")

if __name__ == "__main__":
    assistant = Assistant()
    assistant.run_assistant()