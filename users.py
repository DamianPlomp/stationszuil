import random
import time
from datetime import *

def insert_message():
    stations = ["Amsterdam", "Groningen", "Delft"]

    now = datetime.now()
    submissionTimeStamp = now.strftime("%d/%m/%Y %H:%M:%S")

    station = random.choice(stations)
    while True:
        print("Welcome to our message system, here you can leave a message about what you found of the trip.")
        name = input("Please tell us your name. If you wish to stay anonymous you can leave this field empty.\n>")
        if name == '':
            name = 'anonymous'
        else:
            name = name

        message = input("Please tell us in under 140 words what you thought of the trip.\n>")

        if len(message) > 140:
            print("This message was too long.")
            return insert_message()
        elif message == '':
            print("Oops! You didn't tell us what you thought of your trip!")
            return insert_message()

        information = [message, submissionTimeStamp, name, station]

        with open('messages.txt', 'a') as s:
            for info in information:
                s.write(info)
                s.write(';')
            s.write('\n')

        return_message = input("Would you like to leave another message? If so, please fill in '1', if not fill in '2'\n>")
        if insert_message() == 1:
            return insert_message()
        elif return_message == 2:
            print("Thank you for your time, we hope to see you again.")
            break

    return message, submissionTimeStamp, name, station

