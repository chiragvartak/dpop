import utils

class Agent:
    def __init__(self, i, domain, relations):
        # Use this to initialize all agents
        # This dict will get all the values from the agents.txt file and store them.
        # Also, the domains of some agents will be added to this dict later on.
        # You can access a value as:
        # agent.agents_info[<agent_id>]['field_required']
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
        self.table =  None  # The table that will be stored
        self.IP = agents_info[i]['IP']
        self.PORT = eval(agents_info[i]['PORT'])
        self.is_root = False
        if 'is_root' in agents_info[self.i]:
            self.is_root = eval(agents_info[self.i]['is_root'])
        self.root_id = eval(agents_info[42]['root_id'])
        self.msgs = {}  # The dict where all the received messages are stored

    def getNeighbors(self):
        s = set()
        for first, second in self.relations.keys():
            s.add(second)
        return s

    def calculate_util(self, tup, xi):
        """
        Calculates the util; given a tuple 'tup' which has the assignments of
        values of parent and pseudo-parent nodes, in order; given a value 'xi'
        of this agent.
        """
        # Assumed that utilities are combined by adding to each other

        util = self.relations[(self.id, self.p)](xi, tup[0])
        for x, index in enumerate(tup[1:]):
            util = util + self.relations[(self.id, self.pp[index])](
                xi, tup[index])
        return util


def _test():
    from pprint import pprint, pformat

    # A relation that takes two variables' values as inputs
    def f(xi, xj):
        return x+y

    agent1 = Agent(1, set(7,1,4,5), {(1,2): f, (1,4): f, (1,3): f})
    pprint(vars(agent1))


if __name__ == '__main__':
    _test()
