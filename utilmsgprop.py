
from __future__ import print_function

import socket
import pickle
from itertools import product


# The function that will *actually* run in the algorithm
def main(agent):

    # If agent has no children
    if len(agent.c) == 0:
        # The message to be sent to parent
        M = {}

        # The table to be stored
        T = {}
        
        # A list that has the domains of itself, parent and all pseudoparents
        domains = [agent.domain]
        domains.append( [agent.p[1]] )
        for i, d in agent.pp:
            domains.append(d)

        pairs_combo = []
        for combos in product(*domains):
            pairs_combo.append( (agent.i, combos[0]) )
            pairs_combo.append( (agent.p[0], combos[1]) )
            for i in range(2, len(combos)):
                pairs_combo.append( (agent.pp[i-2][0], combos[i]) )

        
