
import os

import agent

def f12(x1, x2):
    if (x1, x2) == (0, 0): return -3
    elif (x1, x2) == (0, 1): return -2
    elif (x1, x2) == (1, 0): return -4
    else: return -1

def f21(x2, x1):
    return f12(x1, x2)

def f13(x1, x3):
    if (x1, x3) == (0, 0): return -1
    elif (x1, x3) == (0, 1): return -2
    elif (x1, x3) == (1, 0): return -2
    else: return -1

def f31(x3, x1):
    return f13(x1, x3)

def f23(x2, x3):
    if (x2, x3) == (0, 0): return -2
    elif (x2, x3) == (0, 1): return -3
    elif (x2, x3) == (1, 0): return -1
    else: return -3

def f32(x3, x2):
    return f23(x2, x3)

def f24(x2, x4):
    if (x2, x4) == (0, 0): return -2
    elif (x2, x4) == (0, 1): return -1
    elif (x2, x4) == (1, 0): return -4
    else: return -2

def f42(x4, x2):
    return f24(x2, x4)

agent1 = agent.Agent(1, [0, 1], 
     {(1,3): f13,
      (1,2): f12})
agent2 = agent.Agent(2, [0, 1], 
    {(2,4): f24,
     (2,1): f21,
     (2,3): f23})
agent3 = agent.Agent(3, [0, 1],
    {(3, 1): f31,
     (3, 2): f32})
agent4 = agent.Agent(4, [0, 1], {(4,2): f42})    

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

