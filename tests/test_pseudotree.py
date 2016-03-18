
import pytest
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from pseudotree import *

g1 = {1: [2,9],
      2: [1,3,16],
      3: [2,4,7,15],
      4: [3],
      5: [6],
      6: [5,7],
      7: [3,6,8,9],
      8: [7,10],
      9: [1,7,11],
      10: [8,11],
      11: [9,10,16],
      12: [13,16],
      13: [12,14],
      14: [13,15,16],
      15: [3,14],
      16: [2,11,12,14]
      }

# The graph (pseudotree) in the DPOP paper
g2 = {0: [1,2,4,11],
      1: [0,3,4,8],
      2: [0,5,6,12],
      3: [1,7,8],
      4: [0,1,9,10],
      5: [2,11,12],
      6: [2,13],
      7: [3],
      8: [1,3],
      9: [4],
      10: [4],
      11: [0,5],
      12: [2,5],
      13: [6]
      }


def test_dfsTree():
    x = dfsTree(g1, 1)
    y = {1: [2],
         2: [3],
         3: [4, 7],
         6: [5],
         7: [6, 8],
         8: [10],
         10: [11],
         11: [9, 16],
         12: [13],
         13: [14],
         14: [15],
         16: [12],
         'Nothing': [1]
        }
    assert x == y

    x = dfsTree(g2, 0)
    y = {0: [1, 2],
         1: [3, 4],
         2: [5, 6],
         3: [7, 8],
         4: [9, 10],
         5: [11, 12],
         6: [13],
         'Nothing': [0]
        }
    assert x == y


if __name__ == '__main__':
    pytest.main()
