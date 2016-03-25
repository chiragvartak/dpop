import utils

class Agent:
    def getNeighbors(self):
        s = set()
        for first, second in self.relations.keys():
            s.add(second)
        return s
    
    def __init__(self, i, domain, relations):
        # Use this to initialize all agents
        agents_info = utils.get_agents_info("agents.txt")

        self.i = self.id = i
        self.value = None  # The current assigned value to this variable (agent).
        self.domain = domain  # A set of values
        self.relations = relations  # A dict of functions for each edge in the graph
        self.neighbors = self.getNeighbors()  # A set of all the neighbors
        self.p = None  # The parent's id
        self.pp = None  # A list of the pseudoparents' ids
        self.c = None  # A list of the childrens' ids
        self.pc = None # A list of the pseudochildrens' ids
        # table =  # I don't remember why I had made this
        self.IP = agents_info[i]['IP']
        self.PORT = eval(agents_info[i]['PORT'])
        self.is_root = eval(agents_info[i]['is_root'])
        self.root_id = eval(agents_info[42]['root_id'])


def _test():
    from pprint import pprint, pformat

    # A relation that takes two variables' values as inputs
    def f(xi, xj):
        return x+y

    agent1 = Agent(1, set(7,1,4,5), {(1,2): f, (1,4): f, (1,3): f})
    pprint(vars(agent1))


if __name__ == '__main__':
    _test()
