import os
def readTest(file):
	file = open(file, "r") 
	counter2 = 0
	for line in file:
		counter = 0
		params = ""
		for word in line.split(" "):
			if counter == 0:
				testFile = "test_" + word
			elif counter == 1:
				testFunction = word
			elif counter == 2:
				toTestFile = word
			elif counter == 3:
				toTestFunction = word
			elif counter == 4:
				params = word
			else:
				params = params + "," + word
			counter = counter + 1
		if os.path.exists(testFile) and counter2 != 0:
			append = 'a'
		else:
			append = 'w'
		test = open(testFile,append)
		if append == 'w':
			test.write("import "+toTestFile+"\n")
		test.write("def test_"+testFunction+"():\n\t")
	
		test.write("defValue = " + toTestFile + "." + toTestFunction + "(" +params.split("\n")[0]+")\n\t")
		test.write("assert defValue == True\n")
		
		test.close()
		counter2 =counter2 + 1
	file.close()
readTest("autotestmaker.txt")