
def value_msg_prop(agent):

    print str(agent.id)+': Begin value_msg_prop'

    # Wait till value_msg from all parents and pseudo-parents have arrived.
    while True:
        all_parent_msgs_arrived = True
        for node in [agent.p]+agent.pp:
            if ('value_msg_'+str(node)) not in agent.msgs:
                all_parent_msgs_arrived = False
                break
        if all_parent_msgs_arrived == True:
            break

    index = []
    for nodeid in [agent.p]+agent.pp:
        domain = agent.msgs['domain_'+str(nodeid)]
        index.append(domain.index(agent.msgs['value_msg_'+str(nodeid)]))
    index = tuple(index)
    agent.value = agent.table[index]

    for child in agent.c+agent.pc:
        agent.udp_send('value_msg_'+str(agent.id), agent.value, child)

    print str(agent.id)+': End value_msg_prop'