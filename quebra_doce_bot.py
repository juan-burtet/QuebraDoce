from abc import ABC, abstractmethod
from collections import defaultdict
import math
import random
import copy
import time

import board

'''
Classe que Controla a quantidade de Simulações feitas e guarda o
Human Sucess Rate do campo passado
'''
class QuebraDoceAI:

    def __init__(self, board):
        self.board = board # Campo que contem o jogo
        self.plays = 0 # Quantidade de jogdadas
        self.wins = 0 # Quantidade de vitórias
        self.max = -1
        self.min = 99999999
        self.media = 0
    
    def do_playouts(self, n=10000):
        board = None

        begin = time.time()
        for i in range(n):
            match = time.time()
            i += 1
            print("Bot play #%d" % i)

            board = get_board()
            while True:
                if board.moves == 0 or board.is_finished():
                    break
                
                moves = board.possible_moves()
                move = random.choice(moves)
                board.test_move(move[0], move[1])
            
            if board.points > self.max:
                self.max = board.points
            if board.points < self.min:
                self.min = board.points
            self.media += board.points 

            print("Points: %d/%d" % (board.points, board.w_points))
            print("Moves:", board.moves)
            print("Blocks:", board.blocks)
            print("Canes:", board.canes)
            print("Tempo:", time.time() - match)
            print("")

            if board.is_finished():
                self.wins += 1
            self.plays += 1
        
        print("Total Plays:", self.plays)
        print("Total Wins:", self.wins)
        print("Win/Ratio:", float(self.wins/self.plays))
        print("Max points:", self.max)
        print("Min points:", self.min)
        print("Mean:", float(float(self.media)/float(self.plays)))
        print("Tempo Total:", time.time() - begin)

'''
Classe que funciona como uma Monte Carlo Tree Search, que
faz uma jogada do jogo e indica se houve vitória ou não
'''
class MCTS:

    def __init__(self):
        pass

'''
Classe que funciona como um Nó para a MCTS
'''
class Node(ABC):
    """
    A representation of a single board state.
    MCTS works by constructing a tree of these Nodes.
    Could be e.g. a chess or checkers board state.
    """

    def __init__(self, board):
        self.board = board

    @abstractmethod
    def find_children(self):
        "All possible successors of this board state"
        return set()

    @abstractmethod
    def find_random_child(self):
        "Random successor of this board state (for more efficient simulation)"
        return None

    @abstractmethod
    def is_terminal(self):
        "Returns True if the node has no children"
        return True

    @abstractmethod
    def reward(self):
        "Assumes `self` is terminal node. 1=win, 0=loss, .5=tie, etc"
        return 0

    @abstractmethod
    def __hash__(self):
        "Nodes must be hashable"
        return 123456789

    @abstractmethod
    def __eq__(node1, node2):
        "Nodes must be comparable"
        return True

def get_board():
    return board.Board(file="levels/level13.csv")

bot = QuebraDoceAI(None)
bot.do_playouts()