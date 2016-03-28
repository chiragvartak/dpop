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
    indices = range(len(parent_domain)) + \
        [range(len(info[x]['domain'])) for x in agent.pp]
    for item, index in zip(itertools.product(lists), itertools.product(indices)):
        max_util = -1
        xi_val = -1
        for xi in agent.domain:
            util = agent.calculate_util(item, xi)
            if util > max_util:
                max_util = util
                xi_val = xi
        util_msg[index] = max_util
        stored_table[index] = xi_val

    return (util_msg, stored_table)


def get_util_cube(agent):
    """
    Get the utility cube which will be used by a non-leaf node to combine with
    the combined cube it has generated from the util_msgs received from all the
    children.
    """

    info = agent.agents_info
    # Domain of the parent
    parent_domain = info[agent.p]['domain']
    # Calculate the dimensions of the util_msg
    # The dimensions of util_msg and table_stored will be the same.
    dim_util_msg = [len(agent.domain)] + [len(parent_domain)] + \
        [len(info[x]['domain']) for x in agent.pp]
    dim_util_msg = tuple(dim_util_msg)
    util_msg = np.zeros(dim_util_msg, dtype=int)

    lists = [parent_domain] + [info[x]['domain'] for x in agent.pp]
    indices = range(len(parent_domain)) + \
        [range(len(info[x]['domain'])) for x in agent.pp]

    for item, index in zip(itertools.product(lists), itertools.product(indices)):
        for xi, i in enumerate(agent.domain):
            util = agent.calculate_util(item, xi)
            util_msg[(i,)+index] = util

    return util_msg


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

    # Wait till util_msg from all the children have arrived
    while True:
        all_children_msgs_arrived = True
        for child in agent.c:
            if ('util_msg_'+child) not in msgs:
                all_children_msgs_arrived = False
                break
        if all_children_msgs_arrived == True:
            break

    util_msgs = []
    for child in sorted(agent.c):
        util_msgs.append(agent.msgs['util_msg_'+str(child)])
    for child in sorted(agent.c):
        util_msgs.append(agent.msgs['pre_util_msg__'+str(child)]):
    combined_msg, combined_ant = combine(util_msgs)

    info = agent.agents_info
    if agent.is_root:
        assert combined_ant == (agent.id, )

        # Choose the optimal utility
        utils = list(combined_msg)
        max_util = max(utils)
        xi_star = agent.domain[utils.index(max_util)]

        # Send 'value_msg_<rootid>' xi_star to all children and pseudo-children
        for node in c+pc:
            agent.udp_send('value_msg_'+str(agent.id), xi_star, node)
    else:
        util_cube, _ = get_util_cube(agent)
        _, agent.table = get_util_msg(agent)

        combined_cube, cube_ant = utils.combine(
            util_cube, combined_msg,
            tuple([agent.id] + [agent.p] + agent.pp), combined_ant
            )

        # Removing own dimension by taking maximum
        L_ant = list(cube_ant)
        ownid_index = L_ant.index(agent.id)
        msg_to_send = np.maximum.reduce(combined_cube, axis=ownid_index)

        agent.udp_send('util_msg_'+str(agent.id), msg_to_send, agent.p)


def util_msg_prop(agent):
    if agent.is_leaf():
        info = agent.agents_info
        util_msg, agent.table = get_util_msg(agent)

        # Send 'util_msg_<ownid>'' to parent
        agent.udp_send('util_msg_'+str(agent.id), util_msg, agent.p)

        # Send the assignment-nodeid-tuple
        agent.udp_send('pre_util_msg_'+str(agent.id),
            [agent.p]+agent.pp, agent.p)

    else:
        util_msg_handler(agent)
