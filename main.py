import string
import random
import mysql.connector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def hello_user():
    global user_input
    input_bool = True
    while input_bool:
        try:
            user_input = int(
                input("Hello user !\n1. Create password,\n2. Check strenght of passowrd\n3. Save password\n4. Show "
                      "saved passwords\n"))
            input_bool = False
        except ValueError:
            print("Invalid input. Only int is possible!")
    return user_input


################## CLASS ####################

class SQLConnection:
    def __init__(self, username, userpassword):
        self.username = username
        self.userpassword = userpassword

        USER = 'root'
        PASSWORD = 'Zakopane35%'
        HOST = 'localhost'
        DATABASE = 'users'

        self.connection = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)

    def __del__(self):
        self.connection.close()

    def print_query(self, username):
        query = f"SELECT * FROM users WHERE username='{username}';"

        cursor = self.connection.cursor()
        cursor.execute(query)

        for (id, username, password) in cursor:
            print(f"{id} - {username} - {password}")

        self.connection.close()

    def insert_query(self, username, password):
        insertQuery = f"INSERT INTO users(username, password) VALUES('{username}','{password}')"
        insertData = {
            'username': self.username,
            'password': self.userpassword
        }
        cursor = self.connection.cursor()
        cursor.execute(insertQuery, insertData)

        self.connection.commit()
        self.connection.close()


class Password:

    def __init__(self):
        self.upercase = string.ascii_uppercase
        self.lowercase = string.ascii_lowercase
        self.numbers = string.digits
        self.symbols = string.punctuation

    def create_passoword(self):
        loop_handler = True
        user_input_how_secure = None
        n = 0
        while loop_handler:
            Light = self.upercase + self.numbers
            Middle = self.upercase + self.lowercase + self.numbers
            Hard = Middle + self.symbols
            try:
                user_input_how_secure = (input("How secure should be your pass? (Light,Middle,strong )"))
                n = int(input("How many characters would you like in your password?"))
            except ValueError:
                pass

            if user_input_how_secure.capitalize() == "Light":
                light_password = "".join(random.sample(Light, n))
                loop_handler = False
                return light_password
            elif user_input_how_secure.capitalize() == "Middle":
                middle_password = "".join(random.sample(Light, n))
                loop_handler = False
                return middle_password
            elif user_input_how_secure.capitalize() == "Strong":
                hard_password = "".join(random.sample(Hard, n))
                loop_handler = False
                return hard_password
            else:
                print("Invalid syntax, try again!")

    def passowrd_strenght_checker(self, passwordtocheck):

        self.passwordtocheck = passwordtocheck

        score = 0
        length = len(passwordtocheck)

        uper_case_number = 0
        lower_case_number = 0
        symbols_number = 0
        digits_number = 0

        for elem in passwordtocheck:
            if elem in self.upercase:
                uper_case_number += 1
            if elem in self.lowercase:
                lower_case_number += 1
            if elem in self.symbols:
                symbols_number += 1
            if elem in self.numbers:
                digits_number += 1

        uper_case = any([1 if c in self.upercase else 0 for c in passwordtocheck])
        lower_case = any([1 if c in self.lowercase else 0 for c in passwordtocheck])
        symbols = any([1 if c in self.symbols else 0 for c in passwordtocheck])
        digits = any([1 if c in self.numbers else 0 for c in passwordtocheck])

        characters = [uper_case, lower_case, symbols, digits]

        if sum(characters) > 1:
            score += 1
        if sum(characters) > 2:
            score += 2
        if sum(characters) > 3:
            score += 3

        if length > 8:
            score += 1
        if length > 12:
            score += 1
        if length > 17:
            score += 2
        if length > 20:
            score += 3

        with open('rockyou.txt', errors="ignore") as f:
            rockyou = f.read()

        if passwordtocheck in rockyou:
            print("Your password was found in common password list! Score 0")
            exit()

        print(f"Password length is {length}.\n"
              f"Lower case: {lower_case_number}\n"
              f"Uper case: {uper_case_number}\n"
              f"Digits: {digits_number}\n"
              f"Symbols: {symbols_number}")
        if score < 3:
            print(f"Your password is weak! Score {score}")
        elif 3 <= score < 5:
            print(f"Your password is ok! Score {score}")
        elif 5 <= score < 8:
            print(f"Your password is pretty good! Score {score}")
        elif score >= 8:
            print(f"Your password is super strong! Score {score}")

    def time_to_hack_password(self, userpassoword):
        PATH = 'D:\chromedriver.exe'

        chrome_options = Options()
        chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(PATH, options=chrome_options)
        driver.get('https://random-ize.com/how-long-to-hack-pass/')

        searchbox = driver.find_element_by_xpath('//*[@id="password"]')
        searchbox.send_keys(f"{userpassoword}")
        searchtime = driver.find_elements_by_xpath('//*[@id="time"]')
        print("Your password can be hacked in at the most: ", searchtime[0].text)
        driver.quit()


#    ------ main -----    #

if __name__ == '__main__':

    p1 = Password()
    user_choice = hello_user()

    if user_choice == 1:
        print(p1.create_passoword())
    elif user_choice == 2:
        passwordtocheck = input("Enter passowrd to check: \n")
        p1.passowrd_strenght_checker(passwordtocheck)
        p1.time_to_hack_password(passwordtocheck)

    elif user_choice == 3:
        username = input("Enter username > ")
        password = input("Enter passoword > ")
        sql = SQLConnection(username, password)
        sql.insert_query(username, password)

    elif user_choice == 4:
        username = input("Enter username > ")

        sql = SQLConnection(username, None)
        sql.print_query(username)
    else:
        print("Invalid syntax, try again!")
