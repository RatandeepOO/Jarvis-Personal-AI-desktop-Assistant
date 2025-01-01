import pywhatkit as what

def sendmessage(recip_no, message, hour, minute):
    try:
        what.sendwhatmsg(recip_no, message, hour, minute)
        print("Message sent successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
        
def messageinput():
    for i in len(list_no):
        # Collect inputs from the user
        name = input("Enter the name of the recipient: ")
        recip_no = str(list_no[i])
        hour = int(input("Enter the hour (24-hour format): "))
        minute = int(input("Enter the minutes: "))
        message = input("Enter the message: ")
        sendmessage(recip_no, message, hour, minute)

list_no = eval(input("Enter the number and seprate by commas (e.g.  XXXXXXXXXX , XXXXXXXXXX)"))
