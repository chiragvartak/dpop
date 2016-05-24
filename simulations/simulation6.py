# Simulation 6 - JBS on a problem with 5 users and 2 Basestations

import os
import collections
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
import agent


# def arrowhead(agent, b):
#     """Gives the co-ordinate of the arrowhead for the user whose position is
#     given by 'agent' and basestation assigned is given by 'b'."""

#     assert agent != b, "You cannot have a user and a BS in the same position."

#     left_end = b - abs(agent - b)
#     right_end = b + abs(agent - b)
#     if agent < b:
#         return left_end
#     else:  # agent > b
#         return right_end


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


# Value = collections.namedtuple("Value", "basestation color")

def f(agent1, agent2):
    def g(val1, val2):  # Both val1 and val2 are value tuples
        b1, c1 = val1
        b2, c2 = val2
        if is_conflict(agent1, b1, c1, agent2, b2, c2):
            return -1000
        else:
            return -(c1 + c2)
    return g


agents_file = "agents-sim-6.txt"

D1 = zip([4]*5, range(1,6))
# >>> [(4, 1), (4, 2), (4, 3), (4, 4), (4, 5)]

D2 = zip([8]*5, range(1,6))
# >>> [(8, 1), (8, 2), (8, 3), (8, 4), (8, 5)]

agent3 = agent.Agent(3, D1, 
     {(3,5): f(3,5),
      (3,6): f(3,6),
     },
     agents_file)

agent5 = agent.Agent(5, D1+D2, 
     {(5,3): f(5,3),
      (5,6): f(5,6),
      (5,9): f(5,9),
      (5,12): f(5,12),
     },
     agents_file)

agent6 = agent.Agent(6, D1+D2, 
     {(6,3): f(6,3),
      (6,5): f(6,5),
      (6,9): f(6,9),
      (6,12): f(6,12),
     },
     agents_file)

agent9 = agent.Agent(9, D2, 
     {(9,5): f(9,5),
      (9,6): f(9,6),
      (9,12): f(9,12),
     },
     agents_file)

agent12 = agent.Agent(12, D2, 
     {(12,5): f(12,5),
      (12,6): f(12,6),
      (12,9): f(12,9),
     },
     agents_file)

# A trick so that this process is allowed to fork.
pid = os.getpid()

children = []

if pid == os.getpid():
    childid = os.fork()
    children.append(childid)
    if childid == 0:
        agent3.start()
        print 'agent3:', agent3.value

if pid == os.getpid():
    childid = os.fork()
    children.append(childid)
    if childid == 0:
        agent5.start()
        print 'agent5:', agent5.value

if pid == os.getpid():
    childid = os.fork()
    children.append(childid)
    if childid == 0:
        agent9.start()
        print 'agent9:', agent9.value

if pid == os.getpid():
    childid = os.fork()
    children.append(childid)
    if childid == 0:
        agent12.start()
        print 'agent12:', agent12.value

# Root agent
if pid == os.getpid():
    agent6.start()
    print 'max_util:', agent6.max_util
    print 'agent6:', agent6.value
    for i in children:
        os.wait()
