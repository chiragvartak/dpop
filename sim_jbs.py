# This code will simulate a JBSSP simulation.

import os
import collections

import agent

def get_relatives(us, bss):
    """Returns a dict to tell all the other users to which a user is related
    to."""
    R = {}
    
    for idn in us:
        # Left Basestation
        left_bs = None
        min_dist = 10000
        for bs in bss:
            if bs < idn and abs(idn - bs) < min_dist:
                left_bs = bs
                min_dist = abs(idn - bs)

        # Right Basestation
        right_bs = None
        min_dist = 10000
        for bs in bss:
            if bs > idn and abs(idn - bs) < min_dist:
                right_bs = bs
                min_dist = abs(idn - bs)

        # Both left and right BS cannot be 'None'.
        assert left_bs != None or right_bs != None

        # Finding the relatives
        span = (None, None)
        if left_bs == None:
            span = (idn, right_bs + abs(right_bs - idn))
        elif right_bs == None:
            span = (left_bs - abs(left_bs - idn), idn)
        else:  # No BS is 'None'
            span = (left_bs - abs(left_bs - idn), right_bs + abs(right_bs - idn))

        for u in us:
            if u >= span[0] and u <= span[1] and u != idn:
                if idn in R:
                    R[idn].append(u)
                else:
                    R[idn] = [u]
                if u in R:
                    R[u].append(idn)
                else:
                    R[u] = [idn]

    for key in R:
        R[key] = sorted(list(set(R[key])))
    return R

def create_agent(idn, us, bss, cols, func, afile):
    # Left Basestation
    left_bs = None
    min_dist = 10000
    for bs in bss:
        if bs < idn and abs(idn - bs) < min_dist:
            left_bs = bs
            min_dist = abs(idn - bs)

    # Right Basestation
    right_bs = None
    min_dist = 10000
    for bs in bss:
        if bs > idn and abs(idn - bs) < min_dist:
            right_bs = bs
            min_dist = abs(idn - bs)

    # Both left and right BS cannot be 'None'.
    assert left_bs != None or right_bs != None

    # Creating the domain
    D = []
    if left_bs != None:
        D = D + zip([left_bs]*cols, range(1,cols+1))
    if right_bs != None:
        D = D + zip([right_bs]*cols, range(1, cols+1))

    # Creating the relations
    F = {}
    for u in get_relatives(us, bss)[idn]:
        F[(idn, u)] = func(idn, u)

    return agent.Agent(idn, D, F, afile)

def is_conflict(agent1, b1, c1, agent2, b2, c2):
    left_end_1 = b1 - abs(agent1 - b1)
    right_end_1 = b1 + abs(agent1 - b1)
    left_end_2 = b2 - abs(agent2 - b2)
    right_end_2 = b2 + abs(agent2 - b2)

    arrowhead_1 = None
    arrowhead_2 = None
    if agent1 < b1:
        arrowhead_1 = left_end_1
    else:  # agent1 > b1
        arrowhead_1 = right_end_1
    if agent2 < b2:
        arrowhead_2 = left_end_2
    else:  # agent2 > b2
        arrowhead_2 = right_end_2

    if c1 != c2:
        return False
    else:  # c1 == c2
        # Arrowhead of each one doesn't lie on the other
        if arrowhead_1 >= left_end_2 and arrowhead_1 <= right_end_2:
            return True
        if arrowhead_2 >= left_end_1 and arrowhead_2 <= right_end_1:
            return True
        return False

def f(agent1, agent2):
    def g(val1, val2):  # Both val1 and val2 are value tuples
        b1, c1 = val1
        b2, c2 = val2
        if is_conflict(agent1, b1, c1, agent2, b2, c2):
            return -1000
        else:
            return -(c1 + c2)
    return g

if __name__ == '__main__':
    ### Information to specify to simulate ###

    # User id is the same as user's position co-ordinate
    users = [3, 5, 6, 9, 12]
    root_id = 6

    # Basestation id is the same as BS's position co-ordinate
    basestations = [2, 7, 16]

    # Number of maximum colors that will be required
    colors = k = 2

    ### - - - - - - - - - - - - - - - - -  ###

    ### Information generated based on the information provided above ###

    # Creating the agents' text file
    agents_file = open("sim_jbs.txt", "w")
    agents_file.write("id=42 root_id=" + str(root_id) + "\n\n")
    for u in users:
        agents_file.write("id=" + str(u) + " ")
        agents_file.write("IP=127.0.0.1" + " ")
        agents_file.write("PORT=" + str(5000 + u) + " ")
        if u == root_id:
            agents_file.write("is_root=True" + " ")
        agents_file.write("\n\n")
    agents_file.close()

    # Creating the agents
    agents = [create_agent(i, users, basestations, k, f, "sim_jbs.txt") for i in users]

    # Running the agents
    pid = os.getpid()
    children = []

    for a in agents:
        if not a.is_root:
            if pid == os.getpid():
                childid = os.fork()
                children.append(childid)
                if childid == 0:
                    a.start()
                    print 'agent' + str(a.id) + ':', a.value        

    # Start root agent
    root_agent = agents[users.index(root_id)]
    if pid == os.getpid():
        root_agent.start()
        print 'max_util:', root_agent.max_util
        print 'agent' + str(root_agent.id) + ':', root_agent.value
        for i in children:
            os.wait()

    ### - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ###