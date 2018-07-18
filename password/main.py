import re
from time import sleep


def main(regex1, regex2, regex3, levels):
    regex1, regex2, regex3 = re.compile(
        regex1), re.compile(regex2), re.compile(regex3)

    input("Welcome to the AWESOME password checker! You can press enter to continue. ")

    password = ""

    while len(password) < 6 and password not in ["123456", "123456789", "qwerty", "12345678", "111111", "1234567890", "1234567", "password"]:
        password = input(
            "What is your password (we promise we don't keep it) >>> ")
        print("")

        if(len(password) < 6):
            print("I'm sorry, since we're all about security and good practices, you can't have a password that short, try making it over 6 letters long.")

        if password in ["123456", "123456789", "qwerty", "12345678", "111111", "1234567890", "1234567", "password"]:
            print("Come. On. Please, if that is your password, then you should go for a long walk in the forest thinking about what you've done and achieved with your life. Put in something secure this time, will you.")

    print("")
    print("...")
    sleep(1)

    print("")

    if re.match(regex1, password):
        print("Your password is a bit rubbish, to be honest. In cool kid terms, we would say it's {}.".format(
            levels[0]))

    elif re.match(regex1, password) and re.match(regex2, password):
        print("Your password is OK, I guess. It's not great and there is a lot you can improve on, but it's classed as {}.".format(
            levels[1]))

    elif re.match(regex1, password) and re.match(regex2, password) and re.match(regex3, password):
        print("Your password is actualy quite alright. It has everything required, so it's a {}.".format(
            levels[3]))


if __name__ == "__main__":
    stop_choice = ""

    while stop_choice != "y":
        main(re, re, re, [])

        stop_choice = input(
            "Press 'y' if you'd like to quit, but anything else if you want to go again."
        )
