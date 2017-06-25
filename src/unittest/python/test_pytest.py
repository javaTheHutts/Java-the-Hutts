import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))
from main.python import pytester as p

def test_sum():
	sumValue = p.summation(4,5)
	assert sumValue == 9