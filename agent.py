
class Agent:
    def getNeighbors(self):
        s = set()
        for first, second in self.relations.keys():
            s.add(second)
        return s
    
    def __init__(self, i, domain, relations):
        self.i = i
        # self.value = # The current assigned value to this variable (agent).
        self.domain = domain # A set of values
        self.relations = relations
        self.neighbors = self.getNeighbors() # A set of all the neighbors
        # self.p = # A tuple (id, domain)
        # self.pp = # A list of tuples of the above form
        # self.c = # A list of tuples of the above form
        # self.pc = # A list of tuples of the above form
        # table = 
        self.listeningIP = ''
        self.listeningPort = -1
        

def _test():
    from pprint import pprint, pformat

    # A relation that takes two variables' values as inputs
    def f(xi, xj):
        return x+y

    agent1 = Agent(1, set(7,1,4,5), {(1,2): f, (1,4): f, (1,3): f})
    pprint(vars(agent1))


if __name__ == '__main__':
    _test()
