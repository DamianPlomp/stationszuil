import tkinter
from tkinter import *
import customtkinter
import requests
from getFunctions import *

root = customtkinter.CTk()

root.geometry('1024x564')

root.title("StationsZuil")

def get_weather(station):
    """
    Deze functie haalt de weer op dat bij de aangegeven stad/station hoort. Dit is de enige 'get()' functie
    die in GUI.py staat, omdat ik gebruik moest maken van StringVars.
    :param station:
    :return:
    """
    weather_url = 'https://api.openweathermap.org/data/2.5/weather?q=' + station + '&appid=3312f47e4a2e28ca45183d4a8f2e29a4'

    response = requests.get(weather_url).json()

    temp = int(response['main']['temp'] - 273) # Haalt temperatuur data op en rekent dit om tot celcius
    description = response['weather'][0]['description'] # Haalt weer beschrijvingen op

    temp_string = str(temp) + str(chr(176))

    weather_data = []

    weather_data.append(temp_string)
    weather_data.append(description)

    my_string_var.set(''.join(weather_data))

    print(weather_data)

    return my_string_var

message_frame = customtkinter.CTkFrame(root, corner_radius=4, fg_color='#888B8D')
message_frame.place(x=165, y=170, height=300, width=200)

messageLabel = customtkinter.CTkLabel(message_frame, text=''.join(get_messages()), text_color='black', justify=LEFT).pack()

facilities_frame = customtkinter.CTkFrame(root, corner_radius=4, fg_color='#888B8D')
facilities_frame.place(x=405, y=170, height=300, width=200)

facilities_label = customtkinter.CTkLabel(facilities_frame, text=' '.join(get_facilities())).pack()

weather_frame = customtkinter.CTkFrame(root, corner_radius=4, fg_color='#888B8D')
weather_frame.place(x=645, y=170, height=300, width=200)

my_string_var = StringVar()

weather_label = customtkinter.CTkLabel(weather_frame, textvariable=my_string_var, text_color='black', justify=LEFT).pack()

weather_Amsterdam = customtkinter.CTkButton(root, text='Amsterdam', command=lambda: get_weather('Amsterdam'))
weather_Amsterdam.place(x=165, y=100, width=200)

weather_Groningen = customtkinter.CTkButton(root, text='Groningen', command=lambda: get_weather('Groningen'))
weather_Groningen.place(x=405, y=100, width=200)

weather_Delft = customtkinter.CTkButton(root, text='Delft', command=lambda: get_weather('Delft'))
weather_Delft.place(x=645, y=100, width=200)


root.mainloop()


