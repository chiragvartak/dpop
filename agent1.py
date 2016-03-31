
import agent

## Simulation 1
# add = lambda x, y: x + y
# f = {}
# f[1, 4] = lambda x1, x4: x1 - x4
# f[4, 1] = lambda x4, x1: x1 - x4
# f[1, 2] = add
# f[2, 1] = add
# f[1, 3] = lambda x1, x3: x3 - x1
# f[3, 1] = lambda x3, x1: x3 - x1
# f[2, 4] = add
# f[4, 2] = add
# agent1 = agent.Agent(1, [0, 1], 
#     {(1,4): f[1,4],
#      (1,3): f[1,3],
#      (1,2): f[1,2]})
# agent2 = agent.Agent(2, [0, 1], 
#     {(2,4): f[2,4],
#      (2,1): f[2,1]})
# agent3 = agent.Agent(3, [0, 1], {(3, 1): f[3,1]})
# agent4 = agent.Agent(4, [0, 1],
#     {(4,1): f[4,1],
#      (4,2): f[4,2]})

# Simulation 2
def f12(x1, x2):
    if (x1, x2) == (0, 0): return 3
    elif (x1, x2) == (0, 1): return 2
    elif (x1, x2) == (1, 0): return 4
    else: return 1

def f21(x2, x1):
    return f12(x1, x2)

def f13(x1, x3):
    if (x1, x3) == (0, 0): return 1
    elif (x1, x3) == (0, 1): return 2
    elif (x1, x3) == (1, 0): return 2
    else: return 1

def f31(x3, x1):
    return f13(x1, x3)

def f23(x2, x3):
    if (x2, x3) == (0, 0): return 2
    elif (x2, x3) == (0, 1): return 3
    elif (x2, x3) == (1, 0): return 1
    else: return 3

def f32(x3, x2):
    return f23(x2, x3)

def f24(x2, x4):
    if (x2, x4) == (0, 0): return 2
    elif (x2, x4) == (0, 1): return 1
    elif (x2, x4) == (1, 0): return 4
    else: return 2

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

agent1.start()

print 'max_util: ', agent1.max_util
print 'agent1: ', agent1.value
