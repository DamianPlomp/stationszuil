import psycopg2
import requests

def get_messages():
    connection = psycopg2.connect(user="postgres", password="1234", host="localhost", database="stationszuil",
                                  port="5432")
    c = connection.cursor()

    messageslst = []

    c.execute('SELECT message, station FROM bericht ORDER BY submissionTimeStamp DESC limit 5')
    message_info = c.fetchall()
    for msg in message_info:
        messageslst.append(msg[1])
        messageslst.append(': ')
        messageslst.append(msg[0])
        messageslst.append('\n')

    connection.commit()
    c.close()

    return messageslst

def get_weather(station):
    weather_data = []

    weather_url = 'https://api.openweathermap.org/data/2.5/weather?q=' + station + '&appid=3312f47e4a2e28ca45183d4a8f2e29a4'

    response = requests.get(weather_url).json()

    temp = int(response['main']['temp'] - 273)
    description = response['weather'][0]['description']

    temp_string = str(temp) + str(chr(176))

    weather_data.append(temp_string)
    weather_data.append(description)

    weather_label.config(text=''.join(weather_data))

    return weather_data
