import random
import copy
import time

import quebra_doce_bot as qd_bot

class QuebraDoceGenerator:

    def __init__(self, pop_size, n_kids, crossover_rate, mutation_rate):
        self.pop_size = pop_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.n_simulations = 100
        self.n_moves = 1
        self.bias = 0.00
        self.best_distance = 1.0
        self.n_kids = n_kids
    
    # Usada para avaliar o conteúdo
    def _evaluate_content(self, content):
        bot = qd_bot.QuebraDoceAI(string=content)
        return bot.do_playouts(
            n=self.n_simulations, 
            n_moves=self.n_moves,
            info=False
            )

    def generate_moves(self):
        return random.randint(5, 40)
    
    def generate_types(self):
        return random.randint(4, 6)
    
    def generate_points(self, types):
        if self.points:
            x = abs(types - 6)
            return random.randint(0, 100000 + x*20000)
        else:
            return 0

    # Gera um mapa aleatório
    def _random_level(self):
        string = ''

        # Generate the moves
        moves = self.generate_moves()

        # Generate the types
        types = self.generate_types()

        # Generate the points
        points = self.generate_points(types)

        # Write the Info
        string += str(moves) + ","
        string += str(points) + ","
        string += str(types) + "\n"

        # Generate the Level
        pieces = None
        for i in range(9):
            
            # Se não for a primeira linha, diminui o max
            if i > 0:
                pieces = self.pieces
            else:
                pieces = self.first_pieces
            
            for j in range(9):

                # Gera a peça
                p = random.choice(pieces)
                string += str(p)

                # Se não for a ultima peça, adiciona a ','
                if j != 8:
                    string += ","
            
            # Adiciona a nova linha
            string += "\n"

        # Retorna o mapa
        return string

    # Seleciona os melhores
    def _select(self, pop):
        pop.sort(key=lambda data:data['distance'])
        return pop[:2]

    # Cruza os melhores
    def _crossover(self, pop):

        child = None

        # Se estiver no crossover_rate, une os dois
        if random.uniform(0.0, 1.0) <= self.crossover_rate:
            string = ''

            p1 = pop[0]['level']
            p2 = pop[1]['level']
            
            p1_lines = p1.split("\n")
            p2_lines = p2.split("\n")

            line_1 = p1_lines[0].split(",")
            line_2 = p2_lines[0].split(",")
            for i in range(len(line_1)):
                x = int(line_1[i])
                y = int(line_2[i])
                value = random.choice([x, y])
                string += str(value)
                if i != 2:
                    string += ","
            string += "\n"

            for i in range(1, 10):
                line_1 = p1_lines[i]
                line_2 = p2_lines[i]

                for j in range(len(line_1)):
                    if line_1[j] != ",":
                        x, y = int(line_1[j]), int(line_2[j])
                        value = random.choice([x, y])
                        string += str(value)
                    else:
                        string += ","
                string += "\n"
            
            child = string

        # Caso não rolou crossover, retorna o melhor
        else:
            child = min(pop, key=lambda x:x['distance'])
            child = child['level']

        return child

    # Muta um nivel
    def _mutate(self, child, distance):
        string = ''
        
        # calcula o mutation rate
        # Quanto mais longe do resultado esperando, mais mutação
        mutation_rate = self.mutation_rate + (distance/10)
        
        # Divide as linhas
        lines = child.split("\n")
        
        # Divide as informações dos cabeçalhos
        info = lines[0].split(",")
        
        # Pega movimentos
        moves = 0
        if random.uniform(0.0, 1.0) <= mutation_rate:
            moves = self.generate_moves()
        else:
            moves = int(info[0])
        
        # Pega Tipos
        types = 0
        if random.uniform(0.0, 1.0) <= mutation_rate:
            types = self.generate_types()
        else:
            types = int(info[2])
        
        # Pega pontos
        points = 0
        if random.uniform(0.0, 1.0) <= mutation_rate:
            points = self.generate_points(types)
        else:
            points = int(info[1])

        # Escreve o cabeçalho
        string += str(moves) + ","
        string += str(points) + ","
        string += str(types) + "\n"

        # Escreve o mapa
        ps = None
        for i in range(1, 10):
            line = lines[i]
            pieces = line.split(",")

            # Se for depois da primeira linha
            if i > 1:
                ps = self.pieces
            else:
                ps = self.first_pieces

            # Percorre uma linha
            for j in range(len(pieces)):
                p = 0
                if random.uniform(0.0, 1.0) <= mutation_rate:
                    p = random.choice(ps)
                else:
                    p = pieces[j]
                
                string += str(p)
                if j != 8:
                    string += ","
            string += "\n"

        # Retorna o mapa
        return string

    # Cria filhos com a população
    def _create_kids(self, pop):

        # Decide o limite dos melhores
        limit = 10
        if self.pop_size < limit:
            limit = self.pop_size

        # Pega os melhores
        pop.sort(key=lambda x: x['distance'])
        best = pop[:limit]
        best = copy.deepcopy(best)

        # Cria os N Filhos
        kids = []
        for i in range(self.n_kids):

            # Escolhe aleatoriamente os melhores
            p1 = random.choice(best)
            p2 = random.choice(best)

            # Crossover dos pais
            kid = self._crossover([p1,p2])

            # Pega o valor de distância médio dos 2, para
            # utilizar na mutação
            value = (p1['distance'] + p2['distance'])/2

            # Muta a criança
            kid = self._mutate(kid, value)

            # Adiciona a lista de filhos
            data = {
                'level': kid,
                'evaluate': 0.0,
                'distance': 1.0
            }
            kids.append(data)
        
        # Retorna os filhos
        return kids

    # Mata os filhos ruins
    def _kill_bad(self, pop, kids, target):
        for k in kids:
            k['evaluate'] = self._evaluate_content(k['level'])
            k['distance'] = abs(k['evaluate'] - target)
            pop.append(k)
        
        pop.sort(key=lambda data:data['distance'])
        pop = pop[:self.pop_size]
        pop = copy.deepcopy(pop)
        return pop

    # Gera um mapa com o target desejado
    def generate_level(self, target, n_generations=100,
            points=False, blocks=False, canes=False):

        invalid = False

        start = time.time()

        # Confere os targets invalidos
        if target > 1.0:
            invalid = True
        elif target < 0.0:
            invalud = True
        elif target < self.bias:
            invalid = True
        elif (not points) and (not blocks) and (not canes):
            invalid = True

        # Não é possivel gerar
        if invalid:
            return False

        # Inicializa as peças
        self.first_pieces = [0, 1]
        self.pieces = [0, 1]

        # Inicializa os modos
        self.points = points
        self.blocks = blocks
        self.canes = canes

        if blocks:
            self.first_pieces.append(2)
            self.pieces.append(2)

        if canes:
            self.first_pieces.append(3)

        # Percorre tantas gerações
        target_level = None
        print("--------------------\n")
        print("Objetivo:", target)
        print("Quantidade de Gerações:", n_generations)
        print("Tamanho da População:", self.pop_size)
        print("--------------------\n")
        found = False

        # Gera uma população inicial
        pop = []
        print("[", end="")
        for i in range(self.pop_size):

            l = self._random_level()
            val = self._evaluate_content(l)
            d = abs(val - target)
            
            print("%.2f," % val, end="")

            data = {
                'level': l,
                'evaluate': val,
                'distance': d}
            pop.append(data)
        print("]")

        # Inicializa o bias
        self.bias = 0.005

        # Inicializa a melhor distância
        self.best_distance = 1.0

        for gen in range(n_generations):
            if (gen + 1) % 10 == 0:
                self.bias += 0.01

            print("Starting generation #%d\n" % gen)

            # Recebe a melhor população
            best_pop = self._select(pop)
            best_pop = copy.deepcopy(best_pop)

            # Pega a melhor distância
            if best_pop[0]['distance'] < self.best_distance:
                self.best_distance = best_pop[0]['distance']

            # Imprime a população atual
            pop.sort(key=lambda x: x['evaluate'])
            print(" - Population - ")
            print("[", end="")
            for p in pop:
                print("%.2f" % p['evaluate'], end="")
                print(",", end="")
            print("]")


            # Imprime o melhor da geração
            print(
                "Generation %d: Best ->[%.2f, %.2f]\n" % (
                    gen, 
                    best_pop[0]['evaluate'],
                    best_pop[0]['distance'])
            )

            # Se é melhor que o bias
            target_level = best_pop[0]
            if best_pop[0]['distance'] <= self.bias:
                print("Level chosen!\n")
                break

            # Cria novos filhos e elimina os piores
            kids = self._create_kids(pop)
            pop = self._kill_bad(pop, kids, target)
        else:
            print("Nenhum nível teve um target próximo do esperado.")
            print("Foi escolhido o melhor da ultima geração.")
        
        end = time.time() - start
        print("Levou %.2f segs para gerar." % end)

        self._write_info(target, target_level, end)
        self._create_file(target, target_level)
    
    def _write_info(self, target, level, t):
        file_name = ''
        file_name += "levels/"
        file_name += str(target) + "_"
        file_name += "%.2f" % level['evaluate']
        file_name += "_time_"
        file_name += ".txt"

        with open(file_name, "w+") as f:
            f.write("Tempo: %.2fs" % t)

    def _get_type_file(self):
        string = ""
        count = 0
        if self.points:
            count += 1
            string += "points"
        if self.blocks:
            count += 1
            if count > 1:
                string += "_"
            string += "protection"
        if self.canes:
            count += 1
            if count > 1:
                string += "_"
            string += "objective"
        
        return string

    def _create_file(self, target, level):
        file_name = ''
        file_name += "levels/"
        file_name += str(int(target*100)) + "_"
        file_name += str(int(level['evaluate'] * 100)) + "_"
        file_name += self._get_type_file()
        file_name += ".csv"

        with open(file_name, "w+") as f:
            f.write(level['level'])

        print("Arquivo -%s- gerado!" % file_name)
        print("--------------------\n")

for x in [0.85, 0.95]:
    print("Tentando gerar um mapa com target =", x)
    print()
    generator = QuebraDoceGenerator(25, 10, 0.75, 0.01)
    generator.generate_level(x, blocks=True, canes=True, points=True)