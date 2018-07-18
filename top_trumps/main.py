import cmd
import sys
import os
import time
import json
import random
import textwrap


### GLOBAL SETUP VARIABLES ###

CARD_PATH = "cards/dnd.json"
LOGO = ".------..------..------..------..------..------..------..------..------.\n|T.--. ||O.--. ||P.--. ||T.--. ||R.--. ||U.--. ||M.--. ||P.--. ||S.--. |\n| :/\: || :/\: || :/\: || :/\: || :(): || (\/) || (\/) || :/\: || :/\: |\n| (__) || :\/: || (__) || (__) || ()() || :\/: || :\/: || (__) || :\/: |\n| '--'T|| '--'O|| '--'P|| '--'T|| '--'R|| '--'U|| '--'M|| '--'P|| '--'S|\n`------'`------'`------'`------'`------'`------'`------'`------'`------'"

HEAD_COIN = """
                   *** ### ### ***
               *##                 ##*
           *##                         ##*
        *##                               ##*
      *##                                   ##*
    *##                                       ##*
   *##                                         ##*
  *##                                           ##*
 *##                                             ##*
 *##                                             ##*
 *##                    HEADS                    ##*
 *##                                             ##*
 *##                                             ##*
  *##                                           ##*
   *##                                         ##*
    *##                                       ##*
      *##                                   ##*
        *#                                ##*
           *##                         ##*
               *##                 ##*
                   *** ### ### ***"""

TAILS_COIN = """
                   *** ### ### ***
               *##                 ##*
           *##                         ##*
        *##                               ##*
      *##                                   ##*
    *##                                       ##*
   *##                                         ##*
  *##                                           ##*
 *##                                             ##*
 *##                                             ##*
 *##                    TAILS                    ##*
 *##                                             ##*
 *##                                             ##*
  *##                                           ##*
   *##                                         ##*
    *##                                       ##*
      *##                                   ##*
        *#                                ##*
           *##                         ##*
               *##                 ##*
                   *** ### ### ***"""

# TESTING controls how the game acts and will speed things certain things up for testing purposes.
TESTING = False

# Sets the maximum width that the text can go. The code below is just the length of the logo.
SCREEN_WIDTH = max(list(map(lambda x: len(x), LOGO.split("\n"))))

# Sets how fast the text is written on the screen when there is the one letter at a time effect.
DEFAULT_DELAY = [0.1, 0.2]

# Controls if the user should have to hit enter at the end of every line of written text.
DEFAULT_INPUT = False

# Speeds up/slows down all wait times to make gameplay faster. 2 = twice as fast, 0.5 = double speed.
SPEED_MODIFIER = 2

# Defines wether to use the command prompt commands to clear the screen, or just print a bunch of times. Useful for when testing the code using IDLE. The first value is whether to do so, and the second value is the amount of times.
CLEAR_PRINT = [False, 100]

# =========================

### CLASSES ###


class Card():
    # Object used to represent a single card/character.

    def __init__(self, name, description, traits):
        # Stores the name of the card.
        self.name = name

        # Stores the description of the card.
        self.description = description

        # Stores the different traits, i.e. wisdom, strength...
        self.traits = traits


class Player():
    # Object used to store a player. Carries information about their name and whatnot.

    def __init__(self, name, cards):
        self.name = name
        self.cards = cards

# =============

### PROGRAM FUNCTIONS ###


def sleep(wait_time, force=False):
    """
    Waits a certain amount of time, but won't if TESTING variable is set to True and force is False.

    [ wait_time ] !number => The amount of time to wait. Should be a number, so a float or integer.
    [ force ] (False) !bool => If testing mode is enabled, but you still need to wait, force will override that if set to true. Th default is false.
    """

    try:
        wait_time = float(wait_time)

    except:
        raise ValueError(
            "Error trying to convert variable wait_time in sleep function into a float. You put a {}. It needs to be a float or an integer.".format(
                wait_time
            )
        )

    if type(force) is not bool:
        raise ValueError(
            "'force' argument in function sleep should be a bool. You put a {}.".format(
                type(force)
            )
        )

    if TESTING and force is False:
        return

    elif force is True or TESTING is False:
        time.sleep(wait_time / SPEED_MODIFIER)


