import pytester as p

def test_sum():
	sumValue = p.summation(4,5)
	assert sumValue == 9
def test_sub():
	subValue = p.subtraction(6,4)
	assert subValue == 2
def test_validate():
	validateValue = p.validate("Marno","Hermann",9512205074086) and p.validate("Jan","Pompies",9512234081087)
	assert validateValue == True and p.validate("","",0)==False