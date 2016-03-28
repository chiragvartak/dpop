
import pytest
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from utils import *


def test_get_agents_info():
	x = get_agents_info("agents.txt")
	y = {1: {'IP': '127.0.0.1', 'PORT': '5001', 'is_root': 'True'},
    	 2: {'IP': '127.0.0.1', 'PORT': '5002'},
    	 3: {'IP': '127.0.0.1', 'PORT': '5003'},
         42: {'root_id': '1'}
    	}
	assert x == y


def test_add_dims():
    a = np.arange(4)
    x, ant = add_dims(a, (5,), 1, 8, 3)
    y = np.array(
        [[0,0,0],
         [1,0,0],
         [2,0,0],
         [3,0,0]])
    assert np.array_equal(x, y)
    assert ant == (5, 8)

    a = np.arange(12).reshape(3,4)
    x, ant = add_dims(a, (7, 9), 2, 11, 2)
    y = np.array([[[ 0, 0],
                   [ 1, 0],
                   [ 2, 0],
                   [ 3, 0]],

                  [[ 4, 0],
                   [ 5, 0],
                   [ 6, 0],
                   [ 7, 0]],

                  [[ 8, 0],
                   [ 9, 0],
                   [10, 0],
                   [11, 0]]])
    assert np.array_equal(x, y)
    assert ant == (7, 9, 11)


def test_expand():
    a = np.arange(4)
    x, ant = expand(a, (5,), (5,8), (4,3)) 
    y = np.array(
        [[0,0,0],
         [1,0,0],
         [2,0,0],
         [3,0,0]])
    assert np.array_equal(x, y)
    assert ant == (5, 8)


if __name__ == "__main__":
	pytest.main()
