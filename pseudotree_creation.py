
from __future__ import print_function

import socket
import pickle


# The agent's IP
IP = '127.0.0.1'
# The port where the agent listens for messages
PORT = 5005

listening_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print('Listening socket created')
listening_socket.bind((IP, PORT))
print('Listening socket bound to port')
print("%s:%d" % (IP, PORT))


def listen_func(msg, sock):
    while True:
    	# The 'data' which is received should be the pickled string representation of a tuple.
    	# The first element of the tuple should be the data title, a name given to describe the data.
    	# This first element will become the key of the 'msg' dict.
    	# The second element should be the actual data to be passed.
        data, addr = sock.recvfrom(1024)
        u_data = pickle.loads(data) # Unpickled data
        msg[u_data[0]] = u_data[1]
        if u_data[1] == "exit":
            return


def main(agent):
    import threading
    
    # The dict where all the messages are stored
    msg = {}

    # Some clock sync functionality will come here

    # Creating the 'listen' thread
    listen = threading.Thread(target=listen_func, args=(msg, listening_socket))
    listen.setDaemon(True)
    listen.start()
    
    # start the listen (daemon) thread
   

if __name__ == '__main__':
    import threading
    from pprint import pprint

    msg = {}
    listen = threading.Thread(target=listen_func, args=(msg, listening_socket))
    listen.setDaemon(True)
    listen.start()
    
    listening_socket.sendto(pickle.dumps(('greeting', "Kiss kiss to you too")), ("127.0.0.1", 5005))
    listening_socket.sendto(pickle.dumps(('name', "Rachel")), ("127.0.0.1", 5005))
    listening_socket.sendto(pickle.dumps((50, "Montana")), ("127.0.0.1", 5005))
    listening_socket.sendto(pickle.dumps(('food', (125, 'Hamburger'))), ("127.0.0.1", 5005))
    listening_socket.sendto(pickle.dumps((0, "exit")), ("127.0.0.1", 5005))
    listening_socket.sendto(pickle.dumps(('ghosts', "shouldn't exist")), ("127.0.0.1", 5005))
    listen.join()
    
    msg2 = {'greeting': "Kiss kiss to you too",
    		'name': "Rachel",
    		50: "Montana",
    		'food': (125, "Hamburger"),
    		0: "exit"
    	   }
    assert msg == msg2
    
    listening_socket.close()
    print('Listening socket closed')

    pprint(msg)

