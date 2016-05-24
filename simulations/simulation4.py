# Graph coloring using DPOP

import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
import agent


g3 = {1: [2,8,16],
      2: [1],
      3: [14,15],
      4: [12,13],
      5: [8],
      6: [8],
      7: [14,15],
      8: [1,5,6,9,11],
      9: [8,10],
      10: [9],
      11: [8,12,13],
      12: [4,11,16],
      13: [4,11],
      14: [3,7],
      15: [3,7,16],
      16: [1,12,15]
     }


def f(c1, c2):
    if c1 == c2:
        return -1000
    else:  # c1 != c2
        return -(c1 + c2)

agents_file = "agents-sim-4.txt"

agent1 = agent.Agent(1, [1,2,3,4,5], 
     {(1,2): f,
      (1,8): f,
      (1,16): f},
     agents_file
    )
agent2 = agent.Agent(2, [1,2,3,4,5], 
     {(2,1): f},
     agents_file
    )
agent3 = agent.Agent(3, [1,2,3,4,5], 
     {(3,14): f,
      (3,15): f},
      agents_file
    )
agent4 = agent.Agent(4, [1,2,3,4,5], 
     {(4,12): f,
      (4,13): f},
      agents_file
    )    
agent5 = agent.Agent(5, [1,2,3,4,5], 
     {(5,8): f},
     agents_file
    )
agent6 = agent.Agent(6, [1,2,3,4,5], 
     {(6,8): f},
     agents_file
    )
agent7 = agent.Agent(7, [1,2,3,4,5], 
     {(7,14): f,
      (7,15): f},
      agents_file
    )
agent8 = agent.Agent(8, [1,2,3,4,5], 
     {(8,1): f,
      (8,5): f,
      (8,6): f,
      (8,9): f,
      (8,11): f},
      agents_file
    )
agent9 = agent.Agent(9, [1,2,3,4,5], 
     {(9,8): f,
      (9,10): f},
      agents_file
    )
agent10 = agent.Agent(10, [1,2,3,4,5], 
     {(10,9): f},
     agents_file
    )
agent11 = agent.Agent(11, [1,2,3,4,5], 
     {(11,8): f,
      (11,12): f,
      (11,13): f},
      agents_file
    )
agent12 = agent.Agent(12, [1,2,3,4,5], 
     {(12,4): f,
      (12,11): f,
      (12,16): f},
      agents_file
    )
agent13 = agent.Agent(13, [1,2,3,4,5], 
     {(13,4): f,
      (13,11): f},
      agents_file
    )
agent14 = agent.Agent(14, [1,2,3,4,5], 
     {(14,3): f,
      (14,7): f},
      agents_file
    )
agent15 = agent.Agent(15, [1,2,3,4,5], 
     {(15,3): f,
      (15,7): f,
      (15,16): f},
      agents_file
    )
agent16 = agent.Agent(16, [1,2,3,4,5], 
     {(16,1): f,
      (16,12): f,
      (16,15): f},
      agents_file
    )


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
    childid = os.fork()
    children.append(childid)
    if childid == 0:
        agent5.start()
        print 'agent5:', agent5.value

if pid == os.getpid():
    childid = os.fork()
    children.append(childid)
    if childid == 0:
        agent6.start()
        print 'agent6:', agent6.value

if pid == os.getpid():
    childid = os.fork()
    children.append(childid)
    if childid == 0:
        agent7.start()
        print 'agent7:', agent7.value

if pid == os.getpid():
    childid = os.fork()
    children.append(childid)
    if childid == 0:
        agent8.start()
        print 'agent8:', agent8.value

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
        agent10.start()
        print 'agent10:', agent10.value

if pid == os.getpid():
    childid = os.fork()
    children.append(childid)
    if childid == 0:
        agent11.start()
        print 'agent11:', agent11.value

if pid == os.getpid():
    childid = os.fork()
    children.append(childid)
    if childid == 0:
        agent12.start()
        print 'agent12:', agent12.value

if pid == os.getpid():
    childid = os.fork()
    children.append(childid)
    if childid == 0:
        agent13.start()
        print 'agent13:', agent13.value

if pid == os.getpid():
    childid = os.fork()
    children.append(childid)
    if childid == 0:
        agent14.start()
        print 'agent14:', agent14.value

if pid == os.getpid():
    childid = os.fork()
    children.append(childid)
    if childid == 0:
        agent15.start()
        print 'agent15:', agent15.value

if pid == os.getpid():
    childid = os.fork()
    children.append(childid)
    if childid == 0:
        agent16.start()
        print 'agent16:', agent16.value


if pid == os.getpid():
    agent1.start()
    print 'max_util:', agent1.max_util
    print 'agent1:', agent1.value
    for i in children:
        os.wait()
