from datetime import *
import psycopg2

logged_in = False # In het begin is er niemand ingelogd en kan dus niemand berichten checken
logged_in_user = None # In het begin is er niemand ingelogd en is de username dus nog niet bestaand

def register_moderator():
    """
    Deze functie zorgt voor het registreren van een moderator. De moderator-acountdetails schrijft hij weg naar
    de database in pgadmin4.
    :return:
    """
    connection = psycopg2.connect(user="postgres", password="1234", host="localhost", database="stationszuil", port="5432")
    c = connection.cursor()
    username = input("username: ")
    email = input("email: ")
    password = input("password: ")
    registered_moderators = ('SELECT * FROM moderators')
    c.execute(registered_moderators)
    if username in registered_moderators: # Als de username al bestaat in de database kan dit niet, want dit is de primary key, die moet uniek zijn.
        print("This username has already been taken, please choose a different one.")
        return register_moderator()
    else:
        details = (username, email, password)
        insertion = ('INSERT INTO moderators (username, email, password) VALUES (%s,%s,%s)')
        c.execute(insertion, details) # Insert de account details naar de database

    connection.commit()
    c.close()

def login_moderator():
    """
    Deze functie zorgt ervoor dat je kan inloggen als moderator and berichten kan gaan keuren
    :return:
    """

    global logged_in
    global logged_in_user
    connection = psycopg2.connect(user="postgres", password="1234", host="localhost", database="stationszuil", port="5432")
    c = connection.cursor()

    username = input("username: ")
    password = input("password: ")
    c.execute('SELECT username, password FROM moderators') # Haal de bestaande moderators op
    fetched = c.fetchall()
    for moderator in fetched: # Loop door alle moderators om te kijken of deze bestaat
        if username in moderator:
            if password in moderator:
                print("You are now logged in as a moderator.")
                logged_in = True
                logged_in_user = username
                menu()
        else:
            print("This user does not exist in our database.")
            return login_moderator()

    connection.commit()
    c.close()

def push_checked_message():
    """
    Deze functie checked de opgegeven berichten. Hij leest ze vanuit messages.txt en verwijdert de al
    gekeurde berichten. Dit zorgt voor een efficiënte werking. Daarnaast schrijft deze functie alle benodigde
    informatie naar de database in de tabel 'bericht'.
    :return:
    """
    connection = psycopg2.connect(user="postgres", password="1234", host="localhost", database="stationszuil", port="5432")
    c = connection.cursor()
    c.execute("SELECT email FROM moderators WHERE username = %s", [logged_in_user]) # Haalt de email van de ingelogde moderator op om die later weg te schrijven naar kolom 'bericht'
    email = c.fetchall()
    now = datetime.now()
    checkTimeStamp = now.strftime("%d/%m/%Y %H:%M:%S") # Maakt een string format voor de datum en tijd
    with open("messages.txt", "r+") as s:
        lines = s.readlines()
        uncheckedMessages = lines
        for value in lines: # looped door de lijst 'lines' heen om alle verschillende variabele te definiëren
            print(uncheckedMessages)
            message = value.split(';')[0]
            submissionTimeStamp = value.split(';')[1]
            name = value.split(';')[2]
            station = value.split(';')[3]

            print(message)
            check_message = input("Is this message good? (Y/N)\n>").lower()

            if check_message == 'y': # Als het bericht goedgekeurd is schrijft deze if statement het weg naar de database en verwijdert het gekeurde bericht.
                show = True
                insertion = ('INSERT INTO bericht (message, submissionTimestamp, name, station, username, email, checkTimestamp, show) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)')
                insertion_data = (message, submissionTimeStamp, name, station, logged_in_user, email, checkTimeStamp, show)
                c.execute(insertion, insertion_data)
                string = message + ';' + submissionTimeStamp + ';' + name + ';' + station + ';' + '\n'
                uncheckedMessages.remove(string)
            elif check_message == 'n':
                string = message + ';' + submissionTimeStamp + ';' + name + ';' + station + ';' + '\n'
                uncheckedMessages.remove(string)
                continue
            elif check_message == 'stop':
                print(f'There are {len(uncheckedMessages)} left.')
                break

    with open('messages.txt', 'w') as fp:
        fp.write('')
        fp.write(''.join(uncheckedMessages))

    connection.commit()
    c.close()

def menu():
    """
    Dit is het menu voor de moderators
    :return:
    """
    global logged_in_user
    while logged_in:
        moderator_menu_choices = int(input("1. check messages\n"
                                           "2. logout\n>"))
        if moderator_menu_choices == 1:
            push_checked_message()
        elif moderator_menu_choices == 2:
            logged_in_user = None
            break

