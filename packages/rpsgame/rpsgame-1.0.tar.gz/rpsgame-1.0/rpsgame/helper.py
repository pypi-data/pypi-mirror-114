import emoji


def game_input_template(reset=True):
    if reset:
        string_template = """Welcome to the Rock Paper Scissors game!
**************************************************
        
        """
        print(string_template)
    value = input("How many games do you wanna play today? \n")
    if int(value) < 1:
        print("The number of games must be more than 0. Enter the value again")
        game_input_template(reset=False)

    return int(value)


def move_input_template():
    string_template = (
        """Enter your choice as a number:
**************************************************
(1) Rock :curling_stone:
(2) Paper :newspaper:
(3) Scissors :scissors:

"""
    )

    print(emoji.emojize(string_template))
    return int(input())


def winner_template():
    string_template = "Congrats, you won! :party_popper:"
    print(emoji.emojize(string_template))


def loss_template():
    string_template = "Tough luck. :sad_but_relieved_face:"
    print(emoji.emojize(string_template))


def tie_template():
    string_template = "Game tied!"
    print(string_template)


def move_template(player_move: str, ai_move: str):
    string_template = (
        f""":man_frowning: Your move: {player_move.capitalize()}
:robot: Computer's Move: {ai_move.capitalize()}
**************************************************

""")
    print(emoji.emojize(string_template))


def score_template(player_score: int, ai_score: int):
    string_template = (
        f"""Current score:
:man_frowning: You: {player_score}
:robot: Computer: {ai_score}
**************************************************

""")
    print(emoji.emojize(string_template))


def goodbye_template():
    string_template = ("""You have reached the end of the line.
Have a great day!
**************************************************    
""")
    print(string_template)
