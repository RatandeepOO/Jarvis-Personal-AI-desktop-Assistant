import pywhatkit

def sendmessage(recip_no, message):
    try:
        pywhatkit.sendwhatmsg_instantly(recip_no , message)
        
        (recip_no, message)
        print("Message sent successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
        
def messageinput1(list_no):
    
    # Collect inputs from the user
    name = input("Enter the name of the recipient: ")
    recip_no = str(list_no)
    message = input("Enter the message: ")
    sendmessage(recip_no, message)
        
def messageinput(list_no):        
    message = input("Enter the message: ")
    for i in range(len(list_no)):  # Corrected loop
        # Collect inputs from the user
        name = input("Enter the name of the recipient: ")
        recip_no = str(list_no[i])

        sendmessage(recip_no, message)

no = int(input("Enter number of contacts ::"))
if no > 1:
    list_no = input("Enter the numbers and separate by commas (e.g. +XXXXXXXXXX, +XXXXXXXXXX) :: ").split(',')
    messageinput(list_no)
else:
    list_no = [input("Enter the number:: ")]
    messageinput1(list_no)

print(list_no)
