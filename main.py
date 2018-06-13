# SCHOOL OLLY:
# - Implement a regex search for the traits so they don't have to type it all.
# - Make it so they can change the card file from inside the program.
# - Add some DND characteters

import json
import random
import time

from os import system, name

# =========================

CARD_PATH = "cards/dnd.json"
LOGO = ".------..------..------..------..------..------..------..------..------.\n|T.--. ||O.--. ||P.--. ||T.--. ||R.--. ||U.--. ||M.--. ||P.--. ||S.--. |\n| :/\: || :/\: || :/\: || :/\: || :(): || (\/) || (\/) || :/\: || :/\: |\n| (__) || :\/: || (__) || (__) || ()() || :\/: || :\/: || (__) || :\/: |\n| '--'T|| '--'O|| '--'P|| '--'T|| '--'R|| '--'U|| '--'M|| '--'P|| '--'S|\n`------'`------'`------'`------'`------'`------'`------'`------'`------'"

TESTING = True

# =========================


def sleep(t):
    if not TESTING:
        time.sleep(t)

    else:
        pass


def chunks(l, n):
    # Completely unstolen code that chunks an array (l) up into n-sized pieces.

    for i in range(0, len(l), n):
        yield l[i:i + n]


def clear():
    # More completely unstolen code.

    # for windows
    if name == 'nt':
        for i in range(100):
            print("")

        print("==========")
        print("")

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def shuffle(array):
    # More unstolen code.

    random.shuffle(array)
    return array


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

    name = "Name: {}\n".format(card.name)

    if card.description != "":
        description = "Description: {}\n".format(
            "\n".join(chunks(card.description, 76))
        )

    else:
        description = "Description: No description provided."

    traits = "Traits:"

    for i in range(len(card.traits.keys())):
        trait = list(card.traits.keys())[i]
        traits += "\n- [{}] {}: {}".format(i + 1, trait.title(), card.traits[trait])

    print(name)
    print(description)
    print(traits)


def compare(x, y):
    result = {}

    for trait in x.traits.keys():
        valueX = x.traits[trait]
        valueY = y.traits[trait]

        if valueX == "n/a":
            valueX = -float("infinity")

        if valueY == "n/a":
            valueY = -float("infinity")

        if valueX > valueY:
            result[trait] = x

        elif valueY > valueX:
            result[trait] = y

        else:
            result[trait] = "middle"

    return result


