
# The 'main' function is not tested. I suspect it to be full of errors.

from __future__ import print_function

import socket
import pickle
import collections
import threading

import utils
from agent import *

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
    if agent.is_root == 0:

        # Wait till the each agent sends its neighbors' set
        while True:
            all_neighbor_msgs_arrived = True
            for neighbor in agent.neighbors:
                if ('neighbors_'+neighbor) not in msgs:
                    all_neighbor_msgs_arrived = False
                    break
            if all_neighbor_msgs_arrived == True:
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
        
        agents_info = utils.get_agents_info("agents.txt")
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

            data = pickle.dumps(('ptinfo', Relatives(p, pp, c, pc)))
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            socket.sendto(data, (agents_info[neighbor]['IP'], agents_info[neighbor]['PORT']))
            sock.close()

        # Send this node's (root's) domain to all children and pseudochildren
        # For example, if root's id is 1, the message is, in title:value form:
        # domain_1: <the set which is the domain of 1>
        p = parents[agent.id]
        c = pstree[agent.id]
        pp = []
        pc = []
        pseudo_relatives = set(graph[agent.id]) - set(parents[agent.id]) \
            - set(pstree[agent.id])
        pseudo_relatives = list(pseudo_relatives)
        for relative in pseudo_relatives:
            if depths[agent.id] < depths[relative]:
                pc.append(relative)
            else:
                pp.append(relative)

        for child in c+pc:
            data = pickle.dumps(('domain_'+str(agent.id), agent.neighbors))
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(data, (agents_info[child]['IP'], agents_info[child]['PORT']))
            sock.close()

    # Procedure for agent other than root
    else:
        data = pickle.dumps(('neighbors_'+str(agent.id), agent.neighbors))
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(data, (agents_info[agent.root_id]['IP'], agents_info[agent.root_id]['PORT']))
        sock.close()

        # Wait till the message (p, pp, c, pc) [has title: 'ptinfo'] arrives from the root
        while 'ptinfo' not in msgs:
            pass

        # Initialize all the respective fields
        agent.p, agent.pp, agent.c, agent.pc = pickle.loads(msgs['ptinfo'])

        # Send this node's domain to all children and pseudochildren
        # For example, if this node's id is 7, the message is, in title:value form:
        # domain_7: <the set which is the domain of 7>
        for child in c+pc:
            data = pickle.dumps(('domain_'+str(agent.id), agent.neighbors))
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(data, (agents_info[child]['IP'], agents_info[child]['PORT']))
            sock.close()

        # Wait for the 'domain' message from all parents and pseudoparents
        # These messages sent will have the form:
        # (domain_3, set(1, 23, 12, 41, 2, 122))
        while True:
            all_parents_msgs_arrived = True
            for parent in [agent.p]+agent.pp:
                if ('domain_'+parent) not in msgs:
                    all_parents_msgs_arrived = False
                    break
            if all_parents_msgs_arrived == True:
                break

        # Store all these domains that have arrived as messages
        for parent in [agent.p]+agent.pp:
            agent.agents_info[parent] = msgs['domain_'+parent]
