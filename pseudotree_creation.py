
from __future__ import print_function

import socket
import pickle
import collections
import threading

Relatives = collections.namedtuple('Relatives', 'parent pseudoparents children pseudochildren')


def _listen_func(msgs, sock):
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


def _get_parents(pstree):
    """Given a pseudotree (dfsTree), get the parents for each node as a dict"""
    parents = {}
    for node, children in pstree.iteritems():
        for child in children:
            parents[child] = node
    return parents


def _assign_depths(pstree):
    depths = {}
    _assign_depths_helper(depths, pstree, 'Nothing', -1)
    return depths


def _assign_depths_helper(depths, pstree, node, value):
    depths[node] = value
    children = []
    try:
        children = pstree[node]
    except KeyError:
        return depths
    for child in children:
        _assign_depths_helper(depths, pstree, child, value+1)
    return depths


# The function that will *actually* run in the algorithm
def main(agent):
    # The dict where all the messages are stored
    msgs = {}

    # Some clock sync functionality will come here

    # Creating and starting the 'listen' thread
    listen = threading.Thread(target=_listen_func, args=(msgs, listening_socket))
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
        parents = _get_parents(pstree)
        depths = _assign_depths(pstree)
        
        for neighbor in agent.neighbors:
            p = parents[neighbor]
            c = pstree[neighbor]
            pp = []
            pc = []
            pseudo_relatives = set(graph[neighbor]) - set(parents[neighbor])
                - set(pstree[neighbor])
            pseudo_relatives = list(pseudo_relatives)
            for relative in pseudo_relatives:
                if depths[neighbor] < depths[relative]:
                    pc.append(relative)
                else:
                    pp.append(relative)

            raise NotImplementedError


def _test():
    import threading
    from pprint import pprint

    ## Test _listen_func
    # The agent's IP
    IP = '127.0.0.1'
    # The port where the agent listens for messages
    PORT = 5005

    listening_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('Listening socket created')
    listening_socket.bind((IP, PORT))
    print('Listening socket bound to port')
    print("%s:%d" % (IP, PORT))    

    msgs = {}
    listen = threading.Thread(target=_listen_func, args=(msgs, listening_socket))
    listen.setDaemon(True)
    listen.start()
    
    listening_socket.sendto(pickle.dumps(('greeting', "Kiss kiss to you too")), ("127.0.0.1", 5005))
    listening_socket.sendto(pickle.dumps(('name', "Rachel")), ("127.0.0.1", 5005))
    listening_socket.sendto(pickle.dumps((50, "Montana")), ("127.0.0.1", 5005))
    listening_socket.sendto(pickle.dumps(('food', (125, 'Hamburger'))), ("127.0.0.1", 5005))
    listening_socket.sendto(pickle.dumps((0, "exit")), ("127.0.0.1", 5005))
    listening_socket.sendto(pickle.dumps(('ghosts', "shouldn't exist")), ("127.0.0.1", 5005))
    listen.join()
    
    msgs2 = {'greeting': "Kiss kiss to you too",
            'name': "Rachel",
            50: "Montana",
            'food': (125, "Hamburger"),
            0: "exit"
           }
    assert msgs == msgs2
    listening_socket.close()
    print('Listening socket closed')
    pprint(msgs)

    ## Test _get_parents
    import pseudotree as ps
    
    G = ps.g1
    x = _get_parents(ps.dfsTree(G, 1))
    y = {1:'Nothing', 2:1, 3:2, 4:3, 7:3, 5:6, 6:7, 8:7, 10:8,
         11:10, 9:11, 16:11, 13:12, 14:13, 15:14, 12:16
        }
    assert x == y

    G = ps.g2
    x = _get_parents(ps.dfsTree(G, 0))
    y = {0:'Nothing', 1:0, 2:0, 3:1, 4:1, 5:2, 6:2, 7:3, 8:3,
         9:4, 10:4, 11:5, 12:5, 13:6
        }
    assert x == y

    ## Test _assign_depths
    G = ps.g1
    x = _assign_depths(ps.dfsTree(G, 1))
    y = {'Nothing':-1, 1:0, 2:1, 3:2, 4:3, 7:3, 6:4, 8:4, 10:5,
         11:6, 9:7, 16:7, 12:8, 13:9, 14:10, 15:11, 5:5
        }
    assert x == y

    G = ps.g2
    x = _assign_depths(ps.dfsTree(G, 0))
    y = {'Nothing':-1, 0:0, 1:1, 2:1, 3:2, 4:2, 5:2, 6:2, 7:3,
         8:3, 9:3, 10:3, 11:3, 12:3, 13:3
        }
    assert x == y


if __name__ == '__main__':
    _test()