from enum import Enum


class Move(Enum):
    rock = 0
    paper = 1
    scissors = 2


class State(Enum):
    tie = 1
    win = 1
    loss = 0


def determine_winner(move_1: Move, move_2: Move) -> tuple:
    """
    Determines the state of the players/


    Parameters
    ----------
    move_1: :class: `GameObject`
    move_2: :class: `GameObject`

    Returns
    -------
    :class: `tuple`
    Enum object of the state of player
    """

    if move_1 == move_2:
        return State["tie"], State["tie"]
    elif (move_1.value + 1) % 3 == move_2.value:
        return State["loss"], State["win"]
    else:
        return State["win"], State["loss"]
