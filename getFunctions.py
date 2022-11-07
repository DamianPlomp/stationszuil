import psycopg2

def get_messages():
    """
    Deze functie haalt de laatste vijf berichten op uit de kolom 'bericht' en returned deze
    :return:
    """
    connection = psycopg2.connect(user="postgres", password="1234", host="localhost", database="stationszuil",
                                  port="5432")
    c = connection.cursor()

    messageslst = []

    c.execute('SELECT message, station FROM bericht ORDER BY submissionTimeStamp DESC limit 5') # Selecteert laatste vijf berichten
    message_info = c.fetchall()
    for msg in message_info:
        messageslst.append(msg[1])
        messageslst.append(': ')
        messageslst.append(msg[0])
        messageslst.append('\n')

    connection.commit()
    c.close()

    return messageslst

def get_facilities():
    """
    Deze functie haalt de bijbehorende faciliteiten op die bij de laatste vijf berichten horen. We willen echter hebben
    dat hij de naam van de faciliteiten returned en niet true/false.
    :return:
    """
    facilities = ['station_city', 'country', 'ov_bike', 'elevator', 'toilet', 'park_and_ride']

    connection = psycopg2.connect(user="postgres", password="1234", host="localhost", database="stationszuil",
                                  port="5432")
    c = connection.cursor()

    facilities_there = []

    query = ("SELECT country, ov_bike, elevator, toilet, park_and_ride FROM station_service AS S INNER JOIN bericht AS B ON S.station_city = B.station ORDER BY submissiontimestamp DESC limit 5 ")
    c.execute(query)
    booleans = c.fetchall()
    for facility, facility_true in zip(facilities, booleans[0]): # Met deze for-loop zorg ik ervoor dat ik de namen krijg van de faciliteiten die aanwezig zijn.
        if isinstance(facility_true, str):
            facilities_there.append(facility_true)
        elif facility_true:
            facilities_there.append(facility)

    connection.commit()
    c.close()

    return facilities_there