def display(text, width=SCREEN_WIDTH, end="\r\n"):
    """
    Displays text nicely on a set amount of columns.

    [ text ] !string => A string which contains the text that is to be displayed.
    [ width ] (SCREEN_WIDTH) !integer => An integer which sets the width of the text. The default is SCREEN_WIDTH.
    [ end ] ("\r\n") !string => A string which sets what is printed at the end of a piece of text. The default is "\r\n", which is basically just a newline.
    """

    if type(text) is not str:
        raise ValueError(
            "'text' argument in display function should be a string. You gave a {} value.".format(
                type(text)
            )
        )

    if type(width) is not int:
        raise ValueError(
            "'width' argument in display function should be an integer. You gave a {} value.".format(
                type(width)
            )
        )

    if type(end) is not str:
        raise ValueError(
            "'end' argument in display function should be a string. You gave a {} value.".format(
                type(end)
            )
        )

    text = textwrap.dedent(text).strip()
    print(textwrap.fill(text, width=width), end=end)


def write_text(string, letter_by_letter=True, should_input=DEFAULT_INPUT, input_end=" ", width=SCREEN_WIDTH, end="\r\n", delay_settings=DEFAULT_DELAY):
    """
    Prints text one character at a time with a slight delay. Adds a nice effect to the writing.

    [ string ] !string => A string of what to print.
    [ letter_by_letter ] (True) !boolean => Defines whether the text should be printed one letter at a time.
    [ should_input ] (DEFAULT_INPUT) !boolean => Defines whether the user should have to press enter before proceding.
    [ input_end ] (" ") !string => Defines what should be after the text when input mode is enabled.
    [ width ] (SCREEN_WIDTH) !integer => An integer which controls how long the text should be. Default is the SCREEN_WIDTH.
    [ end ] ("\r\n") !string => What gets printed onto the string. The default is "\r\n", or basically just a newline.
    [ delay_settings ] (DEFAULT_DELAY) !list => The first number in the list specifies the time to wait between letters, and the second is the time to wait before a newline. The default is DEFAULT_DELAY.

    """

    if type(string) is not str:
        try:
            string = str(string)
        except:
            raise ValueError(
                "'string' argugument in function write_text should be a string, whereas you gave a {} value.".format(
                    type(string)
                )
            )

    if type(letter_by_letter) is not bool:
        raise ValueError(
            "'letter_by_letter' argument in function write_text should be a boolean. Your argument has the {} type.".format(
                type(letter_by_letter)
            )
        )

    if type(should_input) is not bool:
        raise ValueError(
            "'should_input' argument in function write_text should be a boolean. You gave a {}.".format(
                type(should_input)
            )
        )

    if type(input_end) is not str:
        raise ValueError(
            "'input_end' argument in function write_text should be a string. You gave a {}.".format(
                type(input_end)
            )
        )

    if type(width) is not int:
        raise ValueError(
            "'width' argugument in function write_text should be a string, whereas you gave a {} value.".format(
                type(width)
            )
        )

    if type(end) is not str:
        raise ValueError(
            "'end' argugument in function write_text should be a string, whereas you gave a {} value.".format(
                type(end)
            )
        )

    if type(delay_settings) is not list:
        raise ValueError(
            "'delay_settings' argugument in function write_text should be either a list or None, whereas you gave a {} value.".format(
                type(delay_settings)
            )
        )

    if list(map(lambda x: type(x), delay_settings)) is not [float, float]:
        try:
            delay_settings = list(map(lambda x: float(x), delay_settings))

        except:
            raise ValueError(
                "'delay_settings' argument should be a list of floats, but the value you gave ({}) wasn't.".format(
                    delay_settings
                )
            )

        if len(delay_settings) is not 2:
            raise ValueError(
                "'delay_settings' argument should be a list of floats, but the value you gave ({}) wasn't.".format(
                    delay_settings
                )
            )

    per_character_delay = delay_settings[0]
    per_newline_delay = delay_settings[1]

    if letter_by_letter and not should_input:
        for char in string:
            sys.stdout.write(char)
            sys.stdout.flush()

            sleep(per_character_delay)

        sys.stdout.write(" ")

        sleep(per_newline_delay)
        sys.stdout.write(end)

        sys.stdout.flush()

    elif letter_by_letter and should_input:
        for char in string:
            sys.stdout.write(char)
            sys.stdout.flush()

            sleep(per_character_delay)

        sys.stdout.write(input_end)

        sleep(per_newline_delay)

        input()

        sys.stdout.flush()

    else:
        display(string, end=end)


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


