from abc import ABC, abstractmethod
from collections import defaultdict
import math
import random
import copy
import time
from os import listdir
from os.path import isfile, join

import board


FILE = None

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
        self.rewards = 0
    
    def get_reward(self, board):
        count = 0
        total = 0
        if self.blocks > 0:
            if self.blocks != board.blocks:
                blocks = 1/(self.blocks/(self.blocks - board.blocks))
            else:
                blocks = 0
            total += blocks
            count += 1
        
        if self.canes > 0:
            if self.canes != board.canes:
                canes = 1/(self.canes/(self.canes - board.canes))
            else:
                canes = 0
            
            total += canes
            count += 1

        if self.w_points > 0:
            points = 0
            if board.points >= self.w_points:
                points = 1
            else:
                points = board.points/self.w_points
            
            total += points
            count += 1
        
        if count > 0:
            return total/count
        else:
            return 1.0

    def best_move(self, board, n):
        moves = board.possible_moves()
        children = []
        i = 0
        while i < n:
        #for _ in range(n):
            aux = copy.deepcopy(board)
            aux.copy_level(board.level)
            move = random.choice(moves)
            try:
                aux.test_move(move[0], move[1])
                children.append((move, self.get_reward(aux)))
                i += 1
            except KeyboardInterrupt:
                exit(1)
            except:
                print("Deu probleminha, tenta de novo")
        
        move = max(children, key=lambda x: x[1])
        return move[0]

    def do_playouts(self, n=100, n_moves=1):
        board = get_board()
        self.w_points = board.w_points
        self.blocks = board.blocks
        self.canes = board.canes

        begin = time.time()
        self.rewards = 0
        i = 1

        print("\nDoing %d simulations" % n)
        print("With %d possible moves" % n_moves)
        print("In the Level: %s\n" % FILE)

        while i <= n:
        #for i in range(n):
            match = time.time()
            print("Bot play #%d" % i)

            try:
                board = get_board()
                while True:
                    if board.moves == 0 or board.is_finished():
                        break
                    
                    move = None
                    if n_moves > 1:
                        move = self.best_move(board, n_moves)
                    else:
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
                print("Reward:", self.get_reward(board))
                print("")

                if board.is_finished():
                    self.wins += 1
                
                self.rewards += self.get_reward(board)
                self.plays += 1
                i += 1
            except KeyboardInterrupt:
                exit(1)
            except:
                print("Jogada deu merda")
                print("")
        
        print("Total Plays:", self.plays)
        print("Total Wins:", self.wins)
        print("Total reward:", self.rewards)
        print("Win/Ratio:", float(self.wins/self.plays))
        print("Max points:", self.max)
        print("Min points:", self.min)
        print("Mean:", float(float(self.media)/float(self.plays)))
        print("Tempo Total:", time.time() - begin)

        if FILE is not None:
            string = FILE.replace("levels/", "")
        else:
            string = "None"
        
        with open("tests/%s_%d_%d.txt" % (string, n, n_moves), mode="w+") as f:
            f.write("Doing %d simulations\n" % n)
            f.write("With %d possible moves\n" % n_moves)
            f.write("In the Level: %s\n\n" % string)
            f.write("Total Plays: %d\n" % self.plays)
            f.write("Total Wins: %d\n" % self.wins)
            f.write("Total reward: %s\n" % self.rewards)
            f.write("Win/Ratio: %s\n" % float(self.wins/self.plays))
            f.write("Max points: %s\n" % self.max)
            f.write("Min points: %s\n" % self.min)
            f.write("Mean: %s\n" % float(float(self.media)/float(self.plays)))
            f.write("Tempo Total: %s\n" % (str(time.time() - begin)))

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
        self.board = copy.deepcopy(board)

    def find_children(self):
        return self.board.possible_moves()

    # @abstractmethod
    # def find_children(self):
    #     "All possible successors of this board state"
    #     return set()

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
    return board.Board(file=FILE)

# Pega um nível aleatório da pasta levels
def _pick_a_level():
    mypath = "levels/"
    onlyfiles = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]
    onlyfiles.append(None)
    return onlyfiles

for level in _pick_a_level():
    FILE = level
    for moves in [1,3,5,10]:
        print("----------")
        print("%s -> %d" % (FILE, moves))
        print("----------")
        bot = QuebraDoceAI(None)
        bot.do_playouts(n=100, n_moves=moves)