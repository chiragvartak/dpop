"""
This module implements the functions required by the util_msg_propogation
part of the DPOP algorithm
"""

import numpy as np
import itertools
import socket
import pickle

import agent
import utils

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
    dim_util_msg = \
        [len(parent_domain)] + [len(info[x]['domain']) for x in agent.pp]
    dim_util_msg = dim_stored_table = tuple(dim_util_msg)
    util_msg = np.empty(dim_util_msg, dtype=object)
    stored_table = np.empty(dim_util_msg, dtype=object)

    lists = [parent_domain] + [info[x]['domain'] for x in agent.pp]
    indices = [range(len(parent_domain))] + \
        [range(len(info[x]['domain'])) for x in agent.pp]

    for item, index in zip(itertools.product(*lists), itertools.product(*indices)):
        max_util = agent.max_util
        xi_val = -1
        for xi in agent.domain:
            util = agent.calculate_util(item, xi)
            if util > max_util:
                max_util = util
                xi_val = xi
        util_msg[index] = max_util
        stored_table[index] = xi_val

    agent.table_ant = tuple([agent.p] + agent.pp)

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
    util_msg = np.empty(dim_util_msg, dtype=object)

    lists = [parent_domain] + [info[x]['domain'] for x in agent.pp]
    indices = [range(len(parent_domain))] + \
        [range(len(info[x]['domain'])) for x in agent.pp]

    for item, index in zip(itertools.product(*lists), itertools.product(*indices)):
        for i, xi in enumerate(agent.domain):
            util = agent.calculate_util(item, xi)
            util_msg[(i,)+index] = util

    return util_msg, dim_util_msg


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
            if ('util_msg_'+str(child)) not in agent.msgs:
                all_children_msgs_arrived = False
                break
        if all_children_msgs_arrived == True:
            break

    util_msgs = []
    for child in sorted(agent.c):
        util_msgs.append(agent.msgs['util_msg_'+str(child)])
    for child in sorted(agent.c):
        util_msgs.append(agent.msgs['pre_util_msg_'+str(child)])

    # Combine the util_msgs received from all children
    combined_msg, combined_ant = utils.combine(*util_msgs)

    info = agent.agents_info
    if agent.is_root:
        assert combined_ant == (agent.id, )

        # Choose the optimal utility
        utilities = list(combined_msg)
        max_util = max(utilities)
        xi_star = agent.domain[utilities.index(max_util)]
        agent.value = xi_star
        agent.max_util = max_util

        # Send the index of assigned value
        D = {}
        ind = agent.domain.index(xi_star)
        D[agent.id] = ind        
        for node in agent.c:
            agent.udp_send('value_msg_'+str(agent.id), D, node)
    else:
        util_cube, _ = get_util_cube(agent)

        # Combine the 2 cubes
        combined_cube, cube_ant = utils.combine(
            util_cube, combined_msg,
            tuple([agent.id] + [agent.p] + agent.pp), combined_ant
            )

        # Removing own dimension by taking maximum
        L_ant = list(cube_ant)
        ownid_index = L_ant.index(agent.id)
        msg_to_send = np.maximum.reduce(combined_cube, axis=ownid_index)
        # Ant to send in pre_util_msg
        ant_to_send = cube_ant[:ownid_index] + cube_ant[ownid_index+1:]

        # Creating the table to store
        cc = combined_cube
        table_shape = list(cc.shape[:])
        del table_shape[ownid_index]
        table_shape = tuple(table_shape)
        
        table = np.zeros(table_shape, dtype=object)
        cc_rolled = np.rollaxis(cc, ownid_index)
        for i, abc in enumerate(cc_rolled):
            for index, _ in np.ndenumerate(abc):
                if abc[index] == msg_to_send[index]:
                    table[index] = agent.domain[i]
        agent.table = table
        agent.table_ant = ant_to_send

        # Send the assignment-nodeid-tuple
        agent.udp_send('pre_util_msg_'+str(agent.id),
            ant_to_send, agent.p)

        agent.udp_send('util_msg_'+str(agent.id), msg_to_send, agent.p)


def util_msg_prop(agent):

    print str(agent.id)+': Begin util_msg_prop'

    if agent.is_leaf():
        info = agent.agents_info
        util_msg, agent.table = get_util_msg(agent)

        # Send the assignment-nodeid-tuple
        agent.udp_send('pre_util_msg_'+str(agent.id),
            tuple([agent.p]+agent.pp), agent.p)

        # Send 'util_msg_<ownid>'' to parent
        agent.udp_send('util_msg_'+str(agent.id), util_msg, agent.p)

    else:
        util_msg_handler(agent)

    print str(agent.id)+': End util_msg_prop'
