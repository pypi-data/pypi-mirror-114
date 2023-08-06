import random
import time

from rpsgame.logic import Move, State
from rpsgame.logic import determine_winner
import rpsgame.helper as helper


class Game:
    def __init__(self):
        self.player_score = 0
        self.ai_score = 0

    def _determine_result(self):
        """
        Based on the user provided move and the computer
        generated move, the winner is decided.

        Returns
        -------

        """
        player_state, ai_state = determine_winner(self.player_move, self.ai_move)
        helper.move_template(self.player_move.name, self.ai_move.name)

        if player_state.value == ai_state.value:
            helper.tie_template()
        elif player_state.value > ai_state.value:
            helper.winner_template()
        else:
            helper.loss_template()

        return player_state, ai_state

    def _update_player_scores(self, player_state: State, ai_state: State):
        """
        Updates the score of the user.
        (Determined from the moves)

        Returns
        -------

        """
        self.player_score += player_state.value
        self.ai_score += ai_state.value

    def _get_player_move(self):
        """
        Gets the input from the player.

        Returns
        -------

        """
        try:
            self.player_move = Move(helper.move_input_template() - 1)
        except ValueError:
            print("Please enter a valid choice")
            self._get_player_move()

    def _generate_ai_move(self):
        """
        Generates a random move for the ai player.
        (or for the player if there is a timeout)

        Returns
        -------

        """
        self.ai_move = Move(random.randint(0, 2))

    def start(self):
        """
        Starts a game between the player and the computer.

        Returns
        -------

        """
        # Picking the number of games to be played
        no_of_games = helper.game_input_template()

        while no_of_games > 0:
            # Getting the player's move
            self._get_player_move()
            # Getting the computer generated move
            self._generate_ai_move()
            # Updating the score after generating outcome
            self._update_player_scores(*self._determine_result())
            time.sleep(1)
            # Showing the scores
            helper.score_template(self.player_score, self.ai_score)
            no_of_games -= 1
            time.sleep(1)

        if self.player_score > self.ai_score:
            print("You have won this time...")
        else:
            print("Better luck next time!")

        helper.goodbye_template()
