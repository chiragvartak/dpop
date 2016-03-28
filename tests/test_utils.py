
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


def test_combine():
    a = np.array([0,1,2,3])
    a_ant = (7,)
    b = np.array([0,1,2])
    b_ant = (9,)
    x, merged_ant = combine(a, b, a_ant, b_ant)
    y = np.array(
        [[0, 1, 2],
         [1, 2, 3],
         [2, 3, 4],
         [3, 4, 5]]
        )
    assert np.array_equal(x, y)
    assert merged_ant == (7, 9)

    a = np.array([0,1,2,3])
    a_ant = (7,)
    b = np.array([0,1,2,3])
    b_ant = (9,)
    x, merged_ant = combine(a, b, a_ant, b_ant)
    y = np.array(
        [[0, 1, 2, 3],
         [1, 2, 3, 4],
         [2, 3, 4, 5],
         [3, 4, 5, 6]]
        )
    assert np.array_equal(x, y)
    assert merged_ant == (7, 9)

    a = np.array([0,1,2,3])
    a_ant = (7,)
    b = np.array([0,1,2,3])
    b_ant = (7,)
    x, merged_ant = combine(a, b, a_ant, b_ant)
    y = np.array([0,2,4,6])
    assert np.array_equal(x, y)
    assert merged_ant == (7,)

    a = np.arange(12).reshape(3,4)
    a_ant = (7,9)
    b = np.arange(12).reshape(3,4)
    b_ant = (7,9)
    x, merged_ant = combine(a, b, a_ant, b_ant)
    y = np.arange(12).reshape(3,4) * 2
    assert np.array_equal(x, y)
    assert merged_ant == (7, 9)

    a = np.arange(12).reshape(3,4)
    a_ant = (8,9)
    b = np.arange(12).reshape(3,4)
    b_ant = (7,9)
    x, merged_ant = combine(a, b, a_ant, b_ant)
    y = np.array([[[ 0, 2, 4, 6],
                   [ 4, 6, 8,10],
                   [ 8,10,12,14]],

                  [[ 4, 6, 8,10],
                   [ 8,10,12,14],
                   [12,14,16,18]],

                  [[ 8,10,12,14],
                   [12,14,16,18],
                   [16,18,20,22]]])
    print x
    print
    print y
    assert np.array_equal(x, y)
    assert merged_ant == (7, 8, 9)


def test_add_dims():
    a = np.arange(4)
    x, ant = add_dims(a, (5,), 1, 8, 3)
    y = np.array(
        [[0,0,0],
         [1,1,1],
         [2,2,2],
         [3,3,3]])
    assert np.array_equal(x, y)
    assert ant == (5, 8)

    a = np.arange(12).reshape(3,4)
    x, ant = add_dims(a, (7, 9), 2, 11, 2)
    y = np.array([[[ 0, 0],
                   [ 1, 1],
                   [ 2, 2],
                   [ 3, 3]],

                  [[ 4, 4],
                   [ 5, 5],
                   [ 6, 6],
                   [ 7, 7]],

                  [[ 8, 8],
                   [ 9, 9],
                   [10, 10],
                   [11, 11]]])
    assert np.array_equal(x, y)
    assert ant == (7, 9, 11)


def test_expand():
    a = np.arange(4)
    x, ant = expand(a, (5,), (5,8), (4,3)) 
    y = np.array(
        [[0,0,0],
         [1,1,1],
         [2,2,2],
         [3,3,3]])
    assert np.array_equal(x, y)
    assert ant == (5, 8)


if __name__ == "__main__":
	pytest.main()
