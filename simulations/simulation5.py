# Simulation 5 - Graph coloring on a smaller problem instance

import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
import agent


def f(c1, c2):
    if c1 == c2:
        return -1000
    else:  # c1 != c2
        return -(c1 + c2)

agents_file = "agents-sim-5.txt"

agent1 = agent.Agent(1, [1, 2, 3, 4, 5], 
     {(1,2): f,
      (1,3): f,
      (1,4): f
     },
     agents_file)
agent2 = agent.Agent(2, [1, 2, 3, 4, 5], 
    {(2,1): f,
     (2,4): f
    },
    agents_file)
agent3 = agent.Agent(3, [1, 2, 3, 4, 5],
    {(3, 1): f
    },
    agents_file)
agent4 = agent.Agent(4, [1, 2, 3, 4, 5],
    {(4,1): f,
     (4,2): f
    },
    agents_file)    

# A trick so that this process is allowed to fork.
pid = os.getpid()

children = []

if pid == os.getpid():
    childid = os.fork()
    children.append(childid)
    if childid == 0:
        agent2.start()
        print 'agent2:', agent2.value

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
        agent4.start()
        print 'agent4:', agent4.value

if pid == os.getpid():
    agent1.start()
    print 'max_util:', agent1.max_util
    print 'agent1:', agent1.value
    for i in children:
        os.wait()
