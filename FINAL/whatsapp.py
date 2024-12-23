import webbrowser as web
import pywhatkit as py


def sendmsgnow(ph,msg):
    py.sendwhatmsg_instantly(ph,msg)

""" 
Phone number = String
Message = string
time hour = int
time min = int
"""
def whatsapp(ph,msg):
    sendmsgnow(ph,msg)