def super_input(initial, initial_input, input_type, reprompt, reprompt_input):
    """
    The Super Input Function:
    So the idea with this function is that you can create an input which is super sanitized and handles errors and stuff for you.
    """

    print(initial)
    given_input = input(initial_input)

    while True:
        try:
            # Try convert it into specified type.
            print("")
            given_input = input_type(given_input)

        except:
            # Oops, there was an error.
            print(reprompt)
            given_input = input(reprompt_input)

            continue

        break

    return given_input


def program_close():
    """
    Exits the program nicely.
    """

    print("\n")
    sys.exit(0)


def shuffle(array):
    # More unstolen code.

    random.shuffle(array)
    return array


def read_card_file(file_path):
    # Gets card data from a card data path.

    with open(file_path, "r") as f:
        # Parses the data and stores it in the data variable.
        data = json.load(f)

    return data  # Returns the data.


def dict_to_card(card_dict):
    # Turns a dictonary into a Card object.
    return Card(card_dict["name"], card_dict["description"], card_dict["traits"])


def card_dict_to_card_array(full_card_dict):
    # Takes a entire card dict and converts it into a list of the cards.

    cards = full_card_dict  # Just cards.
    card_array = []

    for card_name in cards:
        card_array.append(dict_to_card(card_name))

    return card_array


def render_card(card):
    # Takes a card object and prints it as a nice looking card.

    name = "Name: {}".format(card.name)

    if card.description != "":
        description = "Description: {}".format(card.description)

    else:
        description = "Description: No description provided.\n"

    traits = "Traits:"

    for i in range(len(card.traits.keys())):
        trait = list(card.traits.keys())[i]
        traits += "\n- [{}] {}: {}".format(i + 1,
                                           trait.title(), card.traits[trait])

    print(name)
    print(description)
    print(traits)


def compare(x, y):
    result = {}

    for trait in x.traits.keys():
        valueX = x.traits[trait]
        valueY = y.traits[trait]

        if valueX == "n/a" or valueX == "N/A":
            valueX = -float("infinity")

        if valueY == "n/a" or valueY == "N/A":
            valueY = -float("infinity")

        if valueX > valueY:
            result[trait] = x

        elif valueY > valueX:
            result[trait] = y

        else:
            result[trait] = "middle"

    return result


def print_logo():
    clear()

    for layer in LOGO.split("\n"):
        print(layer)
        sleep(0.6)

    print("")

    print(max(list(map(lambda x: len(x), LOGO.split("\n")))) * "=")

    print("")


def option_choice():
    print(
        "\t- [standard] => A gamemode where two players get a set of cards each, and they have to battle each other using the highest values on their cards."
    )

    sleep(0.5)

    print("")

    print(
        "\t- [1v1] => A gamemode where two players get 100 points which they can spend freely on three characteristics."
    )

    sleep(0.5)

    print("")

    print(
        "\t- [create] => In this section you can create your own cards to play with during standard mode."
    )

    sleep(0.5)

    print("")

    print(
        "\t- [exit] => Quit the program."
    )

    sleep(0.7)


    print("")

    AVALIABLE_OPTIONS = ["standard", "1v1",
                         "create", "exit", "s", "1", "c", "e"]

    chosen_option = input("What would you like to do? ")

    while chosen_option not in AVALIABLE_OPTIONS:
        print("")
        display("I'm sorry, I don't understand what you mean. Please try again:")
        chosen_option = input("What would you like to do? ")

    clear()
    return chosen_option

#############

### STANDARD MODE ###


def character_creation(player_num):
    name, name_confirm = "", ""

    while name_confirm is not "y":

        name = input("What's your name, Player {}? ".format(
            player_num)).title()

        while name is "":
            print("")

            print("Sorry, I think you made a mistake. Try again:")
            name = input("What's your name, Player {}? ".format(player_num))

        print("")

        name_confirm = input(
            "So you want to be called '{}'? [yes, no] ".format(name)
        ).lower()

        while name_confirm not in ["yes", "no", "y", "n"]:
            print("Sorry, I believe you've made a mistake. Try again:")

            name_confirm = input(
                "So you want to be called '{}'? [yes, no] ".format(name)
            ).lower()

        name_confirm = name_confirm[0]

        if name_confirm == "n":
            input("Ok, sure. (Press enter to go back) ")
            print("")

    return {"name": name}


