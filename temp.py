import numpy as np

a = np.arange(4)
a = np.expand_dims(a, axis=1)
print a
print '---'

a = a.copy()
print a
print '---'

a = a.resize(4, 3, refcheck=False)
print a
print '---'