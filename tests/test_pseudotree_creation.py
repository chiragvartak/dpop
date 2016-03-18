
import threading
import pytest
import sys
import os
from pprint import pprint

sys.path.insert(1, os.path.join(sys.path[0], '..'))
import pseudotree as ps
import test_pseudotree as tps
from pseudotree_creation import *


def test_listen_func():
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
    listen = threading.Thread(target=listen_func, args=(msgs, listening_socket))
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


def test_get_parents():        
    G = tps.g1
    x = get_parents(ps.dfsTree(G, 1))
    y = {1:'Nothing', 2:1, 3:2, 4:3, 7:3, 5:6, 6:7, 8:7, 10:8,
         11:10, 9:11, 16:11, 13:12, 14:13, 15:14, 12:16
        }
    assert x == y

    G = tps.g2
    x = get_parents(ps.dfsTree(G, 0))
    y = {0:'Nothing', 1:0, 2:0, 3:1, 4:1, 5:2, 6:2, 7:3, 8:3,
         9:4, 10:4, 11:5, 12:5, 13:6
        }
    assert x == y

    ## Test assign_depths
    G = tps.g1
    x = assign_depths(ps.dfsTree(G, 1))
    y = {'Nothing':-1, 1:0, 2:1, 3:2, 4:3, 7:3, 6:4, 8:4, 10:5,
         11:6, 9:7, 16:7, 12:8, 13:9, 14:10, 15:11, 5:5
        }
    assert x == y

    G = tps.g2
    x = assign_depths(ps.dfsTree(G, 0))
    y = {'Nothing':-1, 0:0, 1:1, 2:1, 3:2, 4:2, 5:2, 6:2, 7:3,
         8:3, 9:3, 10:3, 11:3, 12:3, 13:3
        }
    assert x == y


if __name__ == '__main__':
    pytest.main()
