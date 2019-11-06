class Foo:

    def __init__(self):
        self.a = 1
    
    def bar(self):

        if self.a == 1:
            self.a += 1
            return self.bar()

        print("oi meu amigo - a =", self.a)

f = Foo()

f.bar()