"Defines the class Agent which represents a node/agent in the DPOP algorithm."

import utils
import pickle
import socket

import pseudotree_creation
import utilmsgprop
import valuemsgprop


class Agent:
    def __init__(self, i, domain, relations, agents_file):
        # Use utils.get_agents_info to initialize all the agents.
        # All the information from 'agents.txt' will be retrieved and stored in
        # this dict 'agents_info'.
        # Also, the domains of some agents will be added to this dict later on.
        # You can access a value as:
        # agent.agents_info[<agent_id>]['field_required']
        # Some miscellaneous information will be stored with id=42.
        self.agents_info = utils.get_agents_info(agents_file)
        info = self.agents_info

        self.value = -1  # The value that will be selected for this agent
        self.max_util = float("-inf")  # Will be initialized only for the root, in the end
        self.i = self.id = i
        self.domain = domain  # A list of values
        self.relations = relations  # A dict of functions, for each edge in the
                                    # graph
        self.graph_nodes = self.get_graph_nodes()  # A list of all the nodes in
                                                   # the graph, except itself
        self.neighbors = self.get_neighbors()  # A list of all the neighbors
                                               # sorted by ids
        self.p = None  # The parent's id
        self.pp = None  # A list of the pseudo-parents' ids
        self.c = None  # A list of the childrens' ids
        self.pc = None # A list of the pseudo-childrens' ids
        self.table =  None  # The table that will be stored
        self.IP = info[self.id]['IP']
        self.PORT = eval(info[self.id]['PORT'])  # Listening Port
        self.is_root = False
        if 'is_root' in info[self.i]:
            self.is_root = eval(info[self.i]['is_root'])
        self.root_id = eval(info[42]['root_id'])
        self.msgs = {}  # The dict where all the received messages are stored

    def get_graph_nodes(self):
        info = self.agents_info
        graph_nodes = []
        for key in info:
            if key != 42 and key != self.id:
                graph_nodes.append(key)
        return graph_nodes

    def get_neighbors(self):
        L = []
        for first, second in self.relations.keys():
            L.append(second)
        return sorted(L)

    def calculate_util(self, tup, xi):
        """
        Calculates the util; given a tuple 'tup' which has the assignments of
        values of parent and pseudo-parent nodes, in order; given a value 'xi'
        of this agent.
        """
        # Assumed that utilities are combined by adding to each other
        util = self.relations[self.id, self.p](xi, tup[0])
        for index, x in enumerate(tup[1:]):
            util = util + self.relations[self.id, self.pp[index]](xi, x)
        return util

    def is_leaf(self):
        "Return True if this node is a leaf node and False otherwise."

        assert self.c != None, 'self.c not yet initialized.'
        if self.c == []:
            return True
        else:
            return False

    def udp_send(self, title, data, dest_node_id):
        """
        Send a UDP message to the node whose id is given by 'dest_node_id'; the
        'title' is the message's title string and 'data' is the content object.
        """
        print str(self.id) + ': udp_send, sending a message ...' 

        info = self.agents_info
        pdata = pickle.dumps((title, data))
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(pdata, (info[dest_node_id]['IP'], int(info[dest_node_id]['PORT'])))
        sock.close()

        print str(self.id) + ': Message sent, ' + title + ": " + str(data)

    def start(self):
        print str(self.id)+': Started'
        pseudotree_creation.pseudotree_creation(self)
        utilmsgprop.util_msg_prop(self)
        if not self.is_root:
            valuemsgprop.value_msg_prop(self)
        print str(self.id)+': Finished'


def _test():
    from pprint import pprint, pformat

    # A relation that takes two variables' values as inputs
    def f(xi, xj):
        return x+y

    agent1 = Agent(1, [7, 1, 4, 5], {(1,2): f, (1,4): f, (1,3): f})
    pprint(vars(agent1))


if __name__ == '__main__':
    _test()