def create_characters():
    print("CHARACTER CREATION:")
    input("At every step, you will need to press enter to continue (like now). ")

    print("")

    input("First, we need to create the two characters that will battle each other, so please can one of the players get ready to enter their details. ")

    print("")

    P1_name = character_creation(1)["name"]

    clear()

    input("Ok, now we need Player 2 to create their character. ")

    print("")

    P2_name = character_creation(2)["name"]

    return {"P1": P1_name, "P2": P2_name}


def card_path_to_name(path_name):
    return read_card_file("cards/{}".format(path_name))["name"]


def file_option_choice():
    json_files = [f for f in os.listdir(
        "cards") if os.path.isfile(os.path.join("cards", f))]

    json_files = list(filter(lambda x: x != "test.json", json_files))

    json_file_names = []

    for f in json_files:
        json_file_names.append(card_path_to_name(f))

    for i in range(len(json_file_names)):
        current_name = json_file_names[i]

        print("\t- [{}] {}".format(i + 1, current_name))

    print("")

    chosen_file = input("Which one would you like to chose? ")

    while chosen_file not in list(map(lambda x: str(x + 1), range(len(json_file_names)))):
        print("I'm pretty sure that's not a file option, try putting in the numbers next to the name:")
        chosen_file = input("Which one would you like to chose? ")

    chosen_file = int(chosen_file) - 1

    return json_files[chosen_file]


def card_choice():
    print("CARD CHOICE: ")
    input("Now you need to decide what deck of cards you'd like to play with. These are the options: (Press enter) ")

    print("")

    card_path = file_option_choice()

    return card_path


def summarise(P1, P2, card_path):
    card_data = read_card_file("cards/{}".format(card_path))

    print("Ok, to summarise:")

    print("")

    input("\t- Player 1, who is named '{}'. ".format(P1["name"]))
    input("\t- Player 2, who is named '{}'. ".format(P2["name"]))

    print("")

    input("You've also chosen the set of cards named '{}', which contains a total of {} cards... ".format(
        card_path_to_name(card_path), len(
            card_dict_to_card_array(card_data["cards"])
        )
    ))

    print("")

    input("These cards have to following traits/characteristics: ")

    print("")

    for i in range(len(card_data["traits"].keys())):
        trait = list(card_data["traits"].keys())[i]
        value = card_data["traits"][trait]

        input("\t- {} => {} ({}/{}) ".format(trait, value,
                                             i +
                                             1, len(card_data["traits"].keys())
                                             ))

    print("")


def warning(P1, P2):
    print("WARNING:")
    input("Whenever a screen comes up with the message: 'Avert your eyes, {}' or 'Avert your eyes, {}', the person it warns not to look should turn their head away or be prevented from looking at the next screen. ".format(
        P1["name"], P2["name"]))

    print("")

    input("This is because as soon as you hit enter, sensitive information that could ruin the game comes up on the screen if the player warned looks at it, so be careful.")


def determine_starting(P1, P2):
    print("WHO'S STARTING:")

    coin_sides = ["heads", "tails"]

    P1["coin_choice"] = input(
        "{}, do you want heads or tails? ".format(P1["name"])
    ).lower()

    while P1["coin_choice"] not in coin_sides:
        print("")
        print("I believe you mistyped something:")

        P1["coin_choice"] = input(
            "{}, do you want heads or tails? ".format(P1["name"])
        ).lower()

    P2["coin_choice"] = list(
        filter(lambda x: x != P1["coin_choice"], coin_sides))[0]

    print("")

    input(
        "Ok {}, do you want to flip the coin (by pressing enter)? ".format(P2["name"]))

    sleep(0.5)

    coin = ["heads", "tails"][random.randint(0, 1)]

    if coin == "heads":
        for i in range(5):
            clear()

            if i % 2 == 0:
                print(HEAD_COIN)

            else:
                print(TAILS_COIN)

            wait_time = 1/(i+1)
            sleep(wait_time)

        if P1["coin_choice"] == "heads":

            input("It was {}, so {} is starting! ".format(coin, P1["name"]))

            return P1

        elif P2["coin_choice"] == "heads":
            print("")
            input("It's a {}, so {} is starting! ".format(coin, P2["name"]))

            return P2

    elif coin == "tails":
        for i in range(6):
            clear()

            if i % 2 == 0:
                print(HEAD_COIN)

            else:
                print(TAILS_COIN)

            wait_time = 1/(i+1)
            sleep(wait_time)

        if P1["coin_choice"] == "tails":
            print("")
            input("It was {}, so {} is starting! ".format(coin, P1["name"]))

            return P1

        elif P2["coin_choice"] == "tails":
            print("")
            input("It's a {}, so {} is starting! ".format(coin, P2["name"]))

            return P2

    print("")


