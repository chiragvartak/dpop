# The agent's IP
IP = '127.0.0.1'
# The port where the agent listens for messages
PORT = 5005

def listen_func(msg):
    import socket
    import pickle

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((IP, PORT))

    while True:
        data, addr = sock.recvfrom(1024)
        u_data = pickle.loads(data) # Unpickled data
        msg[u_data[0]] = u_data[1]

def main(agent):
    import threading
    
    # The dict where all the messages are stored
    msg = {}

    # Some clock sync functionality will come here

    # Creating the 'listen' thread
    listen = threading.Thread(target=listen_func, args=(msg,))
    listen.setDaemon(True)
    listen.start()
    
    # start the listen (daemon) thread
    
