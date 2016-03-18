
from __future__ import print_function

import socket
import pickle
import collections
import threading

Relatives = collections.namedtuple('Relatives', 'parent pseudoparents children pseudochildren')


def listen_func(msgs, sock):
    """
    Continuously listens on the IP and Port specified in 'sock', and stores the
    messages in the dict 'msgs', until an exit message is received. See comments
    in the source code for more information.
    """
    while True:
    	# The 'data' which is received should be the pickled string representation of a tuple.
    	# The first element of the tuple should be the data title, a name given to describe the data.
    	# This first element will become the key of the 'msgs' dict.
    	# The second element should be the actual data to be passed.
        # Loop ends when an exit message is sent.
        data, addr = sock.recvfrom(1024)
        u_data = pickle.loads(data) # Unpickled data
        msgs[u_data[0]] = u_data[1]
        if u_data[1] == "exit":
            return


def get_parents(pstree):
    """Given a pseudotree (dfsTree), get the parents for each node as a dict"""
    parents = {}
    for node, children in pstree.iteritems():
        for child in children:
            parents[child] = node
    return parents


def assign_depths(pstree):
    depths = {}
    assign_depths_helper(depths, pstree, 'Nothing', -1)
    return depths


def assign_depths_helper(depths, pstree, node, value):
    depths[node] = value
    children = []
    try:
        children = pstree[node]
    except KeyError:
        return depths
    for child in children:
        assign_depths_helper(depths, pstree, child, value+1)
    return depths


# The function that will *actually* run in the algorithm
def main(agent):
    # The dict where all the messages are stored
    msgs = {}

    # Some clock sync functionality will come here

    # Creating and starting the 'listen' thread
    listen = threading.Thread(target=listen_func, args=(msgs, listening_socket))
    listen.setDaemon(True)
    listen.start()
    
    # Procedure for the root agent
    if len(agent.c) == 0:

        # Wait till the each agent sends its neighbors' set
        while True:
            all_neighbor_msgs_arrived = True
            for neighbor in agent.neighbors:
                if ('neighbors_'+neighbor) not in msgs:
                    all_neighbor_msgss_arrived = False
                    break
            if all_neighbor_msgss_arrived == True:
                break

        # Generate the pseudotree structure
        graph = {}
        graph[agent.i] = list(agent.neighbors)
        for key, value in msgs.iteritems():
            if key[0:10] == 'neighbors_':
                graph[int(key[10])] = list(value)
        pstree = {}
        pstree = pseudotree.dfsTree(graph, agent.i)

        # Tell each agent their
        # (parent, pseudoparent, children, pseudochildren)
        parents = get_parents(pstree)
        depths = assign_depths(pstree)
        
        for neighbor in agent.neighbors:
            p = parents[neighbor]
            c = pstree[neighbor]
            pp = []
            pc = []
            pseudo_relatives = set(graph[neighbor]) - set(parents[neighbor]) \
                - set(pstree[neighbor])
            pseudo_relatives = list(pseudo_relatives)
            for relative in pseudo_relatives:
                if depths[neighbor] < depths[relative]:
                    pc.append(relative)
                else:
                    pp.append(relative)

            raise NotImplementedError
