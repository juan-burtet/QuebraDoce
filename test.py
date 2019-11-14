import multiprocessing as mp
import random
from multiprocessing import Lock, Process, Queue, current_process
import queue

class Foo:
    

    def jar(self, i, results):
        data = {}

        data['Oi'] = random.randint(0, 5)
        data['Tchau'] = random.randint(0, 5)

        # print("Processo:", i)
        # print("Oi:", data['Oi'])
        # print("Tchau", data['Tchau'])

        #r = data
        return i

    def bar(self):
        self.results = Queue()
        procs = []
        for i in range(mp.cpu_count()):

            proc = Process(target=self.jar, args=(i,self.f))
            procs.append(proc)
            proc.start()
            
        for proc in procs:
            print(proc.join())

foo = Foo()
foo.bar()
print(foo.f)
# results = foo.results
# for data in results:
#     print(data)