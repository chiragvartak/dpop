"""
This module implements the functions required by the util_msg_propogation
part of the DPOP algorithm
"""

import numpy as np
import itertools
import socket
import pickle

from agent import agent


def get_util_msg(agent):
    """
    Get the util_msg to be sent to the parent and the table to be stored as
    a tuple, (util_msg, stored_table).
    """

    info = agent.agents_info
    # Domain of the parent
    parent_domain = info[agent.p]['domain']
    # Calculate the dimensions of the util_msg
    # The dimensions of util_msg and table_stored will be the same.
    dim_util_msg
        = [len(parent_domain)] + [len(info[x]['domain']) for x in agent.pp]
    dim_util_msg = dim_stored_table
        = tuple(dim_util_msg)
    util_msg = np.zeros(dim_util_msg, dtype=int)
    stored_table = np.zeros(dim_util_msg, dtype=int)

    lists = [parent_domain] + [info[x]['domain'] for x in agent.pp]
    for item in itertools.product(lists):
        max_util = -1
        xi_val = -1
        for xi in agent.domain:
            util = agent.calculate_util(item, xi)
            if util > max_util:
                max_util = util
                xi_val = xi
        util_msg[item] = max_util
        stored_table[item] = xi_val

    return (util_msg, stored_table)


def util_msg_handler(agent):
    """
    The util_msg_handler routine in the util_msg_propogation part; this method
    is run for non-leaf nodes; it waits till all the children of this agent
    have sent their util_msg, combines them, and then calculates and sends the
    util_msg to its parent; if this node is the root node, it waits till all
    the children have sent their util_msg, combines these messages, chooses the
    assignment for itself with the optimal utility, and then sends this
    assignment and optimal utility value to all its children and pseudo-
    children; assumes that the listening thread is active; given the 'agent'
    which runs this function.
    """
    


# The function that will *actually* run in the algorithm
def main(agent):
    if is_leaf(agent):
        info = agent.agents_info
        util_msg, agent.table = get_util_msg(agent)
        data = pickle.dumps(('util_msg_'+str(agent.id), util_msg))

        # Send the util_msg to parent of this agent.
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(data, (info[agent.p]['IP'], info[agent.p]['PORT']))
        sock.close()
    else:
        # Wait till util_msg from all the children have arrived
        while True:
            all_children_msgs_arrived = True
            for child in agent.c:
                if ('util_msg_'+child) not in msgs:
                    all_children_msgs_arrived = False
                    break
            if all_children_msgs_arrived == True:
                break



