import tkinter
from tkinter import *
import customtkinter
from getFunctions import *


def get_weather(station):
    weather_data = []

    weather_url = 'https://api.openweathermap.org/data/2.5/weather?q=' + station \
                  + '&appid=3312f47e4a2e28ca45183d4a8f2e29a4'

    response = requests.get(weather_url).json()

    temp = int(response['main']['temp'] - 273)
    description = response['weather'][0]['description']

    temp_string = str(temp) + str(chr(176))

    weather_data.append(temp_string)
    weather_data.append(description)

    weather_label.config(text=''.join(weather_data))

    return weather_data


root = customtkinter.CTk()

root.geometry('1024x564')

message_frame = customtkinter.CTkFrame(root, corner_radius=4, fg_color='#888B8D')
message_frame.place(x=165, y=170, height=300, width=200)

messageLabel = customtkinter.CTkLabel(message_frame, text=''.join(get_messages()), text_color='black', justify=LEFT).pack()

facilities_frame = customtkinter.CTkFrame(root, corner_radius=4, fg_color='#888B8D')
facilities_frame.place(x=405, y=170, height=300, width=200)

weather_frame = customtkinter.CTkFrame(root, corner_radius=4, fg_color='#888B8D')
weather_frame.place(x=645, y=170, height=300, width=200)

weather_label = customtkinter.CTkLabel(weather_frame, text='').pack()

weather_Amsterdam = customtkinter.CTkButton(root, text='Amsterdam', command=lambda: get_weather('Amsterdam'))
weather_Amsterdam.place(x=165, y=100, width=200)

weather_Groningen = customtkinter.CTkButton(root, text='Groningen', command=lambda: get_weather('Groningen'))
weather_Groningen.place(x=405, y=100, width=200)

weather_Delft = customtkinter.CTkButton(root, text='Delft', command=lambda: get_weather('Delft'))
weather_Delft.place(x=645, y=100, width=200)

root.mainloop()