import random
import copy
import time

import quebra_doce_bot as qd_bot

class QuebraDoceGenerator:

    def __init__(self, pop_size, n_kids, crossover_rate, mutation_rate):
        self.pop_size = pop_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.n_simulations = 50
        self.n_moves = 1
        self.bias = 0.01
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
        return random.randint(5, 75)
    
    def generate_types(self):
        return random.randint(3, 6)
    
    def generate_points(self, types):
        x = abs(types - 6)
        return random.randint(0, 100000 + x*20000)

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
        max = 3
        for i in range(9):
            
            # Se não for a primeira linha, diminui o max
            if i > 0:
                max = 2 
            
            for j in range(9):

                # Gera a peça
                p = random.randint(0, max)
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
                a = min(x, y)
                b = max(x, y)
                value = random.randint(a,b)
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
                        a, b = min(x,y), max(x,y)
                        value = random.randint(a,b)
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
    def _mutate(self, child):
        string = ''
        
        # calcula o mutation rate
        # Quanto mais longe do resultado esperando, mais mutação
        mutation_rate = self.mutation_rate + self.best_distance
        if mutation_rate > 1.0:
            mutation_rate = 1.0

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
        max = 3
        for i in range(1, 10):
            line = lines[i]
            pieces = line.split(",")

            # Se o max for maior
            if i > 1:
                max = 2

            # Percorre uma linha
            for j in range(len(pieces)):
                p = 0
                if random.uniform(0.0, 1.0) <= mutation_rate:
                    p = random.randint(0, max)
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

        kids = []
        for i in range(self.n_kids):
            p1 = random.choice(pop)
            p2 = random.choice(pop)
            kid = self._crossover([p1,p2])
            kid = self._mutate(kid)
            data = {
                'level': kid,
                'evaluate': 0.0,
                'distance': 1.0
            }
            kids.append(data)
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
    def generate_level(self, target, n_generations=100):
        invalid = False

        start = time.time()

        # Confere os targets invalidos
        if target > 1.0:
            invalid = True
        elif target < 0.0:
            invalud = True
        elif target < self.bias:
            invalid = True
        
        # Não é possivel gerar
        if invalid:
            return False

        # Gera uma população inicial
        pop = []
        for i in range(self.pop_size):
            data = {
                'level': self._random_level(),
                'evaluate': 0.0,
                'distance': 1.0}
            pop.append(data)
        
        # Percorre tantas gerações
        target_level = None
        print("Objetivo:", target)
        print("Quantidade de Gerações:", n_generations)
        print("Tamanho da População:", self.pop_size)
        print("--------------------\n")
        found = False

        # Avalia as populações originais
        print("[", end="")
        for p in pop:
            p['evaluate'] = self._evaluate_content(p['level'])
            p['distance'] = abs(p['evaluate'] - target)
            print("%.2f" % p['evaluate'], end="")
            print(",", end="")
        print("]")

        for gen in range(n_generations):
            print("Starting generation #%d" % gen)

            # Recebe a melhor população
            best_pop = self._select(pop)
            best_pop = copy.deepcopy(best_pop)

            # Pega a melhor distância
            if best_pop[0]['distance'] < self.best_distance:
                self.best_distance = best_pop[0]['distance']

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

    def _create_file(self, target, level):
        file_name = ''
        file_name += "levels/"
        file_name += str(target) + "_"
        file_name += "%.2f" % level['evaluate']
        file_name += ".csv"

        with open(file_name, "w+") as f:
            f.write(level['level'])

        print("Arquivo -%s- gerado!" % file_name)
        print("--------------------\n")

#for x in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
x = 1.0
print("Tentando gerar um mapa com target =", x)
print()
generator = QuebraDoceGenerator(25, 10, 0.75, 0.25)
generator.generate_level(x)


