"""This module contains utility functions that are used by other modules."""

import collections
import pickle
import socket

Relatives = collections.namedtuple('Relatives',
	'parent pseudoparents children pseudochildren')


def get_agents_info(filepath):
	"""
	Return a dict with that has all the information extracted from a file like
	'agents.txt'.
	"""

	f = open(filepath)
	agents_info = {}
	for line in f:
		if line.split() == [] or line[0] == '#':
			continue
		entries = dict([tuple(entry.split("=")) for entry in line.split()])
		id = int(entries['id'])
		del entries['id']
		agents_info[id] = entries
	return agents_info


def listen_func(msgs, sock):
    """
    Continuously listens on the IP and Port specified in 'sock', and stores the
    messages in the dict 'msgs', until an 'exit' message is received. See
    comments in the source code for more information.
    """
    while True:
    	# The 'data' which is received should be the pickled string
        # representation of a tuple.
    	# The first element of the tuple should be the data title, a name given
        # to describe the data.
    	# This first element will become the key of the 'msgs' dict.
    	# The second element should be the actual data to be passed.
        # Loop ends when an exit message is sent.
        data, addr = sock.recvfrom(1024)
        udata = pickle.loads(data) # Unpickled data
        msgs[udata[0]] = udata[1]
        if udata[1] == "exit":
            return
