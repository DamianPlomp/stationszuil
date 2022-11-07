import psycopg2
from users import *
from moderators import *

def menu(): # Menu voor het kiezen van de verschillende opties.
    while True:
        print("Welcome to our program.")
        menu_choice = int(input("1. Would you like to leave a message?\n"
                            "2. Would you like to log in as a moderator?\n"
                            "3. Would you like to register as a moderator?\n"
                            "4. Would you like to shut down?\n>"))
        if menu_choice == 1:
            insert_message()
            return menu()
        elif menu_choice == 2:
            login_moderator()
            return menu()
        elif menu_choice == 3:
            register_moderator()
            return menu()
        elif menu_choice == 4:
            print("Thank you for using our program!")
            break

menu()
