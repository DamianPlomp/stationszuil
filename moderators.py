from datetime import *
import psycopg2

logged_in = False
logged_in_user = None

def register_moderator():
    connection = psycopg2.connect(user="postgres", password="1234", host="localhost", database="stationszuil", port="5432")
    c = connection.cursor()
    username = input("username: ")
    email = input("email: ")
    password = input("password: ")
    registered_moderators = ('SELECT * FROM moderators')
    c.execute(registered_moderators)
    if username in registered_moderators:
        print("This username has already been taken, please choose a different one.")
        return register_moderator()
    else:
        details = (username, email, password)
        insertion = ('INSERT INTO moderators (username, email, password) VALUES (%s,%s,%s)')
        c.execute(insertion, details)

    connection.commit()
    c.close()

def login_moderator(): # Details zijn vooraf al gemaakt (check txt file moderators)
    global logged_in
    global logged_in_user
    connection = psycopg2.connect(user="postgres", password="1234", host="localhost", database="stationszuil", port="5432")
    c = connection.cursor()

    username = input("username: ")
    password = input("password: ")
    c.execute('SELECT username, password FROM moderators')
    fetched = c.fetchall()
    for moderator in fetched:
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
    connection = psycopg2.connect(user="postgres", password="1234", host="localhost", database="stationszuil", port="5432")
    c = connection.cursor()
    c.execute("SELECT email FROM moderators WHERE username = %s", [logged_in_user])
    email = c.fetchall()
    now = datetime.now()
    checkTimeStamp = now.strftime("%d/%m/%Y %H:%M:%S")
    with open("messages.txt", "r+") as s:
        lines = s.readlines()
        uncheckedMessages = lines
        for value in lines:
            message = value.split(';')[0]
            submissionTimeStamp = value.split(';')[1]
            name = value.split(';')[2]
            station = value.split(';')[3]

            print(message)
            check_message = input("Is this message good? (Y/N)\n>").lower()

            if check_message == 'y':
                show = True
                insertion = ('INSERT INTO bericht (message, submissionTimestamp, name, station, username, email, checkTimestamp, show) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)')
                insertion_data = (message, submissionTimeStamp, name, station, logged_in_user, email, checkTimeStamp, show)
                c.execute(insertion, insertion_data)
                string = message + ';' + submissionTimeStamp + ';' + name + ';' + station + ';' + '\n'
                uncheckedMessages.remove(string)
            elif check_message == 'n':
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
    global logged_in_user
    while logged_in:
        moderator_menu_choices = int(input("1. check messages\n"
                                           "2. logout\n>"))
        if moderator_menu_choices == 1:
            push_checked_message()
        elif moderator_menu_choices == 2:
            logged_in_user = None
            break

login_moderator()