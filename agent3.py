
import agent

add = lambda x, y: x + y

f = {}
f[1, 4] = lambda x1, x4: x1 - x4
f[4, 1] = lambda x4, x1: x1 - x4
f[1, 2] = add
f[2, 1] = add
f[1, 3] = lambda x1, x3: x3 - x1
f[3, 1] = lambda x3, x1: x3 - x1
f[2, 4] = add
f[4, 2] = add


agent1 = agent.Agent(1, [0, 1], 
    {(1,4): f[1,4],
     (1,3): f[1,3],
     (1,2): f[1,2]})

agent2 = agent.Agent(2, [0, 1], 
    {(2,4): f[2,4],
     (2,1): f[2,1]})

agent3 = agent.Agent(3, [0, 1], {(3, 1): f[3,1]})

agent4 = agent.Agent(4, [0, 1],
    {(4,1): f[4,1],
     (4,2): f[4,2]})

agent3.start()

print 'max_util: ', agent1.max_util
print 'agent1: ', agent1.value
print 'agent2: ', agent2.value
print 'agent3: ', agent3.value
print 'agent4: ', agent4.value