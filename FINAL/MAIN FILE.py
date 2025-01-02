import json
import smtplib
import pyttsx3
import datetime
import webbrowser
import os
import language_tool_python
import threading
import requests
import pyaudio
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
from vosk import Model, KaldiRecognizer
from googletrans import Translator

class Assistant:
    def __init__(self):
        # Initialize the text-to-speech engine
        self.assistant = pyttsx3.init('sapi5')
        voices = self.assistant.getProperty('voices')
        self.assistant.setProperty('voice', voices[1].id)
        self.assistant.setProperty('rate', 150)

        # Initialize the Vosk speech recognition model
        self.vosk_models = {
            "english": Model(r"FINAL\Models\vosk-model-small-en-in-0.4\vosk-model-small-en-in-0.4"),
            "hindi": Model(r"FINAL\Models\vosk-model-small-hi-0.22\vosk-model-small-hi-0.22")
        }
        self.current_lang = "english"

        # Initialize the mBERT question-answering model
        model_path = "mbert_model"  # Replace with your mBERT model directory
        self.qa_model = AutoModelForQuestionAnswering.from_pretrained(model_path)
        self.qa_tokenizer = AutoTokenizer.from_pretrained(model_path)

        # Initialize the translator
        self.translator = Translator()

        # Initialize grammar correction tool
        self.grammar_tool = language_tool_python.LanguageTool('en-US')

        # Load user details from a file
        self.user_details = self.load_user_details()

    # Function to speak out loud
    def speak(self, audio):
        self.assistant.say(audio)
        print(f": {audio}")
        self.assistant.runAndWait()

    # Function to take voice commands
    def take_command(self):
        self.speak("Listening...")
        recognizer = KaldiRecognizer(self.vosk_models[self.current_lang], 16000)
        mic = pyaudio.PyAudio()
        stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
        stream.start_stream()

        while True:
            try:
                data = stream.read(4096, exception_on_overflow=False)
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    query = result.get("text", "")
                    print(f'You said: {query}')
                    if self.user_details.get("language", "english") == "hindi":
                        query = self.translator.translate(query, src='hi', dest='en').text
                    return query.lower()
            except Exception:
                self.speak("An error occurred while recognizing speech.")
                return "none"

    def voice_typing_mode(self):
        """Enable voice typing mode."""
        self.speak("Voice typing mode activated. Say 'Jarvis stop' to exit.")
        recognizer = KaldiRecognizer(self.vosk_models[self.current_lang], 16000)
        mic = pyaudio.PyAudio()
        stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
        stream.start_stream()

        text = ""
        file_path = "voice_typing.txt"

        with open(file_path, "w") as file:
            while True:
                try:
                    data = stream.read(4096, exception_on_overflow=False)
                    if recognizer.AcceptWaveform(data):
                        result = json.loads(recognizer.Result())
                        spoken_text = result.get("text", "")
                        if "jarvis stop" in spoken_text.lower():
                            self.speak("Exiting voice typing mode.")
                            break
                        else:
                            corrected_text = self.correct_text(spoken_text)
                            text += corrected_text + " "
                            file.write(corrected_text + "\n")
                            print(f"Dictated: {corrected_text}")
                            self.speak(f"Typed: {corrected_text}")
                except Exception:
                    self.speak("An error occurred. Exiting voice typing mode.")
                    break

        stream.stop_stream()
        stream.close()
        mic.terminate()

        os.system(f"notepad.exe {file_path}")

    def correct_text(self, text):
        matches = self.grammar_tool.check(text)
        corrected_text = language_tool_python.utils.correct(text, matches)
        return corrected_text

    def load_user_details(self):
        try:
            with open("user_details.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {"language": "english"}

    def save_user_details(self):
        with open("user_details.json", "w") as file:
            json.dump(self.user_details, file)

    def get_user_details(self):
        if not self.user_details.get("name"):
            self.speak("Hello, What is your name?")
            self.user_details["name"] = self.take_command()
        if not self.user_details.get("city"):
            self.speak("Which city are you in?")
            self.user_details["city"] = self.take_command()
        if not self.user_details.get("email"):
            self.speak("Please provide your email address for sending emails.")
            self.user_details["email"] = self.take_command()
        self.save_user_details()
        self.speak(f"Nice to meet you, {self.user_details['name']}. You can call me by saying my name Jarvis.")

    def switch_language(self):
        if self.current_lang == "english":
            self.current_lang = "hindi"
            self.speak("भाषा हिंदी में बदल दी गई है।")
        else:
            self.current_lang = "english"
            self.speak("Language has been switched to English.")
        self.save_user_details()

    def get_weather(self):
        city = self.user_details.get("city", None)
        if not city:
            self.speak("Tell me your city")
            city = self.take_command()
            self.user_details["city"] = city
            self.save_user_details()

        api_key = "your_openweather_api_key"
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(weather_url)
            data = response.json()

            if data["cod"] != "404":
                main = data['main']
                temperature = main['temp'] - 273.15
                weather_desc = data['weather'][0]['description']
                self.speak(f"The temperature in {city} is {temperature:.2f} degrees Celsius with {weather_desc}.")
            else:
                self.speak("City not found.")
        except Exception:
            self.speak("Unable to get weather information.")

    def get_location(self):
        try:
            response = requests.get("http://ip-api.com/json/")
            data = response.json()
            city = data['city']
            country = data['country']
            self.speak(f"You are currently in {city}, {country}.")
        except Exception:
            self.speak("Unable to determine your location.")

    def google_search(self, query):
        self.speak(f"Searching Google for {query}.")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    def send_email(self):
        self.speak("What is the subject of the email?")
        subject = self.take_command()
        self.speak("What should I say in the email?")
        body = self.take_command()
        email_content = f"Subject: {subject}\n\n{body}"

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            sender_email = self.user_details.get("email")
            self.speak("Please confirm the recipient email address.")
            recipient_email = self.take_command()
            server.login(sender_email, "your_password")
            server.sendmail(sender_email, recipient_email, email_content)
            server.close()
            self.speak("Email has been sent.")
        except Exception:
            self.speak("Unable to send the email.")

    def ask_question(self, query):
        context = "I am your personal assistant. I can help you with various tasks and answer your questions."
        inputs = self.qa_tokenizer.encode_plus(query, context, return_tensors="pt")
        outputs = self.qa_model(**inputs)
        answer_start = outputs.start_logits.argmax()
        answer_end = outputs.end_logits.argmax()
        answer = self.qa_tokenizer.convert_tokens_to_string(
            self.qa_tokenizer.convert_ids_to_tokens(
                inputs['input_ids'][0][answer_start:answer_end + 1]
            )
        )
        if answer:
            self.speak(answer)
        else:
            self.speak("I couldn't find an answer. Please try rephrasing the question.")

    def run_assistant(self):
        self.get_user_details()

        while True:
            query = self.take_command()
            if query == "none":
                continue

            if 'voice typing' in query:
                self.voice_typing_mode()
            elif 'switch language' in query:
                self.switch_language()
            elif 'weather' in query:
                threading.Thread(target=self.get_weather).start()
            elif 'location' in query:
                threading.Thread(target=self.get_location).start()
            elif 'email' in query:
                threading.Thread(target=self.send_email).start()
            elif 'google' in query:
                self.speak("What should I search for on Google?")
                threading.Thread(target=self.google_search, args=(self.take_command(),)).start()
            elif 'question' in query:
                self.speak("What is your question?")
                threading.Thread(target=self.ask_question, args=(self.take_command(),)).start()
            elif 'exit' in query or 'stop' in query:
                self.speak("Goodbye!")
                break
            else:
                self.speak("I didn't understand that.")

if __name__ == "__main__":
    assistant = Assistant()
    assistant.run_assistant()
