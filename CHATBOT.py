import random



command_1 = ["hello",
'wake up',
'utho',
'you there',
'hey',
'hi',
]

Reply_1 = [
    "Greetings",
    "Hello",
    "Good morning!",
    "Rise and shine!",
    "It's a new day!",
    "Time to start afresh!",
    "Hello there!",
    "Greetings!",
    "Hi!",
    "Good day!",
    "Welcome!",
    "Hey!",
    "Howdy!",
    "Salutations!",
    "Nice to meet you!",
    "Greetings, sir!",
    "Hi there, what can I do for you?",
    "Hello! How can I assist you today?",
    "Hey, how's it going?",
    "Hi! What's on your mind?",
    "Good to see you!",
    "Hello, friend!",
    "Hi, how can I help you today?",
    "Greetings and salutations!",
    "Hey there!",
    "Hey!",
    "Hello!",
    "Hi!",
    "Greetings!",
    "Hey, how's it going?",
    "Hey, what's up?",
    "Hey, nice to see you!",
    "Hey, how can I help you?",
    "Hey, long time no see!",
    "Hello there!",
    "Hi!",
    "Hey!",
    "Greetings!",
    "Hi, how are you?",
    "Hi, nice to meet you!",
    "Hey there, what's up?",
    "Hi, it's great to see you!",
    "Hello, how can I help you?",
    "Hey, good to have you here!",
]

command_2 = ["bye",
"go and sleep",
"sleep",
"shut down"]

Reply_2 = [
    "Goodbye! Take care and see you soon.",
    "Rest well! Sweet dreams await.",
    "Sweet dreams! Have a peaceful night.",
    "Shutting down... Until we meet again!",
]

def chhaterbot(text):

    for word in text.split():

        if word in command_1:
            return random.choice(Reply_1) + "."

        elif word in command_2:
            return random.choice(Reply_2) + "."

