
import threading
import pytest
import sys
import os
from pprint import pprint

sys.path.insert(1, os.path.join(sys.path[0], '..'))
import pseudotree as ps
import test_pseudotree as tps
from pseudotree_creation import *


if __name__ == '__main__':
    pytest.main()