def main():
    # The main function which handles play.
    # =====================================

    # Gameplay consists of this:
    # Both players choose their names, e.g. "Alice" & "Bob".
    # They are then dealt all the cards in their pack equally and if there is an odd number of cards then that card starts in the middle pile.
    # They toss a coin to decide who goes first, virtually of course.

    # The first player (from now on referred to as P1 & the other player P2) now gets to see the first card they have and decides a quality/trait.
    # Although the second player doesn't need to do anything, they too get to see their top card and their qualities/traits.

    # Whoever wins gets the other player's card added to their list of avaliable cards, plus whatever is in the middle (if there is any).
    # However, if the qualities are the same then the two cards get added to the middle and the current player goes again.

    # This continues like this until one player has all the cards or there are no remaining cards left.
    # Good luck, future Olly.

    clear()

    for layer in LOGO.split("\n"):
        print(layer)
        sleep(0.6)

    print("")

    # Just a super hacky, fast way of printing a bar the length of the logo. Forgive me.
    print(max(list(map(lambda x: len(x), LOGO.split("\n")))) * "=")

    print("")

    print("Welcome to TopTrumps, a python script where you can play Top Trumps through a command-prompt because why not?")
    print("To start, we need the two players to define their names and stuff.")

    print("")

    input("Please press <ENTER> to continue. ")

    clear()

    print("Ok, this is player creation for PLAYER 1:")

    print("")

    while True:
        P1_name = input("What's your name? ").title()

        P1_name_confirm = input(
            "Ok, you want your name to be '{}'? [y, n] ".format(P1_name)
        )

        P1_name_confirm = P1_name_confirm[0].lower()

        if P1_name_confirm == "y":
            print("")

            print("Setting...")

            print("")
            sleep(0.5)
            break

        elif P1_name_confirm == "n":
            print("Oh, ok...")
            print("")

            continue

        else:
            print("I'm not sure what you mean, assuming you want to go back.")
            print("")

            continue

    print("I mean, that's basically it... What else is there other than name...")
    sleep(2)

    clear()

    print("Ok, this is player creation for PLAYER 2:")
    print("")

    while True:
        P2_name = input("What's your name? ").title()

        P2_name_confirm = input(
            "Ok, you want your name to be '{}'? [y, n] ".format(P2_name)
        )

        P2_name_confirm = P2_name_confirm[0].lower()

        if P2_name_confirm == "y":
            print("")

            print("Setting...")

            print("")
            sleep(0.5)
            break

        elif P2_name_confirm == "n":
            print("Oh, ok...")
            print("")

            continue

        else:
            print("I'm not sure what you mean, assuming you want to go back.")
            print("")

            continue

    print("I don't know what else to ask for...")
    sleep(2)

    clear()

    print("Ok, character creation is complete! (Isn't this fun!)")

    print("")

    print("You two players:")
    print("-- PLAYER 1, who is called '{}'.".format(P1_name))
    print("-- PLAYER 2, who is called '{}'.".format(P2_name))

    print("")

    input("Press <ENTER> to continue. ")

    clear()

    print("Now we just need to shuffle the deck...")

    sleep(2)

    print("")

    print("*Card riffling sounds*")
    sleep(1)

    print("*Snap of cards against table*")
    sleep(1)

    print("*Splitting of the deck*")
    sleep(2)

    print("")

    print("Wow, that was cringyer than I expected.")

    sleep(1.5)

    print("")

    card_data = read_card_file(CARD_PATH)

    print("You've chosen the '{}' deck.".format(card_data["name"]))

    sleep(2)

    clear()

    print("Ok, I think we can finally play...")

    print("")

    input("Press <ENTER> to continue.")

    clear()

    # ========== GAMEPLAY INIT ==========

    PLAYER1 = Player(P1_name, [])
    PLAYER2 = Player(P2_name, [])

    MIDDLE_CARDS = []

    card_arr = card_dict_to_card_array(card_data["cards"])

    card_arr = shuffle(card_arr)

    print("Oh wait, no we're not.")

    if len(card_arr) % 2 != 0:
        # Cards have an even length.
        input("Since there's an odd number of cards, it means we need to put one 'in the middle'. Press <ENTER> to continue. ")

        print("Ok, a random card has been selected and put in the middle.")

        MIDDLE_CARDS.append(card_arr[0])
        card_arr = card_arr[1:]

    print("")

    starting = PLAYER1 if random.randint(1, 2) == 1 else PLAYER2

    print("We also need to determine who is going first. We can do this using the super hard method of letting the computer pick for you. In fact, I have no idea why I'm saying this.")

    print("")

    sleep(2)

    print("I can't be bothered, let's just say '{}' is starting.".format(starting.name))

    sleep(2)

    input("Press <ENTER> to continue.")

    clear()

    sleep(3)

    CURRENT_PLAYER = starting

    OTHER_PLAYER = list(
        filter(lambda x: x != CURRENT_PLAYER, [PLAYER1, PLAYER2])
    )[0]

    print("Oh wait, one more thing.")
    print("Make sure that the player who isn't starting doesn't see the next screen. It's the card you have and showing it would kind of defeat the point.")

    print("")

    print("In fact, in general, unless a screen comes up saying that you need to swap, don't let the other player see your screen.")

    print("")

    input("Ok... I think that's all. Maybe. Press <ENTER> to continue.")

    clear()

    sleep(2.4)

    PLAYER1.cards = card_arr[:int(len(card_arr)/2)]  #  Splits it in two.
    PLAYER2.cards = card_arr[int(len(card_arr)/2):]

    # ============ GAME PLAY ============

    while not (len(PLAYER1.cards) <= 0 or len(PLAYER2.cards) <= 0):
        clear()
        print("GAMEPLAY: {}".format(CURRENT_PLAYER.name))
        print("====================")
        print("Middle: There are {} cards in the middle.".format(len(MIDDLE_CARDS)))

        print("")

        print("It's currently {}'s turn.".format(CURRENT_PLAYER.name))

        print("")

        print("You currently have {} cards. You lose when you reach 0.".format(
            len(CURRENT_PLAYER.cards)))

        print("")

        render_card(CURRENT_PLAYER.cards[0])

        avaliable_traits = list(card_data["traits"].keys())

        print("")

        print("Please select a quality to challenge them on:")

        try:
            chosen_trait = int(input(">>> ").lower())

        except:
            chosen_trait = float("infinity")

        if chosen_trait not in list(range(1, len(avaliable_traits) + 1)):
            print("I'm sorry, I don't understand. Try again.")
            sleep(2)

            continue

        else:
            chosen_trait = list(avaliable_traits)[chosen_trait - 1]
            input("Awesome. Let's see who wins. Press <ENTER> to continue. ")

            clear()

            print("(You can show the screen now)")

            print("{}, {} has chosen the trait to challenge you on.".format(
                OTHER_PLAYER.name, CURRENT_PLAYER.name)
            )

            input("\nPlease don't let {} see, and we'll look at you card, {}. (Press <ENTER> to continue) ".format(
                CURRENT_PLAYER.name, OTHER_PLAYER.name)
            )

            clear()
            print("GAMEPLAY: {}".format(OTHER_PLAYER.name))
            print("====================")
            print("Middle: There are {} cards in the middle.".format(
                len(MIDDLE_CARDS)))

            print("")

            print("It's currently {}'s turn.".format(OTHER_PLAYER.name))

            print("")

            print("You currently have {} cards. You lose when you reach 0.".format(
                len(OTHER_PLAYER.cards)))

            print("")

            render_card(OTHER_PLAYER.cards[0])

            print("")

            input("When you're ready, press <ENTER> to continue. ")

            clear()

            print("(You can both look now)")
            print("Ok, let's see who wins...")

            sleep(3)

            input("(When you press <ENTER>) ")

            sleep(1)

            comparison = compare(
                CURRENT_PLAYER.cards[0], OTHER_PLAYER.cards[0])

            print("")

            if comparison[chosen_trait] == CURRENT_PLAYER.cards[0]:
                print("For {}, YAY! They've won! ".format(CURRENT_PLAYER.name))
                print("For {}, NAY! They've lost... :(".format(OTHER_PLAYER.name))

                print("")

                print("This also means that {} stays on and gets to choose the next trait again!".format(
                    CURRENT_PLAYER.name))

                if CURRENT_PLAYER == PLAYER1:
                    PLAYER1.cards.append(PLAYER2.cards[0])
                    PLAYER2.cards = PLAYER2.cards[1:]

                    PLAYER1.cards.append(PLAYER1.cards[0])
                    PLAYER1.cards = PLAYER1.cards[1:]

                    CURRENT_PLAYER = PLAYER1
                    OTHER_PLAYER = PLAYER2

                elif CURRENT_PLAYER == PLAYER2:
                    PLAYER2.cards.append(PLAYER1.cards[0])
                    PLAYER1.cards = PLAYER1.cards[1:]

                    PLAYER2.cards.append(PLAYER2.cards[0])
                    PLAYER2.cards = PLAYER2.cards[1:]

                    CURRENT_PLAYER = PLAYER2
                    OTHER_PLAYER = PLAYER1

                input("\nPress <ENTER> to continue.")

            elif comparison[chosen_trait] == OTHER_PLAYER.cards[0]:
                print("Unfortunately, {} won this time.".format(OTHER_PLAYER.name))
                print("This also means {} now gets to choose the trait!".format(
                    OTHER_PLAYER.name))

                print("")

                if CURRENT_PLAYER == PLAYER1:
                    PLAYER2.cards.append(PLAYER1.cards[0])
                    PLAYER1.cards = PLAYER1.cards[1:]

                    PLAYER2.cards.append(PLAYER2.cards[0])
                    PLAYER2.cards = PLAYER2.cards[1:]

                    CURRENT_PLAYER = PLAYER2
                    OTHER_PLAYER = PLAYER1

                elif CURRENT_PLAYER == PLAYER2:
                    PLAYER1.cards.append(PLAYER2.cards[0])
                    PLAYER2.cards = PLAYER2.cards[1:]

                    PLAYER1.cards.append(PLAYER1.cards[0])
                    PLAYER1.cards = PLAYER1.cards[1:]

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

                input("Ok, press <ENTER> to continue.")

    # ===================================


if __name__ == '__main__':
    main()
