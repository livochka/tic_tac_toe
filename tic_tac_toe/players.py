from trees_easy.linked_binary_tree import LinkedBinaryTree
from tic_tac_toe.decision_tree import Tree
from random import randrange
from copy import deepcopy


class ImpossibleMove(Exception):
    pass


class PlayerADT:
    """
    Representation of the abstract player
    """

    def __init__(self, board, mark):
        self.mark = mark
        self.game_board = board

    def make_move(self):
        """
        Making a move in the game
        """
        return self.turn()


class Player(PlayerADT):
    """
    Representing a human-instance player
    """

    def get_data(self):
        """
        Getting the data about the next move from user
        return: tuple, coordinates of move
        """
        available = self.game_board.find_empty()
        while True:
            try:
                answer = input('Enter row and column of your move separated '
                               'by whitespace: ')
                answer = tuple(map(int, answer.split()))
                if answer in available:
                    return answer
                raise ImpossibleMove
            except ValueError:
                print('Incorrect value of row or column')
            except ImpossibleMove:
                print('Move is not possible')

    def turn(self):
        """
        Processing the player turn
        """
        position = self.get_data()
        self.game_board.add(position[0], position[1], self.mark)


class AI(PlayerADT):
    """
    Representation of bot-instance player
    """
    HUMAN = 'X'

    def _score(self, board):
        """
        Created to estimate the decision
        board: game board
        """
        decision = LinkedBinaryTree(board)

        def recurse(decision):
            """
            Recursive function to estimate the bunch of random variants
            decision: binary tree structure
            return: the score of decision
            """
            brd = decision.get_root_val()
            condition = brd.condition()

            if not condition:
                available = brd.find_empty()

                person_move = available.pop(randrange(len(available)))
                brd.add(person_move[0], person_move[1], self.HUMAN)

                if len(available) > 1:
                    m1 = available.pop(randrange(len(available)))
                    m2 = available.pop(randrange(len(available)))
                    decision.insert_left(make_move(brd, m1, self.mark))
                    decision.insert_right(make_move(brd, m2, self.mark))
                    return recurse(decision.get_right_child()) + \
                           recurse(decision.get_left_child())

                elif len(available) == 1:
                    m1 = available.pop(randrange(len(available)))
                    decision.insert_left(make_move(brd, m1, self.mark))
                    return recurse(decision.get_left_child())

                else:
                    return recurse(decision)
            elif condition.startswith('D'):
                return 0
            elif condition.startswith('X'):
                return -1
            else:
                return 1

        def make_move(brd, pos, mark):
            """
            brd: game board with current condition
            pos: coordinates of position to add a mark
            mark: player mark in game
            return: board with added mark
            """
            brd = deepcopy(brd)
            brd.add(pos[0], pos[1], mark)
            return brd

        return recurse(decision)

    def _play_scenario(self, position):
        """
        Playing a scenario of move
        position: coordinates of position of the first move
        """
        brd = deepcopy(self.game_board)
        brd.add(position[0], position[1], self.mark)
        decision = self._score(brd)
        return decision

    def turn(self):
        """
        Handle a bot-instance turn
        """
        available = self.game_board.find_empty()
        if len(available) > 1:
            move1 = available.pop(randrange(len(available)))
            decision1 = self._play_scenario(move1)
            move2 = available.pop(randrange(len(available)))
            decision2 = self._play_scenario(move2)
            decision = max((decision1, move1), (decision2, move2))[1]
            self.game_board.add(decision[0], decision[1], self.mark)
        else:
            move = available[0]
            self.game_board.add(move[0], move[1], self.mark)


class AIUpgraded(AI):
    """
    Upgraded bot for tic-tac-toe game
    """

    def _score(self, board):
        """
        Created to estimate all decisions
        board: copy of the current game board
        return: decision score
        """
        decision = Tree(board)

        def recurse(decision):
            """
            Recursive function to estimate all possible scenarios
            decision: tree data structure
            return: the score of decision
            """
            brd = decision.get_root()
            condition = brd.condition()

            if not condition:
                available = brd.find_empty()
                for i in available:
                    decision.add(make_move(brd, i, self.HUMAN))

                for decis in decision:
                    brd_n = decis.get_root()
                    available = brd_n.find_empty()
                    if not available:
                        return recurse(decis)
                    for i in available:
                        decis.add(make_move(brd_n, i, self.mark))
                return sum([recurse(i) for x in decision for i in x])

            elif condition.startswith('D'):
                return 0
            elif condition.startswith('X'):
                return -2
            else:
                return 1

        def make_move(brd, pos, mark):
            """
            brd: game board with current condition
            pos: coordinates of position to add a mark
            mark: player mark in game
            return: board with added mark
            """
            brd = deepcopy(brd)
            brd.add(pos[0], pos[1], mark)
            return brd

        return recurse(decision)

    def turn(self):
        available = self.game_board.find_empty()
        if len(available) > 8:
            best = available[-1]
        else:
            decisions = []
            for i in available:
                score = self._play_scenario(i)
                decisions.append((score, i))
            best = max(decisions)[1]
        self.game_board.add(best[0], best[1], self.mark)
