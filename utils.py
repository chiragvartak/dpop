"""This module contains utility functions that are used by other modules."""

import collections
import pickle
import socket
import numpy as np

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


def combine(arrays, *ants):
	"""Return the combined array, given n numpy arrays and their corresponding
	n assignment-nodeid-tuples ('ants')."""

	assert len(arrays) == len(ants)

	# Calculate the merged ant
	merged_ant = set()
	for ant in ants:
		merged_ant = merged_ant | set(ant)
	merged_ant = tuple(sorted(tuple(merged_ant)))

	raise NotImplementedError


def expand(array, ant, new_ant, new_shape):
	"""Return the new numpy array after expanding it so that its ant changes
	from 'ant' to 'new_ant'. The value of the new elements created will be
	initialized to 0."""

	# The values of the nodeids in ant and new_ant must be sorted.
	assert new_ant == tuple(sorted(new_ant))

	ant = tuple(sorted(ant))
	a = array.copy()
	x = y = -1
	i = j = 0
	end_of_ant_reached = False

	while(i != len(new_ant)):
		x = new_ant[i]
		try:
			y = ant[j]
		except:
			end_of_ant_reached = True

		if x < y:
			a, ant = add_dims(a, ant, j, x, new_shape[i])
			i += 1
			j += 1
			continue
		elif x > y:
			if not end_of_ant_reached:
				j += 1
			else:
				a, ant = add_dims(a, ant, j, x, new_shape[i])
				i += 1
				j += 1
			continue
		else: #  x == y
			i += 1
			j += 1
			continue

	return (a, ant)


def add_dims(array, ant, index, nodeid, depth):
	"""Return a numpy array with an additional dimension in the place of index.
	The values of all additional elements created are 0. The depth of the 
	'nodeid' is given by 'depth'."""

	assert ant == tuple(sorted(ant))

	a = array.copy()
	a = np.expand_dims(a, axis=index)
	zeros = np.zeros(a.shape[:-1] + (depth-1,), dtype=int)
	a = np.concatenate((a, zeros), axis=index)
	new_ant = list(ant)
	print new_ant
	new_ant.insert(index, nodeid)
	print new_ant
	new_ant = tuple(new_ant)
	print new_ant
	return (a, new_ant)


def prod(S):
	"""Returns the product of all elements in a sequence S."""

	product = 1
	for i in S:
		product = product * i
	return product
