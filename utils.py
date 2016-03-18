"""This module contains utility functions that are used by other modules."""

def get_agents_info(filepath):
	"""Return a dict with that has all the info extracted from a file like 'agents.txt'."""
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