def avert_eyes(player, clear_screen=True):
    if clear_screen:
        clear()

    print("Avert your eyes, {}.".format(player.name))

    print("")

    input("Press <ENTER> to proceed. ")

    clear()


def standard():
    play = "yes"

    while play == "y" or play == "yes":
        clear()

        characters = create_characters()

        P1 = {"name": characters["P1"]}
        P2 = {"name": characters["P2"]}

        clear()

        card_path = card_choice()

        clear()

        summarise(P1, P2, card_path)

        clear()

        warning(P1, P2)

        clear()

        # ========== GAMEPLAY INIT ==========

        CARD_DATA = read_card_file("cards/{}".format(card_path))
        CARD_ARR = shuffle(card_dict_to_card_array(CARD_DATA["cards"]))

        PLAYER1 = Player(P1["name"], [])
        PLAYER2 = Player(P2["name"], [])

        MIDDLE_CARDS = []

        if len(CARD_ARR) % 2 != 0:
            MIDDLE_CARDS.append(CARD_ARR[0])
            CARD_ARR = CARD_ARR[1:]

        starting_player = determine_starting(P1, P2)

        if starting_player == P1:
            starting_player = PLAYER1

        if starting_player == P2:
            starting_player = PLAYER2

        PLAYER1.cards = CARD_ARR[:int(len(CARD_ARR)/2)]
        PLAYER2.cards = CARD_ARR[int(len(CARD_ARR)/2):]

        CURRENT_PLAYER = starting_player
        OTHER_PLAYER = list(
            filter(lambda x: x != CURRENT_PLAYER, [PLAYER1, PLAYER2])
        )[0]

        while not ((len(PLAYER1.cards) <= 0) or (len(PLAYER2.cards) <= 0)):
            CURRENT_NAME = CURRENT_PLAYER.name
            CURRENT_DECK = card_path_to_name(card_path)

            TOTAL_CARDS = len(card_dict_to_card_array(CARD_DATA["cards"]))
            CURRENT_PLAYER_CARDS = len(CURRENT_PLAYER.cards)

            CURRENT_PLAYER_CARD = CURRENT_PLAYER.cards[0]

            OTHER_NAME = OTHER_PLAYER.name
            OTHER_PLAYER_CARDS = len(OTHER_PLAYER.cards)

            OTHER_PLAYER_CARD = OTHER_PLAYER.cards[0]

            avert_eyes(OTHER_PLAYER)

            print("GAMEPLAY: {}'s Turn".format(CURRENT_NAME))
            print("=" * len("GAMEPLAY: {}'s Turn".format(CURRENT_NAME)))

            print("Info:")
            print("-----")

            print("")

            print("\t- Current Deck: {}".format(CURRENT_DECK))
            print("\t- Total Cards: {}".format(TOTAL_CARDS))

            print("")

            print("You:")
            print("----")

            print("\t- Cards You've Got: {} ({}%)".format(
                len(CURRENT_PLAYER.cards), round(
                    (100.0 * CURRENT_PLAYER_CARDS)/float(TOTAL_CARDS) * 10
                )/10
            ))

            print("\t- Cards They've Got: {} ({}%)".format(
                len(OTHER_PLAYER.cards), round(
                    (100.0 * OTHER_PLAYER_CARDS)/float(TOTAL_CARDS) * 10
                )/10
            ))

            print("")

            print("\t- Cards in Middle: {} ({}%)".format(
                len(MIDDLE_CARDS), round(
                    (100.0 * len(MIDDLE_CARDS))/float(TOTAL_CARDS) * 10
                )/10
            ))

            print("")

            print("Current Card:")
            print("-------------")

            print("")

            render_card(CURRENT_PLAYER_CARD)

            avaliable_traits = list(CARD_DATA["traits"].keys())

            print("")

            try:
                chosen_trait = int(input("Please chose a trait >>> "))
            except:
                chosen_trait = None

            while chosen_trait not in list(range(1, len(avaliable_traits) + 1)):
                print("")
                print("Uh oh. I think you put something in wrong. Try again:")

                try:
                    chosen_trait = int(input("Please chose a trait >>> "))
                except:
                    chosen_trait = None

            print("")

            chosen_trait = list(avaliable_traits)[chosen_trait - 1]
            input("Ok, you've decided to go with '{}', with a value of {}. ".format(
                chosen_trait, CURRENT_PLAYER_CARD.traits[chosen_trait]
            ))

            clear()

            print("{} has decided to go with the trait called '{}'.".format(
                CURRENT_NAME, chosen_trait))

            input("{}, you are invited to look at your card, but you can't change anything. ".format(
                OTHER_NAME))

            print("")

            avert_eyes(CURRENT_PLAYER, clear_screen=False)

            print("GAMEPLAY: {}'s Turn".format(OTHER_NAME))
            print("=" * len("GAMEPLAY: {}'s Turn".format(OTHER_NAME)))

            print("Info:")
            print("-----")

            print("")

            print("\t- Current Deck: {}".format(CURRENT_DECK))
            print("\t- Total Cards: {}".format(TOTAL_CARDS))

            print("")

            print("You:")
            print("----")

            print("\t- Cards You've Got: {} ({}%)".format(
                len(OTHER_PLAYER.cards), round(
                    (100.0 * OTHER_PLAYER_CARDS)/float(TOTAL_CARDS) * 10
                )/10
            ))

            print("\t- Cards They've Got: {} ({}%)".format(
                len(CURRENT_PLAYER.cards), round(
                    (100.0 * CURRENT_PLAYER_CARDS)/float(TOTAL_CARDS) * 10
                )/10
            ))

            print("")

            print("\t- Cards in Middle: {} ({}%)".format(
                len(MIDDLE_CARDS), round(
                    (100.0 * len(MIDDLE_CARDS))/float(TOTAL_CARDS) * 10
                )/10
            ))

            print("")

            print("Current Card:")
            print("-------------")

            print("")

            render_card(OTHER_PLAYER_CARD)

            print("")

            print("Out of these, remeber that {} went with '{}'.".format(
                CURRENT_NAME, chosen_trait))

            input("(Press <ENTER> when you're finished) ")

            clear()

            print("THE COMPARISON:")
            input("Ok, so {} chose the trait {}. ".format(
                CURRENT_NAME, chosen_trait))

            print()

            input("{}'s Card's {}: {} ".format(CURRENT_NAME, chosen_trait,
                                               CURRENT_PLAYER_CARD.traits[chosen_trait])
                  )

            input("and...")

            input("{}'s {} was... {} ".format(OTHER_NAME, chosen_trait,
                                              OTHER_PLAYER_CARD.traits[chosen_trait]))

            comparison = compare(
                CURRENT_PLAYER.cards[0], OTHER_PLAYER.cards[0]
            )

            print("")

            if comparison[chosen_trait] == CURRENT_PLAYER.cards[0]:
                print("This means that {} has won this round!".format(
                    CURRENT_PLAYER.name))
                print(
                    "For {}, they've lost... :(".format(OTHER_PLAYER.name))

                print("")

                print("This also means that {} stays on and gets to choose the next trait again!".format(
                    CURRENT_PLAYER.name))

                if CURRENT_PLAYER == PLAYER1:
                    PLAYER1.cards.append(PLAYER2.cards[0])
                    PLAYER2.cards = PLAYER2.cards[1:]

                    PLAYER1.cards.append(PLAYER1.cards[0])
                    PLAYER1.cards = PLAYER1.cards[1:]

                    PLAYER1.cards += MIDDLE_CARDS
                    MIDDLE_CARDS = []

                    CURRENT_PLAYER = PLAYER1
                    OTHER_PLAYER = PLAYER2

                elif CURRENT_PLAYER == PLAYER2:
                    PLAYER2.cards.append(PLAYER1.cards[0])
                    PLAYER1.cards = PLAYER1.cards[1:]

                    PLAYER2.cards.append(PLAYER2.cards[0])
                    PLAYER2.cards = PLAYER2.cards[1:]

                    PLAYER2.cards += MIDDLE_CARDS
                    MIDDLE_CARDS = []

                    CURRENT_PLAYER = PLAYER2
                    OTHER_PLAYER = PLAYER1

                input("\nPress <ENTER> to continue.")

            elif comparison[chosen_trait] == OTHER_PLAYER.cards[0]:
                print("This means that {} won this time!".format(
                    OTHER_PLAYER.name))
                print("This also means {} now gets to choose the trait!".format(
                    OTHER_PLAYER.name))

                print("")

                if CURRENT_PLAYER == PLAYER1:
                    PLAYER2.cards.append(PLAYER1.cards[0])
                    PLAYER1.cards = PLAYER1.cards[1:]

                    PLAYER2.cards.append(PLAYER2.cards[0])
                    PLAYER2.cards = PLAYER2.cards[1:]

                    PLAYER2.cards += MIDDLE_CARDS
                    MIDDLE_CARDS = []

                    CURRENT_PLAYER = PLAYER2
                    OTHER_PLAYER = PLAYER1

                elif CURRENT_PLAYER == PLAYER2:
                    PLAYER1.cards.append(PLAYER2.cards[0])
                    PLAYER2.cards = PLAYER2.cards[1:]

                    PLAYER1.cards.append(PLAYER1.cards[0])
                    PLAYER1.cards = PLAYER1.cards[1:]

                    PLAYER1.cards += MIDDLE_CARDS
                    MIDDLE_CARDS = []

                    CURRENT_PLAYER = PLAYER1
                    OTHER_PLAYER = PLAYER2

                input("\nPress <ENTER> to continue.")

            else:
                print(
                    "Uh-oh... They're both the same! This means we put your cards in the middle and the next person who wins gets all the cards!"
                )

                MIDDLE_CARDS.append(CURRENT_PLAYER.cards[0])
                MIDDLE_CARDS.append(OTHER_PLAYER.cards[0])

                if CURRENT_PLAYER == PLAYER1:
                    PLAYER1.cards = PLAYER1.cards[1:]
                    PLAYER2.cards = PLAYER2.cards[1:]

                    PLAYER1.cards.append(PLAYER1.cards[0])
                    PLAYER1.cards = PLAYER1.cards[1:]

                    CURRENT_PLAYER = PLAYER1
                    OTHER_PLAYER = PLAYER2

                elif CURRENT_PLAYER == PLAYER2:
                    PLAYER2.cards = PLAYER2.cards[1:]
                    PLAYER1.cards = PLAYER1.cards[1:]

                    PLAYER2.cards.append(PLAYER2.cards[0])
                    PLAYER2.cards = PLAYER2.cards[1:]

                    CURRENT_PLAYER = PLAYER2
                    OTHER_PLAYER = PLAYER1

                print("")

                print("However, it's still {}'s turn.".format(
                    CURRENT_PLAYER.name))

                input("Ok, press <ENTER> for the next round! ")

        winning = PLAYER1 if len(PLAYER1.cards) > 0 else PLAYER2

        clear()

        input("Well done {}, you've won the game! ".format(winning.name))

        print("")

        play = input("Would you like to play again? [yes, no] ").lower()

        while play not in ["yes", "no", "y", "n"]:
            print("\nIm pretty sure you made a mistake. Seriously, it's not that hard:")
            play = input("Would you like to play again? [yes, no] ").lower()


