import smtplib
import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import threading
import requests
from transformers import pipeline  # Import Hugging Face pipeline

# Initialize pyttsx3 engine
assistant = pyttsx3.init('sapi5')
voices = assistant.getProperty('voices')
assistant.setProperty('voice', voices[1].id)
assistant.setProperty('rate', 150)

# Function to speak out loud
def speak(audio):
    assistant.say(audio)
    print(f": {audio}")
    assistant.runAndWait()

# Optimized take command function (name requirement removed)
def takecommand():
    command = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        command.pause_threshold = 0.8
        command.energy_threshold = 300  

        while True:
            try:
                audio = command.listen(source, timeout=5, phrase_time_limit=8)
                print("Recognizing...")
                query = command.recognize_google(audio, language="en-in")
                print(f'You said: {query}')
                return query.lower()

            except sr.WaitTimeoutError:
                print("Timeout occurred, restarting listening...")
                continue
            except sr.UnknownValueError:
                print("Sorry, I didn't understand. Could you please repeat?")
                speak("Sorry, I didn't understand. Could you please repeat?")
                continue
            except sr.RequestError:
                print("Could not request results from the speech recognition service.")
                speak("I couldn't reach the speech recognition service. Please check your internet connection.")
                return "none"

# Initialize the Hugging Face pipeline for question-answering with a specific model
question_answerer = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

# Ask question function using Hugging Face
def ask_question(query):
    speak("What would you like to ask?")
    question = query  # Take question from the user's input
    context = "I am your personal assistant. I can help you with various tasks and answer your questions."  # Provide context if needed
    result = question_answerer(question=question, context=context)
    answer = result['answer']
    speak(answer)

# Get user name at startup
def get_user_name():
    speak("Hello, what would you like to call me?")
    global user_name
    user_name = takecommand().split()[0]
    speak(f"Nice to meet you, {user_name}. You can call me by saying my name first.")

# Delayed imports for on-demand functionality
def import_modules():
    global wikipedia
    import wikipedia

# Run this in a separate thread to import the modules in the background
def background_module_import():
    threading.Thread(target=import_modules).start()

# Get weather information
def get_weather():
    speak("Tell me your city")
    city = takecommand()
    api_key = "2a52eb44477d710bab5b4734ef32344b"  # Replace with your actual OpenWeatherMap API key
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    
    try:
        response = requests.get(weather_url)
        data = response.json()
        
        if data["cod"] != "404":
            main = data['main']
            temperature = main['temp'] - 273.15  # Convert from Kelvin to Celsius
            weather_desc = data['weather'][0]['description']
            speak(f"The temperature in {city} is {temperature:.2f} degrees Celsius with {weather_desc}.")
        else:
            speak("City not found.")
    except Exception as e:
        speak("Unable to get weather information.")

# Get current location using IP
def get_location():
    try:
        response = requests.get("http://ip-api.com/json/")
        data = response.json()
        city = data['city']
        country = data['country']
        speak(f"You are currently in {city}, {country}.")
    except Exception as e:
        speak("Unable to determine your location.")

# Google Search
def google_search(query):
    speak(f"Searching Google for {query}.")
    webbrowser.open(f"https://www.google.com/search?q={query}")

# Wikipedia Search
def wikipedia_search(query):
    speak(f"Searching Wikipedia for {query}.")
    try:
        summary = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(summary)
    except wikipedia.exceptions.PageError:
        speak("Sorry, I couldn't find anything on Wikipedia for that.")
    except wikipedia.exceptions.DisambiguationError as e:
        speak(f"Your query is too ambiguous. Did you mean: {e.options[:5]}?")

# YouTube Search
def youtube_search(query):
    speak(f"Searching YouTube for {query}.")
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

# System control functions for shutdown and restart
def system_control(command):
    if 'shut down' in command:
        speak("Shutting down the system.")
        os.system("shutdown /s /t 1")
    elif 'restart' in command:
        speak("Restarting the system.")
        os.system("shutdown /r /t 1")

# Set reminder function
def set_reminder():
    speak("What do you want to be reminded about?")
    reminder = takecommand()
    speak("In how many minutes?")
    minutes = int(takecommand())
    
    future_time = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
    speak(f"Reminder set for {minutes} minutes from now.")
    
    threading.Timer(minutes * 60, lambda: speak(f"Reminder: {reminder}")).start()

# Efficient news function
def get_news():
    try:
        speak("Fetching the latest news...")
        api_key = "028c9fc91fd04dd99d86ba3db42db83d"  # Replace with your actual news API key
        url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
        response = requests.get(url).json()
        for i, article in enumerate(response["articles"][:5]):
            speak(f"News {i + 1}: {article['title']}")
    except Exception as e:
        speak("Unable to fetch news at the moment.")

# Send email function
def send_email():
    speak("What is the subject of the email?")
    subject = takecommand()
    speak("What should I say in the email?")
    body = takecommand()
    email_content = f"Subject: {subject}\n\n{body}"
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('aroraratan77@gmail.com', 'ratan2007')  # Replace with actual credentials
        server.sendmail('aroraratan77@gmail.com', 'recipient_email@gmail.com', email_content)  # Update as needed
        server.close()
        speak("Email has been sent.")
    except Exception as e:
        speak("Unable to send the email. Check your internet connection or email credentials.")

# Main function to run the assistant
def run_assistant():
    get_user_name()  # Get user name at startup
    background_module_import()  # Imports modules in the background

    while True:
        query = takecommand()

        if query == "none":
            continue

        if 'weather' in query:
            get_weather()

        elif 'location' in query:
            get_location()

        elif 'reminder' in query:
            set_reminder()

        elif 'news' in query:
            get_news()

        elif 'email' in query:
            send_email()

        elif 'google' in query:
            speak("What should I search for on Google?")
            google_search(takecommand())
            
        elif 'wikipedia' in query:
            speak("What should I search for on Wikipedia?")
            wikipedia_search(takecommand())
            
        elif 'youtube' in query:
            speak("What should I search for on YouTube?")
            youtube_search(takecommand())
        
        elif 'shut down' in query or 'restart' in query:
            system_control(query)

        elif 'question' in query or 'tell me' in query:
            ask_question(takecommand())  # Call the question-answering model

        elif 'stop' in query or 'exit' in query:
            speak("Goodbye!")
            break

        else:
            speak("Sorry, I didn't understand that command.")

run_assistant()
