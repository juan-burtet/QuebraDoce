'''
Classe que Controla a quantidade de Simulações feitas e guarda o
Human Sucess Rate do campo passado
'''
class QuebraDoceAI:

    def __init__(self, board):
        self.board = board # Campo que contem o jogo
        self.plays = 0 # Quantidade de jogdadas
        self.wins = 0 # Quantidade de vitórias
        pass

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
class Node:

    def __init__(self):
        pass