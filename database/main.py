import hashlib
import json
import os

CLEAR_PRINT = [True, 100]
CASH = 1000


def clear():
    """
    Clears the terminal window.
    If a mac is being used, it runs the "clear" command.
    If a windows machine is being used, it runs the "cls" command.
    If it can't figure out what system is being used, it will print a newline CLEAR_PRINT[1] times.

    However, it can also be overriden if CLEAR_PRINT[0] is set to true.
    """

    if not CLEAR_PRINT[0]:
        try:
            if os.name == "nt":
                # For windows.
                os.system("cls")

            elif os.name == "posix":
                # For mac/linux.
                os.system("clear")

            else:
                # Unknown operating system, just print a newline a bunch of times.
                print("\n" * CLEAR_PRINT[1])

        except:
            # Can't figure out the operating system, safest bet is to just print a newline a bunch of times.
            print("\n" * CLEAR_PRINT[1])

    else:
        # The clearing of screen is overriden, so we just print a newline CLEAR_PRINT[1] times.
        print("\n" * CLEAR_PRINT[1])


def hash(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()


def get_id(username, password):
    return hash(username + password)


def get_credentials():
    username = input("Username: ")

    if username == "quit":
        return "quit"

    password = input("Password: ")

    if password == "quit":
        return "quit"

    print("")

    user_id = get_id(username, password)
    filename = "data/" + user_id + ".json"

    does_exist = False

    try:
        with open(filename, "r") as f:
            f.read()

        does_exist = True

    except:
        # Account does not exist
        does_exist = False

    return username, password, user_id, filename, does_exist


def open_screen():
    input("Hello and Welcome to BANKING SIMULATOR 1976! (Press <ENTER> to continue) ")
    print("")

    start_query = ""

    while start_query != "y" or start_query != "n":
        start_query = input("So, would you like to start? [y,n] ")[0].lower()

        if start_query == "n":
            input("I guess you're one of those people who carry out their actions with no respect for others. I feel pretty hurt now. But I understand. ")
            quit()

        if start_query == "y":
            break

    input("Awesome. Let's get started. ")
    clear()


def open_account():
    global CASH

    print("Ok, I understand you'd like to create your account. Let's get started: \n")

    login_data = get_credentials()

    if login_data == "quit":
        return

    else:
        username, password, user_id, filename, does_exist = login_data

    if does_exist:
        input("I'm sorry, that account already exists. Please try again later. ")
        return

    account_data = {
        "username": username,
        "money": 0,
    }

    initial_deposit = input(
        "Would you like to make an initial deposit? [y,n] "
    )[0].lower()

    if initial_deposit == "y":
        while True:
            try:
                deposit = int(input("How much would you like to add? "))

            except:
                input("I'm sorry, that's not a valid amount. Please try again. ")
                continue

            if (CASH - deposit) < 0:
                input(
                    "I'm sorry, you don't have that much money. The most you can put in is £{}. ".format(CASH))
                continue

            CASH = CASH - deposit

            account_data["money"] += deposit
            break

    with open(filename, "w") as f:
        f.write(json.dumps(account_data, ensure_ascii=False))

    print("")

    input("Thank you for opening an account with us. Press <ENTER> to continue.")


def close_account():
    print("I hear you'd like to close your account. Mind telling us why? ")
    reason = input("I'd like to close my account because ")

    print("")

    input("That's the worst reason I've ever heard. Anyway...")

    print("")

    login_data = get_credentials()

    if login_data == "quit":
        return

    else:
        username, password, user_id, filename, does_exist = login_data

    if not does_exist:
        print("I'm sorry, that account does not exist or you have entered the username or password incorrectly. Please try again later.")
        input("Press <ENTER> to continue. ")
        return

    input("This is your last chance to say goodbye to your account, so when you're done, press <ENTER>. ")

    os.remove(filename)

    print("")

    input("(By the way, we've pocketed your money)")


def look_account():
    print("Ok, so you want to look into your account. We need your credentials first:")

    print("")

    login_data = get_credentials()

    if login_data == "quit":
        return

    else:
        username, password, user_id, filename, does_exist = login_data

    if not does_exist:
        print("I'm sorry, that account does not exist or you have entered the username or password incorrectly. Please try again later.")
        input("Press <ENTER> to continue. ")
        return

    account_data = {}

    with open(filename, "r") as f:
        account_data = json.loads(f.read())

    print("")

    print("Name: {}".format(account_data["username"]))
    print("Current Funds: £{}".format(account_data["money"]))

    print("")

    input("Press <ENTER> when you've finished looking.")


def deposit():
    global CASH

    print("We need your credentials to deposit any money:")

    print("")

    login_data = get_credentials()

    if login_data == "quit":
        return

    else:
        username, password, user_id, filename, does_exist = login_data

    if not does_exist:
        print("I'm sorry, that account does not exist or you have entered the username or password incorrectly. Please try again later.")
        input("Press <ENTER> to continue. ")
        return

    is_number = False
    deposit_amount = 0

    while not is_number:
        deposit_amount = input(
            "Ok, how much would you like to deposit? You have £{} in cash. ".format(CASH))

        try:
            deposit_amount = float(deposit_amount)
            is_number = True

        except:
            input("I'm sorry, that's not a valid amount. Please try again. ")
            is_number = False

        if (CASH - deposit_amount) < 0:
            input(
                "I'm sorry, you don't have that much money. The most you can put in is £{}. ".format(CASH))
            continue

    CASH -= deposit

    account_data = {}

    with open(filename, "r") as f:
        account_data = json.loads(f.read())

    account_data["money"] += deposit_amount

    with open(filename, "w") as f:
        f.write(json.dumps(account_data, ensure_ascii=True))

    print("")

    input("Press <ENTER> to finish. ")


def change_info():
    print("We need your current credentials to make any changes:")

    print("")

    login_data = get_credentials()

    if login_data == "quit":
        return

    else:
        username, password, user_id, filename, does_exist = login_data

    if not does_exist:
        print("I'm sorry, that account does not exist or you have entered the username or password incorrectly. Please try again later.")
        input("Press <ENTER> to continue. ")
        return

    print("")

    account_data = {}

    with open(filename, "r") as f:
        account_data = json.loads(f.read())

    new_username = input("What would you like your new username to be? ")
    new_password = input("What would you like your new password to be? ")

    new_user_id = get_id(new_username, new_password)
    new_filename = "data/" + new_user_id + ".json"

    account_data["username"] = new_username

    os.remove(filename)

    with open(new_filename, "w") as f:
        f.write(json.dumps(account_data, ensure_ascii=True))

    print("")

    input("Press <ENTER> to finish. ")


def leave():
    print("In the words of the famous song 'Hotel California'...")
    input("'You can check out any time you like, but you can never leave.' ")

    print("")

    checkout_query = input("Would you like to check out? ")[0].lower()

    if checkout_query == "n":
        return

    else:
        checkin_query = ""

        while not checkin_query == "y":
            checkin_query = input("Would you like to check in? ")[0].lower()

            if checkin_query == "n":
                print("You can check out, but you can't leave.")
                print("")

            elif checkin_query == "y":
                print("Wow, back so soon?\n")
                input("(Press <ENTER> to continue)")

                return


def main():
    global CASH

    while True:
        clear()
        print("Hello, Customer! You have options as to what you can do today.")
        print("You have £{} in cash that you can use for deposits.".format(CASH))

        print("")

        print("\t- 1. Open a new account.")
        print("\t- 2. Close an account.")
        print("\t- 3. Look at your account.")
        print("\t- 4. Deposit money into your account.")
        print("\t- 5. Change the information in your account.")
        print("\t- 6. Leave the bank.")

        print("")

        user_choice = input("What would you like to do today? ")

        print("")

        if user_choice not in ["1", "2", "3", "4", "5", "6"]:
            input("It was such a simple question and yet you still managed to mess it up. Type in the number that the action is associated with. (Press <ENTER> to continue) ")

        if user_choice == "1":
            open_account()

        elif user_choice == "2":
            close_account()

        elif user_choice == "3":
            look_account()

        elif user_choice == "4":
            deposit()

        elif user_choice == "5":
            change_info()

        elif user_choice == "6":
            leave()


if __name__ == "__main__":
    clear()

    # open_screen()
    main()
