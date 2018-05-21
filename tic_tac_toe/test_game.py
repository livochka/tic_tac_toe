# The main module of the tic-tac-toe game
# Representing the tic-tac-toe game against the bot
# Includes hard and easy modes

from tic_tac_toe.board import GameBoard
from tic_tac_toe.players import Player, AI, AIUpgraded


class Play:
    """
    Created to run tic-tac-toe game
    """

    MODES = {'hard': AIUpgraded, 'easy': AI}

    def __init__(self):
        self.difficulty = self._get_level()
        self.board = GameBoard()

    def _get_level(self):
        """
        Created to get game difficulty from the user
        return: the level of difficulty
        """
        while True:
            level = input('Enter the game difficulty, (easy, hard): ')
            if level in self.MODES.keys():
                return level

    def _get_first(self):
        """
        Getting the first-move player
        return: who will be first
        """
        while True:
            answer = input('Enter who will make the first move, (user, bot): ')
            if answer in {'user', 'bot'}:
                return answer
            else:
                print('Must be user or bot!')

    def play(self):
        """
        Running the game
        """
        bot = self.MODES[self.difficulty](self.board, '0')
        player = Player(self.board, 'X')
        first = self._get_first()
        if first == 'user':
            first, second = player, bot
        else:
            first, second = bot, player

        # Let`s play!
        self.board.draw()
        while not self.board.condition():
            print('\nFirst, your turn!\n')
            first.make_move()
            print('\n')
            self.board.draw()
            if not self.board.condition():
                print('Second turn!')
                second.make_move()
                print('\n')
                self.board.draw()

        print('Congratulation!')
        print(self.board.condition())


if __name__ == '__main__':
    game = Play()
    game.play()
