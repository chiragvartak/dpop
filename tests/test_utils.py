
import pytest
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from utils import *


def test_get_agents_info():
	x = get_agents_info("agents.txt")
	y = {1: {'IP': '127.0.0.1', 'PORT': '5001', 'is_root': 'True'},
	 	 2: {'IP': '127.0.0.1', 'PORT': '5002'},
	 	 3: {'IP': '127.0.0.1', 'PORT': '5003'}
	 	}
	assert x == y


if __name__ == "__main__":
	pytest.main()