### ONE vs ONE MODE ###
def onevsone_create_character(number):
    player = {}
    clear()

    number = str(number)
    print("PLAYER {}:".format(number))

    name = super_input(
        "First, we need to find out what your name is:",
        "What's your name? ",
        str,
        "I'm sorry, something went wrong. Please try again:",
        "What's your name? "
    )

    print("")

    age = super_input(
        "Now we need to find out how old you are:",
        "How old are you? ",
        float,
        "I'm sorry, something went wrong. Please try again:",
        "How old are you? "
    )

    print("")

    return player


def onevsone_charatcer_creation():
    print("CHARACTER CREATION:")
    input("First, we need to create your two characters which you will use for battle. (Press enter) ")

    P1, P2 = {}, {}

    P1 = onevsone_create_character(1)

    return P1, P2


def onevsone():
    P1, P2 = onevsone_charatcer_creation()


#######################

### CREATE MODE ###


def create():
    pass

###################

### MAIN FUNCTION ###


def main():
    while True:
        print_logo()

        print("Welcome to TopTrumps, a python script for playing a version of TopTrumps.")

        print("")

        input("(Press <ENTER> to continue) ")

        print("")

        chosen_option = option_choice().lower()[0]

        if chosen_option == "s":
            standard()

        elif chosen_option == "1":
            onevsone()

        elif chosen_option == "c":
            create()

        elif chosen_option == "q":
            program_close()


####################

### SHH, II'S STARTING ###

if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        program_close()

##########################
