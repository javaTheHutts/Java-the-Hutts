import pytester as p

def test_sum():
	sumValue = p.summation(4,5)
	assert sumValue == 9
def test_sub():
	subValue = p.subtraction(6,4)
	assert subValue == 2